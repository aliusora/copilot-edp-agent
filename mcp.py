"""Microsoft Learn content provider with full article extraction."""

import re
import requests
import streamlit as st
from typing import List, Dict, Any
from bs4 import BeautifulSoup

from cache import DocumentCache
from config import UNC_ENTERPRISE_SOURCES


class MicrosoftLearnMCP:
    """Fetches relevant documentation from Microsoft Learn with full article extraction."""
    
    BASE_SEARCH_URL = "https://learn.microsoft.com/api/search"
    BASE_CONTENT_URL = "https://learn.microsoft.com"
    
    def __init__(self, cache_enabled: bool = True, cache_ttl_hours: int = 24):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html'
        })
        self.cache_enabled = cache_enabled
        self.cache = DocumentCache(ttl_hours=cache_ttl_hours) if cache_enabled else None
        
        if self.cache:
            self.cache.clear_expired()
    
    def _should_include_unc_sources(self, query: str) -> bool:
        """Determine if UNC/NIH-specific sources should be included based on query content."""
        query_lower = query.lower()
        
        unc_keywords = ['unc', 'university of north carolina', 'chapel hill', 'carolina', 'university']
        nih_keywords = ['nih', 'grant', 'research', 'federal', 'funding', 'application']
        
        has_unc = any(keyword in query_lower for keyword in unc_keywords)
        has_nih = any(keyword in query_lower for keyword in nih_keywords)
        
        return has_unc or has_nih
    
    def _get_relevant_unc_sources(self, query: str) -> List[Dict[str, str]]:
        """Get UNC/NIH sources relevant to the query based on context matching."""
        query_lower = query.lower()
        relevant_sources = []
        
        for source in UNC_ENTERPRISE_SOURCES:
            context_lower = source['context'].lower()
            query_terms = query_lower.split()
            
            matches = sum(1 for term in query_terms if len(term) > 3 and term in context_lower)
            
            if matches > 0 or ('copilot' in query_lower and 'unc' in context_lower):
                relevant_sources.append({
                    'title': source['title'],
                    'url': source['url'],
                    'summary': source['summary'],
                    'content': source['summary'],
                    '_matches': matches,
                    '_is_unc_source': True
                })
        
        relevant_sources.sort(key=lambda x: x.get('_matches', 0), reverse=True)
        
        for src in relevant_sources:
            src.pop('_matches', None)
        
        return relevant_sources[:5]
    
    def _enhance_query(self, query: str) -> str:
        """Enhance user query with relevant keywords for better search precision."""
        enhancement_keywords = []
        query_lower = query.lower()
        
        if 'copilot' not in query_lower and 'microsoft 365' not in query_lower:
            enhancement_keywords.append('Microsoft 365 Copilot')
        
        data_protection_terms = ['data', 'security', 'privacy', 'protect', 'compliance', 'governance']
        if any(term in query_lower for term in data_protection_terms):
            if 'enterprise' not in query_lower:
                enhancement_keywords.append('enterprise data protection')
        
        if any(term in query_lower for term in ['cost', 'price', 'license', 'subscription']):
            enhancement_keywords.append('licensing')
        
        if enhancement_keywords:
            return f"{query} {' '.join(enhancement_keywords)}"
        return query
    
    def _calculate_relevance_score(self, doc: Dict[str, Any], query: str) -> float:
        """Calculate relevance score for a document based on multiple factors."""
        score = 0.0
        query_lower = query.lower()
        title_lower = doc.get('title', '').lower()
        summary_lower = doc.get('description', '').lower()
        url_lower = doc.get('url', '').lower()
        
        priority_keywords = ['copilot', 'enterprise data protection', 'microsoft 365', 'security', 'compliance']
        for keyword in priority_keywords:
            if keyword in title_lower:
                score += 10
            if keyword in summary_lower:
                score += 5
            if keyword in url_lower:
                score += 3
        
        query_terms = [term.strip() for term in query_lower.split() if len(term.strip()) > 3]
        for term in query_terms:
            if term in title_lower:
                score += 7
            if term in summary_lower:
                score += 3

        authoritative_paths = ['/copilot/', '/microsoft-365/', '/microsoft-copilot/', '/microsoft-copilot-service/', '/purview/', '/security/', '/compliance/']
        for path in authoritative_paths:
            if path in url_lower:
                score += 8
                break
        
        if any(term in title_lower for term in ['overview', 'introduction', 'getting started', 'what is']):
            score += 4
        
        if any(term in title_lower or term in summary_lower for term in ['preview', 'deprecated', 'legacy']):
            score -= 5
        
        if any(term in query_lower for term in ['admin', 'deploy', 'implement', 'manage', 'leadership', 'executive']):
            if any(term in title_lower for term in ['admin', 'administrator', 'deployment', 'manage']):
                score += 6
        
        return score
    
    def search_documentation(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """Search Microsoft Learn for relevant documentation with enhanced filtering."""
        try:
            enhanced_query = self._enhance_query(query)
            
            search_params = {
                'search': enhanced_query,
                'locale': 'en-us',
                '$top': max_results * 3,
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
            
            for item in results.get('results', []):
                item_url = item.get('url', '')
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
                    '_raw': item
                }
                
                doc['_score'] = self._calculate_relevance_score(doc, query)
                documents.append(doc)
            
            documents.sort(key=lambda x: x['_score'], reverse=True)
            
            min_score = 10
            documents = [doc for doc in documents if doc['_score'] >= min_score]
            
            for doc in documents:
                doc.pop('_score', None)
                doc.pop('_raw', None)
            
            return documents[:max_results]
            
        except Exception as e:
            st.warning(f"Microsoft Learn search encountered an issue: {e}")
            return self._fallback_search(query, max_results)
    
    def _fallback_search(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """Fallback search with minimal filters if enhanced search fails."""
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
                item_url = item.get('url', '')
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
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
    
    def _extract_article_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract structured content from Microsoft Learn article."""
        content = {
            'headings': [],
            'paragraphs': [],
            'lists': [],
            'code_blocks': [],
            'tables': [],
            'metadata': {}
        }
        
        article = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if not article:
            return content
        
        meta_title = soup.find('meta', property='og:title')
        if meta_title:
            content['metadata']['title'] = meta_title.get('content', '')
        
        meta_desc = soup.find('meta', property='og:description')
        if meta_desc:
            content['metadata']['description'] = meta_desc.get('content', '')
        
        for heading in article.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            level = heading.name
            text = self._clean_text(heading.get_text())
            if text:
                content['headings'].append({
                    'level': level,
                    'text': text
                })
        
        for para in article.find_all('p'):
            text = self._clean_text(para.get_text())
            if text and len(text) > 20:
                content['paragraphs'].append(text)
        
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
        
        for code in article.find_all('pre'):
            code_text = code.get_text().strip()
            if code_text:
                content['code_blocks'].append(code_text)
        
        for table in article.find_all('table'):
            table_data = []
            headers = []
            
            header_row = table.find('thead')
            if header_row:
                headers = [self._clean_text(th.get_text()) for th in header_row.find_all('th')]
            
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
        
        if content['metadata'].get('title'):
            formatted_parts.append(f"# {content['metadata']['title']}\n")
        
        if content['metadata'].get('description'):
            formatted_parts.append(f"**Description:** {content['metadata']['description']}\n")
        
        if content['paragraphs']:
            formatted_parts.append("\n**Main Content:**\n")
            for para in content['paragraphs'][:15]:
                formatted_parts.append(para)
        
        for list_item in content['lists'][:5]:
            formatted_parts.append("\n")
            for item in list_item['items']:
                prefix = "- " if list_item['type'] == 'unordered' else "1. "
                formatted_parts.append(f"{prefix}{item}")
        
        if content['code_blocks']:
            formatted_parts.append("\n**Code Examples:**\n")
            for code in content['code_blocks'][:2]:
                formatted_parts.append(f"```\n{code}\n```")
        
        if content['tables']:
            formatted_parts.append("\n**Tables:**\n")
            for table in content['tables'][:2]:
                if table['headers']:
                    formatted_parts.append(" | ".join(table['headers']))
                    formatted_parts.append(" | ".join(['---'] * len(table['headers'])))
                for row in table['rows'][:5]:
                    formatted_parts.append(" | ".join(row))
                formatted_parts.append("")
        
        return "\n".join(formatted_parts)
    
    def fetch_full_content(self, url: str) -> str:
        """Fetch and parse the full content of a documentation page using BeautifulSoup."""
        if self.cache_enabled and self.cache:
            cached_content = self.cache.get(url)
            if cached_content:
                return cached_content
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            content = self._extract_article_content(soup)
            formatted_content = self._format_extracted_content(content)
            
            if not formatted_content or len(formatted_content) < 100:
                return f"[Content extraction incomplete for: {url}]"
            
            if self.cache_enabled and self.cache:
                self.cache.set(url, formatted_content)
            
            return formatted_content
            
        except Exception as e:
            return f"[Content unavailable: {e}]"
    
    def get_contextual_sources(self, query: str, num_sources: int = 3, fetch_full_content: bool = True) -> List[Dict[str, str]]:
        """Main method: search for relevant docs and optionally fetch full content."""
        documents = self.search_documentation(query, max_results=num_sources)
        
        if self._should_include_unc_sources(query):
            unc_sources = self._get_relevant_unc_sources(query)
            if unc_sources:
                documents = unc_sources + documents
                documents = documents[:num_sources + 5]
        
        if not documents:
            st.warning("No highly relevant sources found. Try rephrasing your question or being more specific.")
            return []
        
        if fetch_full_content:
            for doc in documents:
                if doc.get('_is_unc_source'):
                    doc.pop('_is_unc_source', None)
                    continue
                
                cache_status = "💾 (cached)" if self.cache and self.cache.get(doc['url']) else "🌐 (fetching)"
                with st.spinner(f"📄 Extracting content from: {doc['title']} {cache_status}..."):
                    doc['content'] = self.fetch_full_content(doc['url'])
        
        return documents