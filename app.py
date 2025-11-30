import streamlit as st
import re
import zipfile
import io
from pathlib import Path
from collections import defaultdict

st.set_page_config(
    page_title="Python Code Analyzer",
    page_icon="🐍",
    layout="wide"
)

# Custom CSS
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
    .metric-card {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .tag {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🐍 Python Code Analyzer</h1>
    <p>Upload your Python project for comprehensive analysis</p>
</div>
""", unsafe_allow_html=True)

def analyze_python_code(files_content):
    """Analyze Python code for LLMs, frameworks, env vars, and architecture"""
    
    analysis = {
        'total_files': len(files_content),
        'python_files': sum(1 for f in files_content if f['name'].endswith('.py')),
        'total_lines': 0,
        'llm_libraries': set(),
        'frameworks': set(),
        'env_vars': {
            'hardcoded': [],
            'from_env': [],
            'has_env_file': False
        },
        'architecture': {
            'patterns': set()
        },
        'best_practices': [],
        'issues': [],
        'file_details': []
    }
    
    # LLM and AI library patterns
    llm_patterns = {
        'OpenAI': r'import openai|from openai',
        'Anthropic (Claude)': r'import anthropic|from anthropic',
        'LangChain': r'import langchain|from langchain',
        'Hugging Face': r'import transformers|from transformers|import huggingface',
        'Google AI (Gemini)': r'import google\.generativeai|from google\.generativeai',
        'Cohere': r'import cohere|from cohere',
        'LlamaIndex': r'import llama_index|from llama_index',
        'Replicate': r'import replicate|from replicate',
        'Together AI': r'import together|from together',
        'Groq': r'import groq|from groq',
        'Ollama': r'import ollama|from ollama',
        'Mistral AI': r'import mistralai|from mistralai'
    }
    
    # Framework patterns
    framework_patterns = {
        'FastAPI': r'from fastapi|import fastapi',
        'Flask': r'from flask|import flask',
        'Django': r'from django|import django',
        'Streamlit': r'import streamlit',
        'Gradio': r'import gradio',
        'PyTorch': r'import torch',
        'TensorFlow': r'import tensorflow',
        'NumPy': r'import numpy',
        'Pandas': r'import pandas',
        'SQLAlchemy': r'from sqlalchemy|import sqlalchemy',
        'Pydantic': r'from pydantic|import pydantic',
        'Requests': r'import requests',
        'AsyncIO': r'import asyncio',
        'Celery': r'from celery|import celery',
        'Redis': r'import redis',
        'MongoDB': r'import pymongo|from pymongo'
    }
    
    for file_info in files_content:
        content = file_info['content']
        file_name = file_info['name']
        
        lines = content.split('\n')
        analysis['total_lines'] += len(lines)
        
        file_analysis = {
            'name': file_name,
            'lines': len(lines),
            'llms': [],
            'frameworks': [],
            'has_hardcoded': False
        }
        
        # Check for LLM libraries
        for name, pattern in llm_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                analysis['llm_libraries'].add(name)
                file_analysis['llms'].append(name)
        
        # Check for frameworks
        for name, pattern in framework_patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                analysis['frameworks'].add(name)
                file_analysis['frameworks'].append(name)
        
        # Check for hardcoded credentials
        hardcoded_patterns = [
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'password\s*=\s*["\'][^"\']+["\']'
        ]
        
        for pattern in hardcoded_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                analysis['env_vars']['hardcoded'].append({
                    'file': file_name,
                    'matches': matches
                })
                file_analysis['has_hardcoded'] = True
        
        # Check for proper env usage
        if re.search(r'os\.getenv|os\.environ|load_dotenv', content):
            analysis['env_vars']['from_env'].append(file_name)
        
        # Check for .env file
        if file_name == '.env':
            analysis['env_vars']['has_env_file'] = True
        
        # Architecture patterns
        if re.search(r'class.*\(.*BaseModel.*\)', content):
            analysis['architecture']['patterns'].add('Pydantic Models')
        if re.search(r'async def', content):
            analysis['architecture']['patterns'].add('Async/Await Pattern')
        if re.search(r'@app\.route|@router\.|@api\.', content):
            analysis['architecture']['patterns'].add('REST API')
        if re.search(r'class.*Service|class.*Repository|class.*Controller', content):
            analysis['architecture']['patterns'].add('Service Layer Pattern')
        if re.search(r'class\s+\w+.*:', content):
            analysis['architecture']['patterns'].add('Object-Oriented Programming')
        if re.search(r'def\s+\w+\(.*\)\s*->', content):
            analysis['architecture']['patterns'].add('Type Hints')
        
        analysis['file_details'].append(file_analysis)
    
    # Best practices
    if analysis['env_vars']['from_env']:
        analysis['best_practices'].append('✓ Uses environment variables properly')
    if 'Async/Await Pattern' in analysis['architecture']['patterns']:
        analysis['best_practices'].append('✓ Implements asynchronous programming')
    if any(f['name'] == 'requirements.txt' for f in files_content):
        analysis['best_practices'].append('✓ Has requirements.txt for dependencies')
    if 'Type Hints' in analysis['architecture']['patterns']:
        analysis['best_practices'].append('✓ Uses type hints')
    
    # Issues
    if analysis['env_vars']['hardcoded']:
        analysis['issues'].append('⚠️ Hardcoded credentials detected')
    if not any(f['name'] == 'requirements.txt' for f in files_content):
        analysis['issues'].append('⚠️ Missing requirements.txt')
    if not analysis['env_vars']['has_env_file'] and analysis['llm_libraries']:
        analysis['issues'].append('⚠️ No .env file found (recommended for API keys)')
    
    return analysis

def extract_files_from_zip(uploaded_file):
    """Extract Python files from uploaded zip"""
    files_content = []
    
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith(('.py', '.txt', '.toml', '.env', '.cfg', '.ini')):
                try:
                    content = zip_ref.read(file_name).decode('utf-8')
                    files_content.append({
                        'name': Path(file_name).name,
                        'path': file_name,
                        'content': content
                    })
                except:
                    pass
    
    return files_content

def read_uploaded_files(uploaded_files):
    """Read content from uploaded files"""
    files_content = []
    
    for uploaded_file in uploaded_files:
        try:
            content = uploaded_file.read().decode('utf-8')
            files_content.append({
                'name': uploaded_file.name,
                'path': uploaded_file.name,
                'content': content
            })
        except:
            pass
    
    return files_content

# Main UI
st.markdown("### 📁 Upload Your Python Project")

upload_method = st.radio(
    "Choose upload method:",
    ["Upload ZIP file", "Upload individual files"],
    horizontal=True
)

files_content = []

if upload_method == "Upload ZIP file":
    uploaded_zip = st.file_uploader(
        "Upload a ZIP file containing your Python project",
        type=['zip'],
        help="Upload a ZIP archive of your Python project folder"
    )
    
    if uploaded_zip:
        with st.spinner('Extracting files...'):
            files_content = extract_files_from_zip(uploaded_zip)
        
        if files_content:
            st.success(f"✅ Extracted {len(files_content)} files")
        else:
            st.error("❌ No Python files found in the ZIP archive")

else:
    uploaded_files = st.file_uploader(
        "Upload Python files (.py, requirements.txt, .env, etc.)",
        type=['py', 'txt', 'toml', 'env', 'cfg', 'ini'],
        accept_multiple_files=True,
        help="Select multiple files from your Python project"
    )
    
    if uploaded_files:
        files_content = read_uploaded_files(uploaded_files)
        st.success(f"✅ Uploaded {len(files_content)} files")

# Analyze button
if files_content:
    st.markdown("---")
    
    # Show uploaded files
    with st.expander("📄 View Uploaded Files", expanded=False):
        for file_info in files_content:
            st.text(f"• {file_info['path']} ({len(file_info['content'].split(chr(10)))} lines)")
    
    if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
        with st.spinner('Analyzing your Python code...'):
            analysis = analyze_python_code(files_content)
        
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Files", analysis['total_files'])
        with col2:
            st.metric("Python Files", analysis['python_files'])
        with col3:
            st.metric("Total Lines", f"{analysis['total_lines']:,}")
        
        st.markdown("---")
        
        # LLM Libraries
        st.markdown("### 🤖 LLM & AI Libraries Detected")
        if analysis['llm_libraries']:
            tags_html = "".join([f'<span class="tag">{lib}</span>' for lib in sorted(analysis['llm_libraries'])])
            st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No LLM libraries detected")
        
        st.markdown("---")
        
        # Frameworks
        st.markdown("### 🔧 Frameworks & Libraries")
        if analysis['frameworks']:
            tags_html = "".join([f'<span class="tag">{fw}</span>' for fw in sorted(analysis['frameworks'])])
            st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)
        else:
            st.info("No major frameworks detected")
        
        st.markdown("---")
        
        # Environment Variables
        st.markdown("### ⚠️ Environment Variables Analysis")
        
        if analysis['env_vars']['hardcoded']:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("**⚠️ Hardcoded Credentials Found:**")
            for item in analysis['env_vars']['hardcoded']:
                st.markdown(f"- 📄 `{item['file']}`")
                for match in item['matches'][:3]:  # Show first 3 matches
                    st.code(match, language='python')
            st.markdown("**Recommendation:** Move these to environment variables!")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("✅ No hardcoded credentials detected")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if analysis['env_vars']['from_env']:
            st.success(f"✅ {len(analysis['env_vars']['from_env'])} file(s) properly use environment variables")
        
        if analysis['env_vars']['has_env_file']:
            st.success("✅ .env file present")
        
        st.markdown("---")
        
        # Architecture
        st.markdown("### 🏗️ Architecture & Patterns")
        if analysis['architecture']['patterns']:
            tags_html = "".join([f'<span class="tag">{p}</span>' for p in sorted(analysis['architecture']['patterns'])])
            st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)
        else:
            st.info("Basic procedural structure")
        
        st.markdown("---")
        
        # Best Practices
        st.markdown("### ✅ Best Practices")
        if analysis['best_practices']:
            for bp in analysis['best_practices']:
                st.markdown(f"- {bp}")
        else:
            st.warning("Consider implementing more best practices")
        
        st.markdown("---")
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        recommendations = []
        
        if analysis['env_vars']['hardcoded']:
            recommendations.append("Move hardcoded credentials to environment variables")
        if not analysis['env_vars']['has_env_file']:
            recommendations.append("Create a .env file for configuration")
        if analysis['llm_libraries']:
            recommendations.append("Implement proper error handling for API calls")
            recommendations.append("Add rate limiting and retry logic")
        if 'Async/Await Pattern' not in analysis['architecture']['patterns'] and analysis['llm_libraries']:
            recommendations.append("Consider using async/await for better performance")
        recommendations.append("Add comprehensive logging")
        recommendations.append("Implement unit tests")
        recommendations.append("Add docstrings to functions and classes")
        
        for rec in recommendations:
            st.markdown(f"- {rec}")
        
        st.markdown("---")
        
        # File-by-file breakdown
        with st.expander("📋 Detailed File Analysis", expanded=False):
            for file_detail in analysis['file_details']:
                st.markdown(f"**{file_detail['name']}** ({file_detail['lines']} lines)")
                if file_detail['llms']:
                    st.markdown(f"  - LLMs: {', '.join(file_detail['llms'])}")
                if file_detail['frameworks']:
                    st.markdown(f"  - Frameworks: {', '.join(file_detail['frameworks'])}")
                if file_detail['has_hardcoded']:
                    st.markdown("  - ⚠️ Contains hardcoded credentials")
                st.markdown("")

else:
    st.info("👆 Upload your Python project to get started")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Built with Streamlit 🎈 | Analyze Python code for LLMs, frameworks, and best practices</p>
</div>
""", unsafe_allow_html=True)