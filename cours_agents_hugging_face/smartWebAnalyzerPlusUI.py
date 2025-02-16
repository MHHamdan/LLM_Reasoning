import gradio as gr
import json
from smolagents import load_tool
import time
from datetime import datetime
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import os

# Load the analyzer with caching
analyzer = load_tool("MHamdan/smart-web-analyzer-plus", trust_remote_code=True)
analysis_cache = {}

def create_sentiment_chart(sentiment_data):
    """Creates an interactive bar chart for sentiment analysis."""
    sections = []
    scores = []
    
    for item in sentiment_data['sections']:
        sections.append(f"Section {item['section']}")
        scores.append(item['score'])
    
    fig = go.Figure(data=[
        go.Bar(
            x=sections,
            y=scores,
            marker_color='rgb(55, 83, 109)',
            text=scores,
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title='Sentiment Analysis by Section',
        xaxis_title='Content Sections',
        yaxis_title='Sentiment Score (1-5)',
        yaxis_range=[0, 5]
    )
    
    return fig

def generate_pdf_report(analysis_result):
    """Generates a PDF report from analysis results."""
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Content Analysis Report', 0, 1, 'C')
    pdf.line(10, 30, 200, 30)
    
    # Date
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
    
    # Content
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Basic Statistics:', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    stats = analysis_result.get('stats', {})
    for key, value in stats.items():
        pdf.cell(0, 10, f'{key.title()}: {value}', 0, 1)
    
    if 'summary' in analysis_result:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Summary:', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 10, analysis_result['summary'])
    
    # Save to temporary file
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, 'analysis_report.pdf')
    pdf.output(pdf_path)
    
    return pdf_path
def process_content(input_text, mode, theme, progress=gr.Progress()):
    """Main processing function with error handling."""
    try:
        cache_key = f"{input_text}_{mode}"
        if cache_key in analysis_cache:
            return (
                analysis_cache[cache_key],
                "Content preview unavailable for cached results",
                "Using cached results",
                None
            )

        progress(0, desc="Initializing analysis...")
        time.sleep(0.5)

        progress(0.3, desc="Fetching content...")
        result = analyzer(input_text, mode)

        # Ensure valid JSON
        try:
            analysis_result = json.loads(result)
        except json.JSONDecodeError:
            raise ValueError("The response from the analyzer is not valid JSON.")

        progress(0.6, desc="Analyzing content...")

        # If no response content, return an error
        if not analysis_result or "status" not in analysis_result:
            raise ValueError("Received an empty or invalid response from the analyzer.")

        # Handle sentiment visualization
        chart = None
        if mode == "sentiment" and analysis_result.get('status') == 'success':
            progress(0.8, desc="Generating visualizations...")
            chart = create_sentiment_chart(analysis_result.get('sentiment_analysis', {}))

        # Cache results
        analysis_cache[cache_key] = analysis_result

        preview = analysis_result.get('stats', {}).get('title', '')
        if 'summary' in analysis_result:
            preview += f"\n\nSummary:\n{analysis_result['summary']}"

        progress(1.0, desc="Complete!")
        return analysis_result, preview, "Analysis complete!", chart

    except Exception as e:
        return (
            {"status": "error", "message": str(e)},
            "Error occurred",
            f"Error: {str(e)}",
            None
        )

    """Main processing function with progress updates."""
    try:
        cache_key = f"{input_text}_{mode}"
        if cache_key in analysis_cache:
            return (
                analysis_cache[cache_key],
                "Content preview unavailable for cached results",
                "Using cached results",
                None
            )
        
        progress(0, desc="Initializing analysis...")
        time.sleep(0.5)  
        progress(0.3, desc="Fetching content...")
        result = analyzer(input_text, mode)
        analysis_result = json.loads(result)
        
        progress(0.6, desc="Analyzing content...")
        
        chart = None
        if mode == "sentiment" and analysis_result.get('status') == 'success':
            progress(0.8, desc="Generating visualizations...")
            chart = create_sentiment_chart(analysis_result['sentiment_analysis'])
        
        analysis_cache[cache_key] = analysis_result
        preview = analysis_result.get('stats', {}).get('title', '')
        if 'summary' in analysis_result:
            preview += f"\n\nSummary:\n{analysis_result['summary']}"
        
        progress(1.0, desc="Complete!")
        return analysis_result, preview, "Analysis complete!", chart
        
    except Exception as e:
        return (
            {"status": "error", "message": str(e)},
            "Error occurred",
            f"Error: {str(e)}",
            None
        )