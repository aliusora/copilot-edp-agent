"""Configuration and constants for the application."""

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

# UNC-specific and NIH-related authoritative sources
UNC_ENTERPRISE_SOURCES = [
    {
        'title': 'UNC ITS - Microsoft 365 Copilot for UNC',
        'url': 'https://its.unc.edu/ai/copilot/',
        'context': 'unc copilot enterprise deployment university',
        'summary': 'UNC Information Technology Services official guidance on Microsoft 365 Copilot deployment, access, and enterprise data protection for UNC-Chapel Hill users.'
    },
    {
        'title': 'UNC Graduate Handbook - Generative AI Policy',
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

# Default settings
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 1500
DEFAULT_NUM_SOURCES = 3
DEFAULT_CACHE_TTL_HOURS = 24