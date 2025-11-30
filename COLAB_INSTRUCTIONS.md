# 🚀 Run in Google Colab

## Method 1: One-Line Command (Easiest)

Open Google Colab and run this single command:

```python
!wget -q https://raw.githubusercontent.com/priyankathoa-droid/python-code-analyzer-streamlit/main/colab_setup.py && python colab_setup.py
```

That's it! The script will:
- ✅ Install all dependencies
- ✅ Create the Streamlit app
- ✅ Start the server
- ✅ Generate a public URL

Click the URL to access your analyzer!

---

## Method 2: Step-by-Step

### Step 1: Open Google Colab
Go to: https://colab.research.google.com/

### Step 2: Create a new notebook

### Step 3: Copy and paste this code in a cell:

```python
# Install packages
!pip install -q streamlit pyngrok

# Download the setup script
!wget -q https://raw.githubusercontent.com/priyankathoa-droid/python-code-analyzer-streamlit/main/colab_setup.py

# Run the setup
!python colab_setup.py
```

### Step 4: Run the cell
Click the play button or press `Shift + Enter`

### Step 5: Access your app
Click the ngrok URL that appears in the output

---

## Method 3: Manual Setup (Full Control)

```python
# 1. Install dependencies
!pip install -q streamlit pyngrok

# 2. Create the app file
%%writefile app.py
import streamlit as st
import re
import zipfile
from pathlib import Path

st.set_page_config(page_title="Python Code Analyzer", page_icon="🐍", layout="wide")

st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;">
    <h1>🐍 Python Code Analyzer</h1>
    <p>Upload your Python project for comprehensive analysis</p>
</div>
""", unsafe_allow_html=True)

def analyze_python_code(files_content):
    analysis = {
        'total_files': len(files_content),
        'python_files': sum(1 for f in files_content if f['name'].endswith('.py')),
        'total_lines': 0,
        'llm_libraries': set(),
        'frameworks': set(),
        'env_vars': {'hardcoded': [], 'from_env': []},
        'architecture': {'patterns': set()}
    }
    
    llm_patterns = {
        'OpenAI': r'import openai|from openai',
        'Anthropic': r'import anthropic|from anthropic',
        'LangChain': r'import langchain|from langchain',
        'Hugging Face': r'import transformers|from transformers',
        'Gemini': r'import google\\.generativeai|from google\\.generativeai'
    }
    
    framework_patterns = {
        'FastAPI': r'from fastapi|import fastapi',
        'Flask': r'from flask|import flask',
        'Django': r'from django|import django',
        'Streamlit': r'import streamlit',
        'PyTorch': r'import torch',
        'TensorFlow': r'import tensorflow'
    }
    
    for file_info in files_content:
        content = file_info['content']
        lines = content.split('\\n')
        analysis['total_lines'] += len(lines)
        
        for name, pattern in llm_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                analysis['llm_libraries'].add(name)
        
        for name, pattern in framework_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                analysis['frameworks'].add(name)
        
        if re.search(r'api[_-]?key\\s*=\\s*["\'][^"\']+["\']', content, re.IGNORECASE):
            analysis['env_vars']['hardcoded'].append(file_info['name'])
        
        if re.search(r'os\\.getenv|os\\.environ', content):
            analysis['env_vars']['from_env'].append(file_info['name'])
        
        if re.search(r'async def', content):
            analysis['architecture']['patterns'].add('Async/Await')
        if re.search(r'class\\s+\\w+', content):
            analysis['architecture']['patterns'].add('OOP')
    
    return analysis

uploaded_files = st.file_uploader("Upload Python files", type=['py', 'txt'], accept_multiple_files=True)

if uploaded_files:
    files_content = []
    for f in uploaded_files:
        try:
            files_content.append({'name': f.name, 'content': f.read().decode('utf-8')})
        except:
            pass
    
    st.success(f"✅ Uploaded {len(files_content)} files")
    
    if st.button("🔍 Analyze Code", type="primary"):
        analysis = analyze_python_code(files_content)
        
        st.markdown("## 📊 Results")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Files", analysis['total_files'])
        col2.metric("Python Files", analysis['python_files'])
        col3.metric("Total Lines", analysis['total_lines'])
        
        st.markdown("### 🤖 LLM Libraries")
        if analysis['llm_libraries']:
            for lib in analysis['llm_libraries']:
                st.markdown(f"- {lib}")
        else:
            st.info("None detected")
        
        st.markdown("### 🔧 Frameworks")
        if analysis['frameworks']:
            for fw in analysis['frameworks']:
                st.markdown(f"- {fw}")
        else:
            st.info("None detected")
        
        st.markdown("### ⚠️ Security")
        if analysis['env_vars']['hardcoded']:
            st.warning(f"Hardcoded credentials in: {', '.join(analysis['env_vars']['hardcoded'])}")
        else:
            st.success("No hardcoded credentials")
        
        st.markdown("### 🏗️ Architecture")
        if analysis['architecture']['patterns']:
            for p in analysis['architecture']['patterns']:
                st.markdown(f"- {p}")

# 3. Setup ngrok and run
from pyngrok import ngrok
import threading
import subprocess
import time

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"])

thread = threading.Thread(target=run_streamlit, daemon=True)
thread.start()
time.sleep(5)

public_url = ngrok.connect(8501)
print(f"🔗 Your app is running at: {public_url}")
```

---

## 📝 Usage Instructions

1. **Upload Files**: Click "Browse files" or drag & drop
2. **Analyze**: Click the "Analyze Code" button
3. **Review Results**: See detected LLMs, frameworks, security issues, and architecture

## 🎯 What Gets Analyzed

- ✅ LLM libraries (OpenAI, Anthropic, LangChain, etc.)
- ✅ Frameworks (FastAPI, Flask, Django, PyTorch, etc.)
- ✅ Hardcoded credentials and secrets
- ✅ Environment variable usage
- ✅ Architecture patterns (Async, OOP, REST API)
- ✅ Best practices and recommendations

## 🔧 Troubleshooting

**Issue**: "Module not found"
- **Solution**: Run `!pip install streamlit pyngrok` again

**Issue**: "Port already in use"
- **Solution**: Restart the Colab runtime (Runtime → Restart runtime)

**Issue**: "ngrok URL not working"
- **Solution**: Wait 10 seconds and try again, or restart the cell

---

## 💡 Tips

- Upload ZIP files for entire projects
- Upload individual .py files for quick checks
- Keep the Colab cell running while using the app
- The ngrok URL is temporary and changes each run

---

Built with ❤️ using Streamlit