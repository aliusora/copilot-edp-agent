"""Streamlit UI for using GPT-4o via the OpenAI Response API with automated Microsoft Learn content retrieval."""

import os
import shutil
import streamlit as st
from openai import OpenAI
from typing import List, Dict
from pathlib import Path

from config import SYSTEM_PROMPT, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, DEFAULT_NUM_SOURCES, DEFAULT_CACHE_TTL_HOURS, UNC_ENTERPRISE_SOURCES
from cache import DocumentCache
from mcp import MicrosoftLearnMCP

# ----------------------------
# Configuration & Setup
# ----------------------------

def _load_openai_api_key() -> str | None:
    """Load OpenAI API key from environment or Streamlit secrets."""
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
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
# Helper Functions
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

# ----------------------------
# UI Layout
# ----------------------------

st.title("🤖 Microsoft Copilot for Research Recruitment: A Q&A Tool")
st.subheader("Built By Ali Sora")
st.caption("Powered by GPT‑4o mini + Microsoft Learn Model Context Protocol + Vetted UNC/NIH Sources")

with st.expander("How this works"):
    st.markdown("""
- Uses **GPT-4o mini** AI to answer your questions.
- **Searches Microsoft's official documentation** and finds the most relevant and up-to-date information.
- **Includes UNC-Chapel Hill and NIH sources** when your question is about university or research policies.
- **Downloads and reads entire web pages** to get complete information, not just summaries.
- **Prioritizes trusted sources**: Microsoft's official guides, UNC policies, NIH requirements, and other reliable documentation.
- Pulls out **all the important content** from articles including main text, bullet points, examples, and tables.
- **Saves information temporarily** so repeat questions load faster.
- **Only uses approved sources**: answers come strictly from official Microsoft, UNC, and NIH documentation.
- **Shows you where information comes from** with links so you can read more if needed.
- Easy to use — just type your question in everyday language.
    """)

# Sidebar settings
st.sidebar.header("⚙️ Danger Zone")
st.sidebar.subheader("Do not modify any of the parameters below unless you know what you're doing!")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, DEFAULT_TEMPERATURE, 0.05)
max_tokens = st.sidebar.slider("Max tokens", 64, 4096, DEFAULT_MAX_TOKENS, 64)
num_sources = st.sidebar.slider("Number of sources to retrieve", 1, 5, DEFAULT_NUM_SOURCES, 1)
auto_mode = st.sidebar.checkbox("Automatic source retrieval", value=True, help="Fetch sources from Microsoft Learn automatically with enhanced relevance filtering")
full_content = st.sidebar.checkbox("Extract full article content", value=True, help="Use BeautifulSoup to parse complete articles (recommended)")

# Cache settings
st.sidebar.subheader("🗄️ Cache Settings")
cache_enabled = st.sidebar.checkbox("Enable caching", value=True, help="Cache retrieved documents to improve performance")
cache_ttl = st.sidebar.slider("Cache TTL (hours)", 1, 168, DEFAULT_CACHE_TTL_HOURS, 1, help="How long to keep cached documents")

# Display cache stats if enabled
if cache_enabled:
    try:
        temp_cache = DocumentCache(ttl_hours=cache_ttl)
        stats = temp_cache.get_stats()
        st.sidebar.caption(f"📊 Cache: {stats['entries']} entries, {stats['total_size_kb']:.1f} KB")
        if st.sidebar.button("🗑️ Clear Cache"):
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
    placeholder="For example: How does Copilot protect UNC's data?",
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
                    is_unc_source = any(src['url'] == unc_src['url'] for unc_src in UNC_ENTERPRISE_SOURCES)
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
st.caption("This tool automatically finds and reads complete Microsoft documentation using Microsoft's new Learn Model Context Protocol. It includes special features for UNC-Chapel Hill and NIH users, with improved search and ranking to give you the best results.")