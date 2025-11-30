"""
Python Code Analyzer - Google Colab Setup
Run this in Google Colab to analyze your Python code with Streamlit UI
"""

# Install required packages
print("📦 Installing required packages...")
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "streamlit", "pyngrok"])

print("✅ Packages installed successfully!")
print("\n" + "="*60)
print("🐍 Python Code Analyzer - Streamlit UI")
print("="*60)

# Create the Streamlit app file
app_code = '''import streamlit as st
import re
import zipfile
import io
from pathlib import Path

st.set_page_config(page_title="Python Code Analyzer", page_icon="🐍", layout="wide")

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .tag {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
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
        'env_vars': {'hardcoded': [], 'from_env': [], 'has_env_file': False},
        'architecture': {'patterns': set()},
        'best_practices': [],
        'issues': []
    }
    
    llm_patterns = {
        'OpenAI': r'import openai|from openai',
        'Anthropic (Claude)': r'import anthropic|from anthropic',
        'LangChain': r'import langchain|from langchain',
        'Hugging Face': r'import transformers|from transformers',
        'Google AI (Gemini)': r'import google\\.generativeai|from google\\.generativeai',
        'Cohere': r'import cohere|from cohere',
        'Groq': r'import groq|from groq'
    }
    
    framework_patterns = {
        'FastAPI': r'from fastapi|import fastapi',
        'Flask': r'from flask|import flask',
        'Django': r'from django|import django',
        'Streamlit': r'import streamlit',
        'PyTorch': r'import torch',
        'TensorFlow': r'import tensorflow',
        'NumPy': r'import numpy',
        'Pandas': r'import pandas'
    }
    
    for file_info in files_content:
        content = file_info['content']
        file_name = file_info['name']
        lines = content.split('\\n')
        analysis['total_lines'] += len(lines)
        
        for name, pattern in llm_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                analysis['llm_libraries'].add(name)
        
        for name, pattern in framework_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                analysis['frameworks'].add(name)
        
        hardcoded = re.findall(r'api[_-]?key\\s*=\\s*["\'][^"\']+["\']|secret\\s*=\\s*["\'][^"\']+["\']|token\\s*=\\s*["\'][^"\']+["\']', content, re.IGNORECASE)
        if hardcoded:
            analysis['env_vars']['hardcoded'].append({'file': file_name, 'matches': hardcoded})
        
        if re.search(r'os\\.getenv|os\\.environ|load_dotenv', content):
            analysis['env_vars']['from_env'].append(file_name)
        
        if file_name == '.env':
            analysis['env_vars']['has_env_file'] = True
        
        if re.search(r'async def', content):
            analysis['architecture']['patterns'].add('Async/Await')
        if re.search(r'@app\\.route|@router\\.|@api\\.', content):
            analysis['architecture']['patterns'].add('REST API')
        if re.search(r'class\\s+\\w+.*:', content):
            analysis['architecture']['patterns'].add('OOP')
    
    if analysis['env_vars']['from_env']:
        analysis['best_practices'].append('✓ Uses environment variables')
    if any(f['name'] == 'requirements.txt' for f in files_content):
        analysis['best_practices'].append('✓ Has requirements.txt')
    
    if analysis['env_vars']['hardcoded']:
        analysis['issues'].append('⚠️ Hardcoded credentials detected')
    
    return analysis

st.markdown("### 📁 Upload Your Python Project")

upload_method = st.radio("Choose upload method:", ["Upload ZIP file", "Upload individual files"], horizontal=True)

files_content = []

if upload_method == "Upload ZIP file":
    uploaded_zip = st.file_uploader("Upload a ZIP file", type=['zip'])
    if uploaded_zip:
        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith(('.py', '.txt', '.env')):
                    try:
                        content = zip_ref.read(file_name).decode('utf-8')
                        files_content.append({'name': Path(file_name).name, 'content': content})
                    except:
                        pass
        if files_content:
            st.success(f"✅ Extracted {len(files_content)} files")
else:
    uploaded_files = st.file_uploader("Upload Python files", type=['py', 'txt', 'env'], accept_multiple_files=True)
    if uploaded_files:
        for f in uploaded_files:
            try:
                files_content.append({'name': f.name, 'content': f.read().decode('utf-8')})
            except:
                pass
        st.success(f"✅ Uploaded {len(files_content)} files")

if files_content and st.button("🔍 Analyze Code", type="primary", use_container_width=True):
    with st.spinner('Analyzing...'):
        analysis = analyze_python_code(files_content)
    
    st.markdown("## 📊 Analysis Results")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Files", analysis['total_files'])
    col2.metric("Python Files", analysis['python_files'])
    col3.metric("Total Lines", f"{analysis['total_lines']:,}")
    
    st.markdown("### 🤖 LLM & AI Libraries")
    if analysis['llm_libraries']:
        st.markdown("".join([f'<span class="tag">{lib}</span>' for lib in sorted(analysis['llm_libraries'])]), unsafe_allow_html=True)
    else:
        st.info("No LLM libraries detected")
    
    st.markdown("### 🔧 Frameworks & Libraries")
    if analysis['frameworks']:
        st.markdown("".join([f'<span class="tag">{fw}</span>' for fw in sorted(analysis['frameworks'])]), unsafe_allow_html=True)
    else:
        st.info("No major frameworks detected")
    
    st.markdown("### ⚠️ Environment Variables")
    if analysis['env_vars']['hardcoded']:
        st.warning(f"⚠️ Found hardcoded credentials in {len(analysis['env_vars']['hardcoded'])} file(s)")
        for item in analysis['env_vars']['hardcoded']:
            st.markdown(f"- 📄 `{item['file']}`")
    else:
        st.success("✅ No hardcoded credentials detected")
    
    if analysis['env_vars']['from_env']:
        st.success(f"✅ {len(analysis['env_vars']['from_env'])} file(s) use environment variables")
    
    st.markdown("### 🏗️ Architecture Patterns")
    if analysis['architecture']['patterns']:
        st.markdown("".join([f'<span class="tag">{p}</span>' for p in sorted(analysis['architecture']['patterns'])]), unsafe_allow_html=True)
    else:
        st.info("Basic structure")
    
    st.markdown("### ✅ Best Practices")
    if analysis['best_practices']:
        for bp in analysis['best_practices']:
            st.markdown(f"- {bp}")
    else:
        st.warning("Consider implementing best practices")
    
    st.markdown("### 💡 Recommendations")
    recs = []
    if analysis['env_vars']['hardcoded']:
        recs.append("Move hardcoded credentials to environment variables")
    if not analysis['env_vars']['has_env_file']:
        recs.append("Create a .env file")
    if analysis['llm_libraries']:
        recs.append("Add error handling for API calls")
    recs.extend(["Add logging", "Implement unit tests", "Add docstrings"])
    for rec in recs:
        st.markdown(f"- {rec}")
'''

# Write the app to a file
with open('analyzer_app.py', 'w') as f:
    f.write(app_code)

print("\n✅ Streamlit app created: analyzer_app.py")

# Setup ngrok for public URL
from pyngrok import ngrok
import threading
import time

print("\n🌐 Setting up public URL with ngrok...")

# Kill any existing ngrok tunnels
ngrok.kill()

# Start Streamlit in background
def run_streamlit():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "analyzer_app.py", "--server.port=8501", "--server.headless=true"])

thread = threading.Thread(target=run_streamlit, daemon=True)
thread.start()

# Wait for Streamlit to start
time.sleep(5)

# Create ngrok tunnel
public_url = ngrok.connect(8501)

print("\n" + "="*60)
print("🎉 SUCCESS! Your Streamlit app is running!")
print("="*60)
print(f"\n🔗 Public URL: {public_url}")
print("\n📝 Instructions:")
print("   1. Click the URL above to open your app")
print("   2. Upload your Python project (ZIP or individual files)")
print("   3. Click 'Analyze Code' to see results")
print("\n⚠️  Keep this cell running to maintain the connection")
print("="*60)

# Keep the script running
try:
    thread.join()
except KeyboardInterrupt:
    print("\n\n👋 Shutting down...")
    ngrok.kill()
