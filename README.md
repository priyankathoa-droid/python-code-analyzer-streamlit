# 🐍 Python Code Analyzer

A comprehensive Streamlit-based tool to analyze Python projects for LLM usage, frameworks, environment variables, and architecture patterns.

## Features

- **🤖 LLM Detection**: Identifies OpenAI, Anthropic, LangChain, Hugging Face, Gemini, Cohere, Groq, and more
- **🔧 Framework Analysis**: Detects FastAPI, Flask, Django, Streamlit, PyTorch, TensorFlow, and other popular frameworks
- **⚠️ Security Scanning**: Finds hardcoded credentials and suggests proper environment variable usage
- **🏗️ Architecture Patterns**: Identifies REST APIs, async patterns, OOP, service layers, and type hints
- **✅ Best Practices**: Checks for proper dependency management and coding standards
- **💡 Recommendations**: Provides actionable suggestions for improvement

## Installation

```bash
# Clone the repository
git clone https://github.com/priyankathoa-droid/python-code-analyzer-streamlit.git
cd python-code-analyzer-streamlit

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Usage

1. **Upload your Python project**:
   - Option 1: Upload a ZIP file containing your entire project
   - Option 2: Upload individual Python files

2. **Click "Analyze Code"** to get comprehensive analysis

3. **Review the results**:
   - Project overview metrics
   - LLM and AI libraries detected
   - Frameworks and libraries used
   - Environment variable security analysis
   - Architecture patterns identified
   - Best practices evaluation
   - Actionable recommendations

## Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select this repository
6. Set main file path to `app.py`
7. Click "Deploy"

## Supported File Types

- `.py` - Python source files
- `requirements.txt` - Dependency files
- `.env` - Environment configuration
- `pyproject.toml` - Project configuration
- `.cfg`, `.ini` - Configuration files

## Analysis Categories

### LLM Libraries
- OpenAI, Anthropic (Claude), LangChain, Hugging Face
- Google AI (Gemini), Cohere, LlamaIndex
- Replicate, Together AI, Groq, Ollama, Mistral AI

### Frameworks
- Web: FastAPI, Flask, Django
- UI: Streamlit, Gradio
- ML: PyTorch, TensorFlow
- Data: NumPy, Pandas
- Database: SQLAlchemy, Redis, MongoDB

### Architecture Patterns
- REST API
- Async/Await Pattern
- Object-Oriented Programming
- Service Layer Pattern
- Pydantic Models
- Type Hints

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

---

Built with ❤️ using Streamlit