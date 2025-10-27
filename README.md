# 🤖 Microsoft Copilot Chat: UNC Q&A Tool

An intelligent Q&A chatbot for UNC-Chapel Hill leadership and faculty to get answers about Microsoft 365 Copilot, enterprise data protection, and institutional AI policies. Built with Streamlit and powered by GPT-4o mini with automated Microsoft Learn content retrieval.

## ✨ Features

- **🔍 Intelligent Search**: Automatically retrieves and parses relevant Microsoft Learn documentation
- **🏛️ UNC Context Integration**: Includes UNC-Chapel Hill and NIH-specific policies and guidelines
- **📚 Full Content Extraction**: Uses BeautifulSoup to parse complete articles with headings, lists, tables, and code blocks
- **💾 Smart Caching**: Stores retrieved content for faster repeat queries (configurable TTL)
- **🎯 Relevance Scoring**: Multi-factor algorithm prioritizes authoritative, recent, and high-quality sources
- **📖 Citation Support**: All responses include proper citations with clickable links to original sources
- **🔒 Source-Only Answers**: Strictly answers from approved Microsoft, UNC, and NIH documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key with access to GPT-4o mini

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aliusora/copilot-edp-agent.git
   cd copilot-edp-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**
   
   Create a `.streamlit/secrets.toml` file:
   ```toml
   OPENAI_API_KEY = "sk-your-api-key-here"
   ```
   
   Or set as environment variable:
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"  # On Windows: set OPENAI_API_KEY=sk-...
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Ask a question** in natural language (e.g., "How does Copilot protect UNC's data?")
2. **Automatic retrieval**: The app searches Microsoft Learn and UNC/NIH sources
3. **Review sources**: Expand the "Retrieved Sources" section to see what was found
4. **Get answer**: GPT-4o mini generates a response based only on the retrieved content
5. **Download**: Save the answer with sources as a Markdown file

### Example Questions

- "What is enterprise data protection in Microsoft 365 Copilot?"
- "How does UNC implement Copilot for research purposes?"
- "What are NIH guidelines for using AI in grant applications?"
- "How much does Microsoft 365 Copilot cost?"

## ⚙️ Configuration

### Sidebar Settings

- **Temperature** (0.0-1.0): Controls response randomness (lower = more deterministic)
- **Max tokens** (64-4096): Maximum length of generated responses
- **Number of sources** (1-5): How many documents to retrieve per query
- **Extract full content**: Toggle BeautifulSoup parsing (recommended: ON)
- **Enable caching**: Store retrieved content for faster repeat queries
- **Cache TTL**: How long to keep cached documents (1-168 hours)

## 🏗️ Architecture

```
app.py
├── DocumentCache: File-based cache with TTL support
├── MicrosoftLearnMCP: Content retrieval and parsing
│   ├── Search Microsoft Learn API
│   ├── UNC/NIH source detection and integration
│   ├── Relevance scoring algorithm
│   ├── BeautifulSoup content extraction
│   └── Intelligent caching
└── Streamlit UI: Interactive chat interface
```

### UNC Enterprise Sources

The app automatically includes UNC-specific sources when queries mention:
- UNC, University of North Carolina, or Chapel Hill
- NIH, grants, research, or federal funding

**Integrated Sources:**
- UNC ITS - Microsoft 365 Copilot Guidance
- UNC Employee Handbook - Generative AI Policy
- UNC AI Initiative - Research & AI Usage Guidance
- UNC School of Medicine - AI Tools Best Practices
- UNC Policies - Generative AI in Teaching and Research
- NIH - AI Use in Research Applications Policy
- NIH Notice - Generative AI in Grant Applications

## 📁 Project Structure

```
copilot-edp-agent/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
├── .gitignore            # Git ignore rules
├── .streamlit/           # Streamlit configuration
│   └── secrets.toml      # API keys (not committed)
└── .doc_cache/           # Document cache (auto-created, ignored)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Ali Sora**  
NC TraCS Recruitment & Retention Program  
UNC-Chapel Hill

## 🙏 Acknowledgments

- Microsoft Learn for comprehensive Copilot documentation
- UNC ITS for institutional AI guidance
- NIH for research policy framework
- OpenAI for GPT-4o mini API

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Contact NC TraCS Recruitment & Retention Program

---

**Note**: This tool provides information from approved sources only. Always verify critical decisions with official UNC IT Services and relevant institutional policies.
