# deploy_to_hf.py

import os
import requests

# Your Hugging Face token
HF_TOKEN = os.environ.get("HF_REPO_API")
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# The main app content (from your previous app.py)
app_content = """
import gradio as gr
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import PyPDF2
import docx
import os
from typing import List, Tuple, Optional

class ContentAnalyzer:
    def __init__(self):
        # Initialize models
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.zero_shot = pipeline("zero-shot-classification")
        
    def read_file(self, file_obj) -> str:
        # ... [rest of your ContentAnalyzer class code]
        pass

# ... [rest of your app.py code]
"""

def commit_files_to_space():
    # Prepare files content
    files = {
        'app.py': app_content,
        'requirements.txt': """gradio>=4.0.0
requests>=2.31.0
beautifulsoup4>=4.12.2
transformers>=4.35.0
torch>=2.0.1
PyPDF2>=3.0.0
python-docx>=0.8.11
smolagents>=0.2.0""",
        'README.md': """---
title: Content Analyzer
emoji: 📑
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Content Analyzer

An advanced content analysis tool that can process:
- Text input
- Web URLs
- Document files (.txt, .pdf, .docx)

## Features
- Text summarization
- Sentiment analysis
- Topic detection
"""
    }

    # Commit each file
    commit_url = "https://huggingface.co/api/spaces/MHamdan/ContentAnalyzer/commit"
    
    operations = []
    for filename, content in files.items():
        operations.append({
            "operation": "create",
            "path": filename,
            "content": content
        })

    commit_data = {
        "operations": operations,
        "commit_message": "Initial content analyzer setup"
    }

    response = requests.post(
        commit_url, 
        headers=headers,
        json=commit_data
    )

    if response.status_code == 200:
        print("Files committed successfully!")
        print("You can view your space at: https://huggingface.co/spaces/MHamdan/ContentAnalyzer")
    else:
        print("Error committing files:", response.text)
        print("Status code:", response.status_code)

if __name__ == "__main__":
    # Verify authentication first
    auth_response = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)
    if auth_response.status_code == 200:
        print("Authentication successful!")
        commit_files_to_space()
    else:
        print("Authentication failed. Please check your token.")
        print("Status code:", auth_response.status_code)
        print("Response:", auth_response.text)