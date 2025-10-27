# Microsoft Copilot Chat: A Question-and-Answer Tool for UNC-Chapel Hill

**Developed by Staff at the NC TraCS Recruitment and Retention Program**

An intelligent question-and-answer application designed for UNC-Chapel Hill leadership, faculty, staff, and researchers/study teams. This tool provides accurate, source-based answers about Microsoft 365 Copilot, enterprise data protection, and institutional AI policies by automatically retrieving and analyzing official documentation from Microsoft, UNC-Chapel Hill, and the National Institutes of Health (NIH).

---

## Table of Contents

- [For Users: Understanding and Using This Tool](#for-users-understanding-and-using-this-tool)
  - [Overview](#overview)
  - [How This Tool Differs from General AI](#how-this-tool-differs-from-general-ai)
  - [Key Features](#key-features)
  - [How to Use This Tool](#how-to-use-this-tool)
  - [Configuration Options](#configuration-options)
  - [Institutional Sources](#institutional-sources)
- [For Builders and Developers](#for-builders-and-developers)
  - [Getting Started](#getting-started)
  - [Technical Architecture](#technical-architecture)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
- [Project Information](#project-information)
- [License](#license)

---

## For Users: Understanding and Using This Tool

### Overview

This application addresses the challenge of consolidating reliable, current information about Microsoft 365 Copilot and related institutional policies. Rather than relying on general knowledge or manually searching for information, the tool searches official documentation for you in real-time and provides answers strictly based on authoritative sources.

### How This Tool Differs from General AI

Unlike ChatGPT, Google, or other general-purpose AI assistants that generate responses from pre-trained knowledge that may be generic or outdated, this tool actively retrieves live documentation from Microsoft's official technical library and select UNC-Chapel Hill institutional resources. Every answer is grounded in current, verified sources—not approximated from memory or training data that could be months or years old.

**Key Distinctions:**
- **Real-Time Retrieval**: Searches current documentation at the moment of your query, not months-old training data
- **Authoritative Sources Only**: Pulls exclusively from Microsoft Learn, UNC policies, and NIH guidelines
- **Institutional Context**: Automatically incorporates UNC-Chapel Hill and NIH-specific policies when relevant
- **Complete Transparency**: Every answer includes citations with direct links to source materials
- **Verified Accuracy**: Responses are based solely on official documentation, eliminating AI hallucination or speculation

### Key Features

- **Automated Documentation Retrieval**: Searches [Microsoft Learn's official documentation library](https://learn.microsoft.com/en-us/) and retrieves the most relevant, up-to-date articles
- **Institutional Context Integration**: Automatically includes select UNC-Chapel Hill policies and NIH guidelines when queries relate to university or research contexts
- **Complete Content Analysis**: Extracts full article content including headings, paragraphs, lists, tables, and examples—not just summaries
- **Performance Optimization**: Stores retrieved documentation temporarily to provide faster responses for repeated queries
- **Intelligent Source Ranking**: Prioritizes authoritative, current documentation over outdated or less relevant materials
- **Transparent Citations**: All responses include proper citations with direct links to original sources for verification
- **Source-Based Answers Only**: Generates responses exclusively from retrieved documentation, ensuring accuracy and compliance

### How to Use This Tool

#### Basic Workflow

1. **Enter Your Question**: Type your question in plain language in the text box (e.g., "How does Microsoft 365 Copilot protect institutional data?")
2. **Automatic Search**: The application searches Microsoft Learn documentation and relevant UNC/NIH resources
3. **Review Sources**: Expand the "Retrieved Sources" section to see which documents were found and analyzed
4. **Read the Answer**: The application generates a response based exclusively on the retrieved documentation
5. **Download Results**: Save your answer along with source citations as a downloadable file for future reference

#### Example Questions

- "What is enterprise data protection in Microsoft 365 Copilot?"
- "How does UNC-Chapel Hill implement Copilot for research purposes?"
- "What are NIH guidelines for using AI tools in grant applications?"
- "What are the licensing costs for Microsoft 365 Copilot?"
- "How does Copilot handle sensitive patient data in healthcare settings?"

### Configuration Options

#### Adjustable Settings

The application includes several configurable parameters accessible through the sidebar interface:

- **Temperature** (Range: 0.0-1.0): Controls response variability. Lower values produce more consistent, deterministic answers; higher values allow more creative variation.
- **Maximum Tokens** (Range: 64-4096): Sets the maximum length of generated responses. Higher values allow for more detailed answers.
- **Number of Sources** (Range: 1-5): Determines how many documentation articles to retrieve and analyze per query.
- **Full Content Extraction**: When enabled, the application downloads and parses complete articles rather than relying on summaries.
- **Caching**: Stores retrieved documentation temporarily to improve performance for repeated or similar queries.
- **Cache Duration** (Range: 1-168 hours): Determines how long retrieved documents remain stored before being refreshed.

**Note for General Users**: Default settings are optimized for most use cases. Modification is only recommended for users familiar with language model parameters.

### Institutional Sources

#### What Sources Are Included?

The application automatically includes UNC-Chapel Hill and NIH-specific sources when queries contain keywords related to:
- UNC-Chapel Hill, University of North Carolina, or Carolina
- NIH, grants, research, or federal funding

#### Integrated Authoritative Sources

- **UNC Information Technology Services** - Microsoft 365 Copilot Guidance
- **UNC Employee Handbook** - Generative AI Policy
- **UNC AI Initiative** - Research and Generative AI Usage Guidance
- **UNC School of Medicine** - Safe Uses and Best Practices of AI Tools
- **UNC Policies** - Generative AI in Teaching and Research
- **NIH** - Policy on AI Use in Research Applications
- **NIH Notice** - Use of Generative AI Technologies in Grant Applications

---

## For Builders and Developers

### Getting Started

##### System Requirements

- Python 3.10 or higher
- OpenAI API key with access to GPT-4o mini model
- Internet connection for retrieving documentation

#### Installation Instructions

**Step 1: Download the Application**
   ```bash
   git clone https://github.com/aliusora/copilot-edp-agent.git
   cd copilot-edp-agent
   ```

**Step 2: Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

**Step 3: Install Required Software**
   ```bash
   pip install -r requirements.txt
   ```

**Step 4: Configure OpenAI API Key**
   
   Create a `.streamlit/secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```
   
   Or set as environment variable:
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"  # On Windows: set OPENAI_API_KEY=sk-...
   ```

**Step 5: Launch the Application**
   ```bash
   streamlit run app.py
   ```

The application will open in your web browser at `http://localhost:8501`

### Technical Architecture

#### System Components

The application consists of three primary components:

1. **Document Cache**: A file-based storage system that temporarily saves retrieved documentation to improve performance and reduce redundant searches.

2. **Microsoft Learn Content Provider**: The core retrieval engine that:
   - Searches Microsoft Learn's official API for relevant documentation
   - Detects when queries relate to UNC-Chapel Hill or NIH contexts and includes institutional sources
   - Ranks results using a multi-factor relevance algorithm
   - Extracts complete article content including structured elements (headings, lists, tables, code examples)
   - Manages the document cache for optimal performance

3. **User Interface**: An interactive web-based interface built with Streamlit that allows users to submit questions, review retrieved sources, and access generated answers.

### Project Structure

```
copilot-edp-agent/
├── app.py                 # Main application code
├── requirements.txt       # Required software dependencies
├── README.md             # Documentation (this file)
├── DEPLOYMENT.md         # Deployment instructions for various platforms
├── LICENSE               # MIT License
├── .gitignore            # Files excluded from version control
├── .streamlit/           # Application configuration
│   └── secrets.toml      # API keys (not included in version control)
└── .doc_cache/           # Temporary document storage (auto-created)
```

### Contributing

Contributions to this project are welcome. To contribute:

1. Fork the repository on GitHub
2. Create a feature branch (`git checkout -b feature/YourFeatureName`)
3. Commit your changes with descriptive messages (`git commit -m 'Add detailed explanation of feature'`)
4. Push your branch to GitHub (`git push origin feature/YourFeatureName`)
5. Submit a Pull Request for review

---

## Project Information

**Developer**: Ali Sora | ali.sora@unc.edu
**Affiliation**: NC TraCS Recruitment and Retention Program  
**Institution**: University of North Carolina at Chapel Hill

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete details.

## Acknowledgments

This project builds upon documentation and resources provided by:
- Microsoft Learn for comprehensive Microsoft 365 Copilot documentation
- UNC Information Technology Services for institutional AI guidance and policies
- National Institutes of Health for research funding and AI usage policy frameworks
- OpenAI for access to the GPT-4o mini language model API

## Support and Contact

For technical issues, questions, or feedback:
- Submit an issue through the GitHub repository issue tracker
- Contact the NC TraCS Recruitment and Retention Program

## Important Notice

This tool provides information synthesized from approved institutional and vendor sources. Users should verify critical decisions with official UNC Information Technology Services representatives and consult relevant institutional policies before making final determinations regarding data protection, compliance, or policy matters.
