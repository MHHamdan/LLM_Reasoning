# app.py
import gradio as gr
from smart_web_analyzer import WebAnalyzer

analyzer = WebAnalyzer()

def format_results(results: dict) -> dict:
    """Format analysis results for Gradio tabs"""
    outputs = {}
    if 'error' in results:
        return {"📜 Error": f"❌ {results['error']}"}
    
    outputs["📜 Clean Text"] = results.get('clean_text', 'No text extracted')
    
    if 'summary' in results:
        outputs["📝 Summary"] = f"**AI Summary:**\n{results['summary']}"
        
    if 'sentiment' in results:
        outputs["🎭 Sentiment"] = f"**Sentiment Score:**\n{results['sentiment']}"
        
    if 'topics' in results:
        topics = "\n".join([f"- **{k}**: {v:.2f}" for k,v in results['topics'].items()])
        outputs["📊 Topics"] = f"**Detected Topics:**\n{topics}"
    
    return outputs

with gr.Blocks(title="Smart Web Analyzer Plus") as demo:
    gr.Markdown("# 🌐 Smart Web Analyzer Plus")
    
    with gr.Row():
        url_input = gr.Textbox(label="Enter URL", placeholder="https://example.com")
        modes = gr.CheckboxGroup(["summarize", "sentiment", "topics"], 
                                label="Analysis Types")
        submit_btn = gr.Button("Analyze", variant="primary")
    
    with gr.Tabs():
        with gr.Tab("📜 Clean Text"):
            clean_text = gr.Markdown()
        with gr.Tab("📝 Summary"):
            summary = gr.Markdown()
        with gr.Tab("🎭 Sentiment"):
            sentiment = gr.Markdown()
        with gr.Tab("📊 Topics"):
            topics = gr.Markdown()
    
    examples = gr.Examples(
        examples=[
            ["https://www.bbc.com/news/technology-67881954", ["summarize", "sentiment"]],
            ["https://arxiv.org/html/2312.17296v1", ["topics", "summarize"]]
        ],
        inputs=[url_input, modes]
    )
    
    submit_btn.click(
        fn=lambda url, m: format_results(analyzer.analyze(url, m)),
        inputs=[url_input, modes],
        outputs=[clean_text, summary, sentiment, topics]
    )

if __name__ == "__main__":
    demo.launch()