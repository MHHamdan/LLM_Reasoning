# smart_web_analyzer.py
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import torch
from typing import Dict, List, Optional
import logging
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebAnalyzer:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        self._models: Dict[str, Optional[pipeline]] = {
            'summarize': None,
            'sentiment': None,
            'topics': None
        }
        
    def _load_model(self, model_type: str) -> None:
        """Lazy load models only when needed"""
        if self._models[model_type] is None:
            logger.info(f"Loading {model_type} model...")
            if model_type == 'summarize':
                self._models[model_type] = pipeline(
                    "summarization",
                    model="facebook/bart-large-cnn",
                    device=self.device
                )
            elif model_type == 'sentiment':
                self._models[model_type] = pipeline(
                    "text-classification",
                    model="nlptown/bert-base-multilingual-uncased-sentiment",
                    device=self.device
                )
            elif model_type == 'topics':
                self._models[model_type] = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=self.device
                )
    
    @lru_cache(maxsize=100)
    def fetch_content(self, url: str) -> str:
        """Fetch webpage content with caching and better error handling"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            raise ValueError(f"Failed to fetch content: {str(e)}")

    def clean_html(self, html: str) -> str:
        """Extract readable text content from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "meta", "noscript"]):
            script.decompose()
            
        # Extract text while preserving some structure
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text

    def analyze(self, url: str, modes: List[str]) -> Dict:
        """Improved analysis pipeline with better error handling"""
        results = {}
        
        try:
            # Fetch and clean content
            html = self.fetch_content(url)
            cleaned_text = self.clean_html(html)
            results['clean_text'] = cleaned_text
            
            # Validate text length
            if len(cleaned_text.split()) < 10:
                raise ValueError("Insufficient text content found on page")
            
            # Text chunks for different models
            summary_text = cleaned_text[:2048]  # BART limit
            classification_text = cleaned_text[:512]  # BERT limit
            
            for mode in modes:
                if mode not in self._models:
                    continue
                    
                self._load_model(mode)
                
                if mode == 'summarize':
                    summary = self._models[mode](summary_text, 
                                              max_length=150,
                                              min_length=30,
                                              do_sample=False)[0]['summary_text']
                    results['summary'] = summary
                    
                elif mode == 'sentiment':
                    sentiment = self._models[mode](classification_text)[0]
                    results['sentiment'] = f"{sentiment['label']} ({sentiment['score']:.2f})"
                    
                elif mode == 'topics':
                    topics = self._models[mode](
                        classification_text,
                        candidate_labels=[
                            "Technology", "Artificial Intelligence",
                            "Business", "Science", "Politics",
                            "Health", "Environment", "Education"
                        ]
                    )
                    results['topics'] = {
                        topic: score 
                        for topic, score in zip(topics['labels'], topics['scores'])
                        if score > 0.1  # Filter low confidence topics
                    }
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            results['error'] = str(e)
            
        return results

# app.py
import gradio as gr
from smart_web_analyzer import WebAnalyzer

analyzer = WebAnalyzer()

def format_results(results: Dict) -> Dict:
    """Format analysis results for Gradio tabs"""
    outputs = {}
    
    if 'error' in results:
        return {
            "📜 Clean Text": f"❌ Error: {results['error']}",
            "📝 Summary": "",
            "🎭 Sentiment": "",
            "📊 Topics": ""
        }
    
    # Clean text tab
    text_preview = results.get('clean_text', 'No text extracted')
    if len(text_preview) > 1000:
        text_preview = text_preview[:1000] + "...(truncated)"
    outputs["📜 Clean Text"] = text_preview
    
    # Summary tab    
    if 'summary' in results:
        outputs["📝 Summary"] = f"**AI Summary:**\n{results['summary']}"
    else:
        outputs["📝 Summary"] = ""
        
    # Sentiment tab    
    if 'sentiment' in results:
        outputs["🎭 Sentiment"] = f"**Sentiment Analysis:**\n{results['sentiment']}"
    else:
        outputs["🎭 Sentiment"] = ""
        
    # Topics tab
    if 'topics' in results:
        topics = "\n".join([
            f"- **{k}**: {v:.1%}" 
            for k,v in sorted(results['topics'].items(), 
                            key=lambda x: x[1], reverse=True)
        ])
        outputs["📊 Topics"] = f"**Detected Topics:**\n{topics}"
    else:
        outputs["📊 Topics"] = ""
    
    return outputs

with gr.Blocks(title="Smart Web Analyzer Plus") as demo:
    gr.Markdown("# 🌐 Smart Web Analyzer Plus")
    gr.Markdown("Analyze web content with AI - extract summaries, sentiment, and topics.")
    
    with gr.Row():
        with gr.Column(scale=4):
            url_input = gr.Textbox(
                label="Enter URL",
                placeholder="https://example.com",
                show_label=True
            )
        with gr.Column(scale=2):
            modes = gr.CheckboxGroup(
                ["summarize", "sentiment", "topics"],
                label="Analysis Types",
                value=["summarize"]  # Default selection
            )
        with gr.Column(scale=1):
            submit_btn = gr.Button("Analyze", variant="primary")
    
    with gr.Tabs() as tabs:
        text_tab = gr.Tab("📜 Clean Text")
        with text_tab:
            clean_text = gr.Markdown()
        
        summary_tab = gr.Tab("📝 Summary")
        with summary_tab:
            summary = gr.Markdown()
            
        sentiment_tab = gr.Tab("🎭 Sentiment")
        with sentiment_tab:
            sentiment = gr.Markdown()
            
        topics_tab = gr.Tab("📊 Topics")
        with topics_tab:
            topics = gr.Markdown()
    
    # Example URLs
    examples = gr.Examples(
        examples=[
            ["https://www.bbc.com/news/technology-67881954", ["summarize", "sentiment"]],
            ["https://arxiv.org/html/2312.17296v1", ["topics", "summarize"]]
        ],
        inputs=[url_input, modes]
    )
    
    # Handle submission
    submit_btn.click(
        fn=lambda url, m: format_results(analyzer.analyze(url, m)),
        inputs=[url_input, modes],
        outputs=[clean_text, summary, sentiment, topics],
        api_name="analyze"
    )
    
    # Error handling for empty URL
    url_input.change(
        fn=lambda x: gr.update(interactive=bool(x.strip())),
        inputs=[url_input],
        outputs=[submit_btn]
    )

if __name__ == "__main__":
    demo.launch()