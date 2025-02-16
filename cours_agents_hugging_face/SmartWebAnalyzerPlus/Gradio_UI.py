# Gradio_UI.py
import gradio as gr
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebAnalyzer:
    def __init__(self, agent):
        self.agent = agent

    def fetch_webpage(self, url: str) -> str:
        """Fetch and extract text content from a webpage."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator='\n')
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            text = '\n'.join(line for line in lines if line)
            return text
        except Exception as e:
            logger.error(f"Error fetching webpage: {e}")
            return f"Error: Failed to fetch webpage - {str(e)}"

    def analyze_content(self, url: str, analysis_types: List[str]) -> Tuple[str, str, str, str]:
        """Analyze webpage content based on selected analysis types."""
        try:
            # Fetch content
            content = self.fetch_webpage(url)
            if content.startswith("Error:"):
                return content, "", "", ""

            # Initialize results
            clean_text = content[:2000] + "..." if len(content) > 2000 else content
            summary = ""
            sentiment = ""
            topics = ""

            # Perform selected analyses
            if "summarize" in analysis_types:
                summary = self.agent.run(f"Please summarize this text concisely: {clean_text}")

            if "sentiment" in analysis_types:
                sentiment = self.agent.run(f"Analyze the sentiment of this text: {clean_text}")

            if "topics" in analysis_types:
                topics = self.agent.run(f"Identify and list the main topics in this text: {clean_text}")

            return clean_text, summary, sentiment, topics

        except Exception as e:
            error_msg = f"Error during analysis: {str(e)}"
            logger.error(error_msg)
            return error_msg, "", "", ""

class GradioUI:
    def __init__(self, agent):
        self.analyzer = WebAnalyzer(agent)

    def create_interface(self):
        """Create the Gradio interface."""
        # Create interface components
        url_input = gr.Textbox(
            label="Enter URL",
            placeholder="https://example.com"
        )
        
        analysis_types = gr.CheckboxGroup(
            choices=["summarize", "sentiment", "topics"],
            value=["summarize"],
            label="Analysis Types"
        )

        # Create output components
        with gr.Blocks() as demo:
            gr.Markdown("# Smart Web Analyzer Plus")
            gr.Markdown("Analyze web content using AI to extract summaries, determine sentiment, and identify topics.")

            with gr.Row():
                with gr.Column(scale=4):
                    url_input.render()
                with gr.Column(scale=2):
                    analysis_types.render()
                with gr.Column(scale=1):
                    analyze_button = gr.Button("Analyze", variant="primary")

            # Status indicator
            status = gr.Markdown(visible=False)

            # Output tabs
            with gr.Tabs():
                with gr.Tab("Clean Text"):
                    clean_text_output = gr.Markdown()
                with gr.Tab("Summary"):
                    summary_output = gr.Markdown()
                with gr.Tab("Sentiment"):
                    sentiment_output = gr.Markdown()
                with gr.Tab("Topics"):
                    topics_output = gr.Markdown()

            # Examples
            gr.Examples(
                examples=[
                    ["https://www.bbc.com/news/technology-67881954", ["summarize", "sentiment"]],
                    ["https://arxiv.org/html/2312.17296v1", ["topics", "summarize"]]
                ],
                inputs=[url_input, analysis_types],
            )

            # Event handlers
            def on_analyze_click(url, types):
                if not url:
                    return "Please enter a URL", "", "", ""
                if not types:
                    return "Please select at least one analysis type", "", "", ""
                return self.analyzer.analyze_content(url, types)

            analyze_button.click(
                fn=lambda: gr.Markdown("⏳ Analysis in progress...", visible=True),
                outputs=[status]
            ).then(
                fn=on_analyze_click,
                inputs=[url_input, analysis_types],
                outputs=[clean_text_output, summary_output, sentiment_output, topics_output]
            ).then(
                fn=lambda: gr.Markdown("", visible=False),
                outputs=[status]
            )

        return demo

    def launch(self, server_name=None, server_port=None, share=False):
        """Launch the Gradio interface."""
        demo = self.create_interface()
        demo.launch(
            server_name=server_name,
            server_port=server_port,
            share=share
        )