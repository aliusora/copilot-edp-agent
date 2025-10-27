# app.py
"""
Streamlit UI for using GPT-4o via the OpenAI Response API with automated Microsoft Learn content retrieval.
"""

import os
import streamlit as st
from openai import OpenAI
import requests
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import re
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

# ----------------------------
# Configuration & Setup
# ----------------------------

def _load_openai_api_key() -> str | None:
    # 1) Prefer environment variable (works locally & in many hosts)
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    # 2) Fall back to Streamlit secrets if available
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None

OPENAI_API_KEY = _load_openai_api_key()
if not OPENAI_API_KEY:
    st.error(
        "Missing OpenAI API key. Set environment variable OPENAI_API_KEY "
        "or add it to .streamlit/secrets.toml (OPENAI_API_KEY = \"sk-...\")."
    )
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ----------------------------
# Microsoft Learn Content Provider
# ----------------------------

class DocumentCache:
    """Simple file-based cache for documentation with TTL support."""
    
    def __init__(self, cache_dir: str = ".doc_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.metadata_file = self.cache_dir / "metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata from disk."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save_metadata(self):
        """Save cache metadata to disk."""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception:
            pass
    
    def _get_cache_key(self, url: str) -> str:
        """Generate a unique cache key from URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def get(self, url: str) -> str | None:
        """Retrieve cached content if valid, else None."""
        cache_key = self._get_cache_key(url)
        
        # Check if cached and not expired
        if cache_key in self.metadata:
            cached_at = datetime.fromisoformat(self.metadata[cache_key]['cached_at'])
            if datetime.now() - cached_at < self.ttl:
                cache_file = self.cache_dir / f"{cache_key}.txt"
                if cache_file.exists():
                    try:
                        with open(cache_file, 'r', encoding='utf-8') as f:
                            return f.read()
                    except Exception:
                        pass
        return None
    
    def set(self, url: str, content: str):
        """Store content in cache with metadata."""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{cache_key}.txt"
        
        try:
            # Save content
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update metadata
            self.metadata[cache_key] = {
                'url': url,
                'cached_at': datetime.now().isoformat(),
                'size': len(content)
            }
            self._save_metadata()
        except Exception:
            pass
    
    def clear_expired(self):
        """Remove expired cache entries."""
        expired_keys = []
        for cache_key, meta in self.metadata.items():
            cached_at = datetime.fromisoformat(meta['cached_at'])
            if datetime.now() - cached_at >= self.ttl:
                expired_keys.append(cache_key)
                cache_file = self.cache_dir / f"{cache_key}.txt"
                if cache_file.exists():
                    cache_file.unlink()
        
        for key in expired_keys:
            del self.metadata[key]
        
        if expired_keys:
            self._save_metadata()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_size = sum(meta.get('size', 0) for meta in self.metadata.values())
        return {
            'entries': len(self.metadata),
            'total_size_kb': total_size / 1024,
            'cache_dir': str(self.cache_dir)
        }

class MicrosoftLearnMCP:
    """Fetches relevant documentation from Microsoft Learn with full article extraction."""
    
    BASE_SEARCH_URL = "https://learn.microsoft.com/api/search"
    BASE_CONTENT_URL = "https://learn.microsoft.com"
    
    # UNC-specific and NIH-related authoritative sources
    UNC_ENTERPRISE_SOURCES = [
        {
            'title': 'UNC ITS - Microsoft 365 Copilot for UNC',
            'url': 'https://its.unc.edu/ai/copilot/',
            'context': 'unc copilot enterprise deployment university',
            'summary': 'UNC Information Technology Services official guidance on Microsoft 365 Copilot deployment, access, and enterprise data protection for UNC-Chapel Hill users.'
        },
        {
            'title': 'UNC Employee Handbook - Generative AI Policy',
            'url': 'https://handbook.unc.edu/generativeai.html',
            'context': 'unc policy generative ai guidelines university',
            'summary': 'UNC-Chapel Hill institutional policy on the responsible use of generative AI tools, including guidelines for employees and faculty regarding data privacy, security, and acceptable use.'
        },
        {
            'title': 'UNC AI Initiative - Research & Generative AI Usage Guidance',
            'url': 'https://ai.unc.edu/research-generative-ai-usage-guidance/',
            'context': 'unc research ai guidance best practices university',
            'summary': 'UNC AI Initiative guidance for researchers using generative AI tools, covering best practices, ethical considerations, data protection, and compliance requirements for academic research.'
        },
        {
            'title': 'UNC School of Medicine - Safe Uses and Best Practices of AI Tools',
            'url': 'https://www.med.unc.edu/spo/2025/04/safe-uses-and-best-practices-of-ai-tools-at-unc/',
            'context': 'unc medical school ai safety best practices healthcare',
            'summary': 'UNC School of Medicine guidelines for safe and effective use of AI tools in healthcare settings, including patient data protection, HIPAA compliance, and clinical best practices.'
        },
        {
            'title': 'UNC Policies - Generative AI in Teaching and Research',
            'url': 'https://policies.unc.edu/TDClient/2833/Portal/KB/ArticleDet?ID=131244',
            'context': 'unc policy teaching research academic ai university',
            'summary': 'Official UNC-Chapel Hill policy on the use of generative AI in teaching and research contexts, including academic integrity, student privacy, and faculty responsibilities.'
        },
        {
            'title': 'NIH - AI Use in Research Applications Policy',
            'url': 'https://grants.nih.gov/news-events/nih-extramural-nexus-news/2025/07/apply-responsibly-policy-on-ai-use-in-nih-research-applications-and-limiting-submissions-per-pi',
            'context': 'nih grants research ai policy applications federal',
            'summary': 'National Institutes of Health policy on the responsible use of AI in research grant applications, including disclosure requirements, limitations on AI-generated content, and guidelines for principal investigators.'
        },
        {
            'title': 'NIH Notice - Use of Generative AI Technologies in NIH Grant Applications',
            'url': 'https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html',
            'context': 'nih notice ai grant applications policy federal',
            'summary': 'Official NIH notice providing guidance on the acceptable use of generative AI technologies in grant applications, including requirements for transparency, attribution, and quality assurance.'
        }
    ]
    
    def __init__(self, cache_enabled: bool = True, cache_ttl_hours: int = 24):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html'
        })
        self.cache_enabled = cache_enabled
        self.cache = DocumentCache(ttl_hours=cache_ttl_hours) if cache_enabled else None
        
        # Clear expired entries on initialization
        if self.cache:
            self.cache.clear_expired()
    
    def _should_include_unc_sources(self, query: str) -> bool:
        """
        Determine if UNC/NIH-specific sources should be included based on query content.
        """
        query_lower = query.lower()
        
        # UNC-related keywords
        unc_keywords = ['unc', 'university of north carolina', 'chapel hill', 'carolina', 'university']
        
        # NIH-related keywords
        nih_keywords = ['nih', 'grant', 'research', 'federal', 'funding', 'application']
        
        # Check if query mentions UNC or NIH
        has_unc = any(keyword in query_lower for keyword in unc_keywords)
        has_nih = any(keyword in query_lower for keyword in nih_keywords)
        
        return has_unc or has_nih
    
    def _get_relevant_unc_sources(self, query: str) -> List[Dict[str, str]]:
        """
        Get UNC/NIH sources relevant to the query based on context matching.
        """
        query_lower = query.lower()
        relevant_sources = []
        
        for source in self.UNC_ENTERPRISE_SOURCES:
            # Calculate simple relevance based on context keywords
            context_lower = source['context'].lower()
            query_terms = query_lower.split()
            
            # Count matching terms
            matches = sum(1 for term in query_terms if len(term) > 3 and term in context_lower)
            
            # Include if there are matches or if it's a general UNC/Copilot query
            if matches > 0 or ('copilot' in query_lower and 'unc' in context_lower):
                relevant_sources.append({
                    'title': source['title'],
                    'url': source['url'],
                    'summary': source['summary'],
                    'content': source['summary'],  # Use summary as content for UNC sources
                    '_matches': matches,
                    '_is_unc_source': True  # Flag to skip web scraping
                })
        
        # Sort by relevance (match count)
        relevant_sources.sort(key=lambda x: x.get('_matches', 0), reverse=True)
        
        # Remove match count metadata but keep UNC flag
        for src in relevant_sources:
            src.pop('_matches', None)
        
        # Return top 3 most relevant UNC sources
        return relevant_sources[:3]
    
    def _enhance_query(self, query: str) -> str:
        """
        Enhance user query with relevant keywords for better search precision.
        Adds context-aware keywords to improve relevance.
        """
        # Core topics related to Copilot and data protection
        enhancement_keywords = []
        query_lower = query.lower()
        
        # Add specific product context if not already present
        if 'copilot' not in query_lower and 'microsoft 365' not in query_lower:
            enhancement_keywords.append('Microsoft 365 Copilot')
        
        # Add data protection context for relevant queries
        data_protection_terms = ['data', 'security', 'privacy', 'protect', 'compliance', 'governance']
        if any(term in query_lower for term in data_protection_terms):
            if 'enterprise' not in query_lower:
                enhancement_keywords.append('enterprise data protection')
        
        # Add licensing context for cost/pricing queries
        if any(term in query_lower for term in ['cost', 'price', 'license', 'subscription']):
            enhancement_keywords.append('licensing')
        
        # Combine original query with enhancements
        if enhancement_keywords:
            return f"{query} {' '.join(enhancement_keywords)}"
        return query
    
    def _calculate_relevance_score(self, doc: Dict[str, Any], query: str) -> float:
        """
        Calculate relevance score for a document based on multiple factors.
        Higher score = more relevant.
        """
        score = 0.0
        query_lower = query.lower()
        title_lower = doc.get('title', '').lower()
        summary_lower = doc.get('description', '').lower()
        url_lower = doc.get('url', '').lower()
        
        # Priority keywords (highest weight)
        priority_keywords = ['copilot', 'enterprise data protection', 'microsoft 365', 'security', 'compliance']
        for keyword in priority_keywords:
            if keyword in title_lower:
                score += 10
            if keyword in summary_lower:
                score += 5
            if keyword in url_lower:
                score += 3
        
        # Query term matching (medium weight)
        query_terms = [term.strip() for term in query_lower.split() if len(term.strip()) > 3]
        for term in query_terms:
            if term in title_lower:
                score += 7
            if term in summary_lower:
                score += 3
        
        # Prioritize authoritative paths (medium-high weight)
        authoritative_paths = ['/copilot/', '/microsoft-365/', '/purview/', '/security/', '/compliance/']
        for path in authoritative_paths:
            if path in url_lower:
                score += 8
                break
        
        # Boost overview and getting started pages (low-medium weight)
        if any(term in title_lower for term in ['overview', 'introduction', 'getting started', 'what is']):
            score += 4
        
        # Penalize outdated or deprecated content
        if any(term in title_lower or term in summary_lower for term in ['preview', 'deprecated', 'legacy']):
            score -= 5
        
        # Boost administrative and deployment guides for leadership queries
        if any(term in query_lower for term in ['admin', 'deploy', 'implement', 'manage', 'leadership', 'executive']):
            if any(term in title_lower for term in ['admin', 'administrator', 'deployment', 'manage']):
                score += 6
        
        return score
    
    def search_documentation(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Search Microsoft Learn for relevant documentation with enhanced filtering.
        Returns list of documents with title, url, and summary, ranked by relevance.
        """
        try:
            # Enhance query for better precision
            enhanced_query = self._enhance_query(query)
            
            # Microsoft Learn search API endpoint with simplified, supported filters
            search_params = {
                'search': enhanced_query,
                'locale': 'en-us',
                '$top': max_results * 3,  # Fetch more to allow for filtering
                # Simplified filter - only use supported syntax
                'category': 'Documentation'
            }
            
            response = self.session.get(
                self.BASE_SEARCH_URL,
                params=search_params,
                timeout=10
            )
            response.raise_for_status()
            
            results = response.json()
            documents = []
            
            # Process and score results
            for item in results.get('results', []):
                # Get URL and ensure it's properly formatted
                item_url = item.get('url', '')
                # If URL is already absolute, use it as-is; otherwise prepend base URL
                if item_url.startswith('http://') or item_url.startswith('https://'):
                    full_url = item_url
                elif item_url.startswith('/'):
                    full_url = f"{self.BASE_CONTENT_URL}{item_url}"
                else:
                    full_url = f"{self.BASE_CONTENT_URL}/{item_url}"
                
                doc = {
                    'title': item.get('title', 'Untitled'),
                    'url': full_url,
                    'summary': item.get('description', ''),
                    'last_modified': item.get('last_modified', ''),
                    '_raw': item  # Keep raw data for scoring
                }
                
                # Calculate relevance score
                doc['_score'] = self._calculate_relevance_score(doc, query)
                documents.append(doc)
            
            # Sort by relevance score (descending)
            documents.sort(key=lambda x: x['_score'], reverse=True)
            
            # Filter out low-relevance results (score threshold)
            min_score = 10  # Minimum relevance threshold
            documents = [doc for doc in documents if doc['_score'] >= min_score]
            
            # Remove scoring metadata before returning
            for doc in documents:
                doc.pop('_score', None)
                doc.pop('_raw', None)
            
            # Return top results
            return documents[:max_results]
            
        except Exception as e:
            st.warning(f"Microsoft Learn search encountered an issue: {e}")
            # Fallback to basic search if enhanced search fails
            return self._fallback_search(query, max_results)
    
    def _fallback_search(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Fallback search with minimal filters if enhanced search fails.
        """
        try:
            search_params = {
                'search': query,
                'locale': 'en-us',
                '$top': max_results
            }
            
            response = self.session.get(
                self.BASE_SEARCH_URL,
                params=search_params,
                timeout=10
            )
            response.raise_for_status()
            
            results = response.json()
            documents = []
            
            for item in results.get('results', [])[:max_results]:
                # Get URL and ensure it's properly formatted
                item_url = item.get('url', '')
                # If URL is already absolute, use it as-is; otherwise prepend base URL
                if item_url.startswith('http://') or item_url.startswith('https://'):
                    full_url = item_url
                elif item_url.startswith('/'):
                    full_url = f"{self.BASE_CONTENT_URL}{item_url}"
                else:
                    full_url = f"{self.BASE_CONTENT_URL}/{item_url}"
                
                doc = {
                    'title': item.get('title', 'Untitled'),
                    'url': full_url,
                    'summary': item.get('description', ''),
                }
                documents.append(doc)
            
            return documents
            
        except Exception:
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text by removing extra whitespace and normalizing."""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
    
    def _extract_article_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extract structured content from Microsoft Learn article.
        Returns dictionary with headings, paragraphs, lists, and metadata.
        """
        content = {
            'headings': [],
            'paragraphs': [],
            'lists': [],
            'code_blocks': [],
            'tables': [],
            'metadata': {}
        }
        
        # Find the main article content container
        # Microsoft Learn uses specific classes for article content
        article = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if not article:
            return content
        
        # Extract metadata
        meta_title = soup.find('meta', property='og:title')
        if meta_title:
            content['metadata']['title'] = meta_title.get('content', '')
        
        meta_desc = soup.find('meta', property='og:description')
        if meta_desc:
            content['metadata']['description'] = meta_desc.get('content', '')
        
        # Extract headings (h1-h6)
        for heading in article.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = heading.name
            text = self._clean_text(heading.get_text())
            if text:
                content['headings'].append({
                    'level': level,
                    'text': text
                })
        
        # Extract paragraphs
        for para in article.find_all('p'):
            text = self._clean_text(para.get_text())
            if text and len(text) > 20:  # Filter out very short paragraphs
                content['paragraphs'].append(text)
        
        # Extract lists (ul, ol)
        for list_elem in article.find_all(['ul', 'ol']):
            list_items = []
            for li in list_elem.find_all('li', recursive=False):
                text = self._clean_text(li.get_text())
                if text:
                    list_items.append(text)
            if list_items:
                content['lists'].append({
                    'type': 'ordered' if list_elem.name == 'ol' else 'unordered',
                    'items': list_items
                })
        
        # Extract code blocks
        for code in article.find_all('pre'):
            code_text = code.get_text().strip()
            if code_text:
                content['code_blocks'].append(code_text)
        
        # Extract tables
        for table in article.find_all('table'):
            table_data = []
            headers = []
            
            # Extract headers
            header_row = table.find('thead')
            if header_row:
                headers = [self._clean_text(th.get_text()) for th in header_row.find_all('th')]
            
            # Extract rows
            for row in table.find_all('tr'):
                cells = [self._clean_text(td.get_text()) for td in row.find_all(['td', 'th'])]
                if cells:
                    table_data.append(cells)
            
            if table_data:
                content['tables'].append({
                    'headers': headers,
                    'rows': table_data
                })
        
        return content
    
    def _format_extracted_content(self, content: Dict[str, Any]) -> str:
        """Format extracted content into readable text for the model."""
        formatted_parts = []
        
        # Add metadata
        if content['metadata'].get('title'):
            formatted_parts.append(f"# {content['metadata']['title']}\n")
        
        if content['metadata'].get('description'):
            formatted_parts.append(f"**Description:** {content['metadata']['description']}\n")
        
        # Add paragraphs
        if content['paragraphs']:
            formatted_parts.append("\n**Main Content:**\n")
            for para in content['paragraphs'][:15]:  # Limit to first 15 paragraphs
                formatted_parts.append(para)
        
        # Add lists
        for list_item in content['lists'][:5]:  # Limit to first 5 lists
            formatted_parts.append("\n")
            for item in list_item['items']:
                prefix = "- " if list_item['type'] == 'unordered' else "1. "
                formatted_parts.append(f"{prefix}{item}")
        
        # Add important code blocks (limit to first 2)
        if content['code_blocks']:
            formatted_parts.append("\n**Code Examples:**\n")
            for code in content['code_blocks'][:2]:
                formatted_parts.append(f"```\n{code}\n```")
        
        # Add tables (limit to first 2)
        if content['tables']:
            formatted_parts.append("\n**Tables:**\n")
            for table in content['tables'][:2]:
                if table['headers']:
                    formatted_parts.append(" | ".join(table['headers']))
                    formatted_parts.append(" | ".join(['---'] * len(table['headers'])))
                for row in table['rows'][:5]:  # Limit rows
                    formatted_parts.append(" | ".join(row))
                formatted_parts.append("")
        
        return "\n".join(formatted_parts)
    
    def fetch_full_content(self, url: str) -> str:
        """
        Fetch and parse the full content of a documentation page using BeautifulSoup.
        Returns structured, readable text extracted from the HTML.
        Uses cache to avoid redundant requests.
        """
        # Check cache first
        if self.cache_enabled and self.cache:
            cached_content = self.cache.get(url)
            if cached_content:
                return cached_content
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract structured content
            content = self._extract_article_content(soup)
            
            # Format for model consumption
            formatted_content = self._format_extracted_content(content)
            
            if not formatted_content or len(formatted_content) < 100:
                return f"[Content extraction incomplete for: {url}]"
            
            # Store in cache
            if self.cache_enabled and self.cache:
                self.cache.set(url, formatted_content)
            
            return formatted_content
            
        except Exception as e:
            return f"[Content unavailable: {e}]"
    
    def get_contextual_sources(self, query: str, num_sources: int = 3, fetch_full_content: bool = True) -> List[Dict[str, str]]:
        """
        Main method: search for relevant docs and optionally fetch full content.
        Utilizes caching to improve performance for repeated queries.
        Uses enhanced search with relevance scoring and filtering.
        Includes UNC-specific sources when relevant.
        """
        documents = self.search_documentation(query, max_results=num_sources)
        
        # Add UNC/NIH-specific sources if query is UNC-related
        if self._should_include_unc_sources(query):
            unc_sources = self._get_relevant_unc_sources(query)
            if unc_sources:
                # Prepend UNC sources to ensure they're included
                documents = unc_sources + documents
                # Keep total under reasonable limit
                documents = documents[:num_sources + 3]  # Allow extra UNC sources
        
        if not documents:
            st.warning("No highly relevant sources found. Try rephrasing your question or being more specific.")
            return []
        
        if fetch_full_content:
            for doc in documents:
                # Skip web scraping for UNC sources (they already have content)
                if doc.get('_is_unc_source'):
                    doc.pop('_is_unc_source', None)  # Remove flag
                    continue
                
                # Check if content is cached
                cache_status = "💾 (cached)" if self.cache and self.cache.get(doc['url']) else "🌐 (fetching)"
                with st.spinner(f"📄 Extracting content from: {doc['title']} {cache_status}..."):
                    doc['content'] = self.fetch_full_content(doc['url'])
        
        return documents

# ----------------------------
# Prompt caching (system message)
# ----------------------------
SYSTEM_PROMPT = """You are a precise assistant for leadership Q&A about Microsoft Copilot (with Data Protection) for UNC-Chapel Hill.

IMPORTANT CONTEXT:
- UNC-Chapel Hill is part of the University of North Carolina system and uses Microsoft 365 Copilot as an enterprise tool.
- When answering UNC-specific questions, integrate information from both Microsoft documentation AND UNC/NIH-specific sources.
- UNC has its own policies, guidelines, and implementation practices that supplement Microsoft's documentation.

You MUST answer strictly from the SOURCES provided below. If sources are insufficient, reply:
"I can't answer from approved sources."

Use clear bullets and include citations (title + URL) for any claims.
Be accessible to non-technical audiences while maintaining accuracy.

When citing sources, use the format: [Source Title](URL)

For UNC-specific questions, prioritize combining:
1. Microsoft's technical documentation on Copilot features and data protection
2. UNC's institutional policies and guidelines
3. NIH guidance when relevant to research contexts
"""

# ----------------------------
# UI Layout
# ----------------------------
st.title("🤖 Microsoft Copilot Chat: A Q&A Tool")
st.subheader("Built By Ali Sora — NC TraCS Recruitment & Retention Program.")
st.caption("Powered by GPT‑4o mini + Microsoft Learn Full Content Retrieval")

with st.expander("How this works"):
    st.markdown("""
- Uses **GPT‑4o mini** via OpenAI Responses API.
- **Intelligently searches** Microsoft Learn with enhanced relevance scoring and filtering.
- **Automatically includes UNC-specific sources** when queries reference UNC-Chapel Hill or NIH contexts.
- **Automatically retrieves** and **fully parses** documentation using BeautifulSoup.
- **Prioritizes authoritative sources**: Official Microsoft documentation, UNC institutional policies, NIH guidance, and high-relevance matches.
- Extracts **complete article content** including headings, paragraphs, lists, code blocks, and tables.
- **Smart caching**: Stores retrieved content for faster repeat queries.
- Enforces **approved sources only**: answers strictly from fetched Microsoft, UNC, and NIH documentation.
- Includes **citations** with links to original sources for further exploration.
- No technical expertise required — just ask your question naturally.
    """)

# Sidebar settings
st.sidebar.header("⚙️ Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
max_tokens = st.sidebar.slider("Max tokens", 64, 4096, 1500, 64)
num_sources = st.sidebar.slider("Number of sources to retrieve", 1, 5, 3, 1)
auto_mode = st.sidebar.checkbox("Automatic source retrieval", value=True, help="Fetch sources from Microsoft Learn automatically with enhanced relevance filtering")
full_content = st.sidebar.checkbox("Extract full article content", value=True, help="Use BeautifulSoup to parse complete articles (recommended)")

# Cache settings
st.sidebar.subheader("🗄️ Cache Settings")
cache_enabled = st.sidebar.checkbox("Enable caching", value=True, help="Cache retrieved documents to improve performance")
cache_ttl = st.sidebar.slider("Cache TTL (hours)", 1, 168, 24, 1, help="How long to keep cached documents")

# Display cache stats if enabled
if cache_enabled:
    try:
        temp_cache = DocumentCache(ttl_hours=cache_ttl)
        stats = temp_cache.get_stats()
        st.sidebar.caption(f"📊 Cache: {stats['entries']} entries, {stats['total_size_kb']:.1f} KB")
        if st.sidebar.button("🗑️ Clear Cache"):
            import shutil
            if Path(".doc_cache").exists():
                shutil.rmtree(".doc_cache")
                st.sidebar.success("Cache cleared!")
                st.rerun()
    except Exception:
        pass

# Main input
st.subheader("🧠 Ask your question")
question = st.text_area(
    "Question", 
    placeholder="For example: What is enterprise data protection in Microsoft 365 Copilot? Or: How does Copilot protect UNC's data?",
    height=100
)

# Initialize sources_text with a default value
sources_text = ""

# Optional manual sources (only shown if auto mode is off)
if not auto_mode:
    st.subheader("📚 Manual sources")
    sources_text = st.text_area(
        "Sources (one per line)", 
        value="Enterprise data protection — https://learn.microsoft.com/en-us/copilot/microsoft-365/enterprise-data-protection",
        help="Provide sources manually if automatic retrieval is disabled"
    )

submit = st.button("🚀 Generate Answer", type="primary")

# ----------------------------
# Handle submission
# ----------------------------

def format_sources_for_prompt(sources: List[Dict[str, str]]) -> str:
    """Format retrieved sources for inclusion in the prompt."""
    formatted = []
    for i, src in enumerate(sources, start=1):
        formatted.append(f"\n{'='*60}")
        formatted.append(f"SOURCE [{i}]: {src['title']}")
        formatted.append(f"URL: {src['url']}")
        formatted.append(f"{'='*60}\n")
        
        if 'content' in src and src['content']:
            formatted.append(f"{src['content']}")
        elif src['summary']:
            formatted.append(f"Summary: {src['summary']}")
        
        formatted.append("")
    return "\n".join(formatted)

if submit:
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()
    
    sources = []
    
    # Retrieve sources automatically or use manual input
    if auto_mode:
        with st.spinner("🔍 Searching Microsoft Learn for relevant documentation..."):
            mcp = MicrosoftLearnMCP(cache_enabled=cache_enabled, cache_ttl_hours=cache_ttl)
            sources = mcp.get_contextual_sources(
                query=question, 
                num_sources=num_sources,
                fetch_full_content=full_content
            )
            
            if not sources:
                st.error("Could not retrieve relevant sources. Please try rephrasing your question or disable automatic mode.")
                st.stop()
            
            # Display retrieved sources
            with st.expander("📚 Retrieved Sources", expanded=False):
                for i, src in enumerate(sources, start=1):
                    # Highlight UNC/NIH sources
                    is_unc_source = any(src['url'] == unc_src['url'] for unc_src in MicrosoftLearnMCP.UNC_ENTERPRISE_SOURCES)
                    emoji = "🏛️" if is_unc_source else "📖"
                    
                    st.markdown(f"{emoji} **{i}. {src['title']}**")
                    st.markdown(f"🔗 [{src['url']}]({src['url']})")
                    if src.get('summary'):
                        st.caption(src['summary'])
                    if src.get('content'):
                        content_preview = src['content'][:300] + "..." if len(src['content']) > 300 else src['content']
                        st.code(content_preview, language=None)
                        st.caption(f"✅ Full content extracted ({len(src['content'])} characters)")
                    st.divider()
    else:
        # Parse manual sources
        raw_sources = [line.strip() for line in sources_text.splitlines() if line.strip()]
        if not raw_sources:
            st.warning("No sources provided — refusing to answer.")
            st.stop()
        
        sources = [{'title': s, 'url': s, 'summary': '', 'content': ''} for s in raw_sources]
    
    # Build combined prompt
    sources_block = format_sources_for_prompt(sources)
    user_prompt = f"[SOURCES]\n{sources_block}\n\n[USER QUESTION]\n{question}"

    with st.spinner("🤖 Generating answer from extracted content..."):
        try:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            answer = response.output_text
        except Exception as e:
            st.error(f"API call failed: {e}")
            st.stop()

    # Display result
    st.success("✅ Answer generated from full article content")
    st.markdown("### Answer")
    st.markdown(answer)
    
    # Create downloadable content with sources
    download_content = f"# Question\n\n{question}\n\n# Answer\n\n{answer}\n\n# Sources\n\n"
    for i, src in enumerate(sources, start=1):
        download_content += f"{i}. {src['title']}\n   {src['url']}\n"
        if src.get('content'):
            download_content += f"   ✅ Full content extracted\n"
        download_content += "\n"

    st.download_button(
        "⬇️ Download Answer with Sources", 
        download_content, 
        file_name="copilot_answer.md", 
        mime="text/markdown"
    )

st.markdown("---")
st.caption("Automatically retrieves and fully parses Microsoft Learn documentation using BeautifulSoup for comprehensive content extraction. Enhanced with intelligent search filtering, relevance scoring, and UNC-Chapel Hill/NIH enterprise context for optimal results.")
