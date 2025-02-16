# app.py
from smolagents import CodeAgent, HfApiModel, Tool
import logging
from Gradio_UI import GradioUI
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AnalysisTool(Tool):
    """Tool for analyzing web content."""
    
    name = "web_analyzer"
    description = "Analyzes web content for summaries, sentiment, and topics"
    
    # Define the required inputs
    inputs: Dict[str, Any] = {
        "text": {
            "type": "string",
            "description": "The text content to analyze"
        },
        "analysis_type": {
            "type": "string",
            "description": "Type of analysis to perform (summarize, sentiment, or topics)"
        }
    }
    
    # Define the output type
    output_type = "string"
    
    def forward(self, text: str, analysis_type: str) -> str:
        """Process the text based on analysis type."""
        try:
            if analysis_type == "summarize":
                return f"Summary of the text: {text[:500]}..."
            elif analysis_type == "sentiment":
                return f"Sentiment analysis of: {text[:500]}..."
            elif analysis_type == "topics":
                return f"Topics identified in: {text[:500]}..."
            else:
                return f"Unknown analysis type: {analysis_type}"
        except Exception as e:
            logger.error(f"Error in analysis: {e}")
            return f"Error during analysis: {str(e)}"

def create_agent():
    """Create and configure the agent."""
    try:
        # Initialize tools
        analyzer = AnalysisTool()
        
        # Initialize model
        model = HfApiModel(
            model_id='Qwen/Qwen2.5-Coder-32B-Instruct',
            max_tokens=2096,
            temperature=0.5
        )
        
        # Create agent with tools
        return CodeAgent(
            model=model,
            tools=[analyzer],
            max_steps=3,
            verbosity_level=1
        )
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        raise

def main():
    """Main application entry point."""
    try:
        logger.info("Starting Smart Web Analyzer Plus...")
        
        # Create agent
        agent = create_agent()
        logger.info("Agent created successfully")
        
        # Create and launch UI
        ui = GradioUI(agent)
        ui.launch(
            server_name="0.0.0.0",
            server_port=7860
        )
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        raise

if __name__ == "__main__":
    main()