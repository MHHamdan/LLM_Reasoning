import os
import requests

HF_TOKEN = os.environ.get("HF_REPO_API")
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def commit_files_to_space():
    # Prepare files content
    files = {
        'app.py': app_content,  # The content from previous code
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
    else:
        print("Error committing files:", response.text)
        print("Status code:", response.status_code)

# Execute the commit
commit_files_to_space()