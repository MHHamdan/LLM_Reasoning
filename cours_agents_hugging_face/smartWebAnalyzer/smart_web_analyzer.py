# smart_web_analyzer.py
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import torch

class WebAnalyzer:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self.models = {
            'summarize': pipeline("summarization", model="facebook/bart-large-cnn"),
            'sentiment': pipeline("text-classification", 
                                model="nlptown/bert-base-multilingual-uncased-sentiment"),
            'topics': pipeline("zero-shot-classification",
                             model="facebook/bart-large-mnli")
        }
    
    def fetch_content(self, url: str) -> str:
        """Fetch webpage content with custom headers"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text

    def clean_html(self, html: str) -> str:
        """Basic HTML cleaning preserving all tags"""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.prettify()

    def analyze(self, url: str, modes: list) -> dict:
        """Core analysis pipeline"""
        results = {}
        try:
            html = self.fetch_content(url)
            results['clean_text'] = self.clean_html(html)
            
            if 'summarize' in modes:
                results['summary'] = self.models['summarize'](html, max_length=150)[0]['summary_text']
                
            if 'sentiment' in modes:
                sentiment = self.models['sentiment'](html[:512])[0]
                results['sentiment'] = f"{sentiment['label']} ({sentiment['score']:.2f})"
                
            if 'topics' in modes:
                topics = self.models['topics'](html[:512], 
                                            candidate_labels=["Technology", "AI", "Business", 
                                                             "Science", "Politics"])
                results['topics'] = {topic: score for topic, score 
                                   in zip(topics['labels'], topics['scores'])}
            
        except Exception as e:
            results['error'] = str(e)
            
        return results