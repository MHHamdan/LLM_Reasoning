# tools/final_answer.py
from smolagents import Tool
from typing import Optional, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class FinalAnswerTool(Tool):
    """Tool for providing final answers to user queries with improved error handling and validation."""
    
    name = "final_answer"
    description = "Tool for providing the final answer to the agent's task with structured output"
    
    inputs: Dict[str, Any] = {
        "answer": {
            "type": "string",
            "description": "The final answer to be returned in JSON format"
        }
    }
    
    output_type = "string"
    
    def __init__(self, description: Optional[str] = None):
        super().__init__()
        self.description = description or self.description
    
    def validate_json(self, answer: str) -> bool:
        """Validate if the answer is proper JSON format."""
        try:
            if isinstance(answer, str):
                json.loads(answer)
            return True
        except json.JSONDecodeError:
            return False
    
    def format_response(self, answer: str) -> str:
        """Format the response to ensure consistent structure."""
        try:
            if isinstance(answer, str):
                # Try to parse as JSON first
                if self.validate_json(answer):
                    return answer
                
                # If not JSON, create a structured response
                return json.dumps({
                    'clean_text': answer,
                    'summary': '',
                    'sentiment': '',
                    'topics': ''
                })
            
            # If answer is already a dict, convert to JSON
            if isinstance(answer, dict):
                return json.dumps(answer)
            
            raise ValueError("Invalid answer format")
            
        except Exception as e:
            logger.error(f"Error formatting response: {str(e)}")
            return json.dumps({
                'error': str(e),
                'clean_text': str(answer),
                'summary': '',
                'sentiment': '',
                'topics': ''
            })
    
    def forward(self, answer: str) -> str:
        """Process and return the final answer with improved error handling.
        
        Args:
            answer: The answer text to be returned
        
        Returns:
            str: The processed answer in JSON format
        """
        try:
            return self.format_response(answer)
        except Exception as e:
            logger.error(f"Error in forward method: {str(e)}")
            return json.dumps({
                'error': str(e),
                'clean_text': 'An error occurred while processing the response',
                'summary': '',
                'sentiment': '',
                'topics': ''
            })

    def __call__(self, answer: str) -> str:
        """Alias for forward method to maintain compatibility"""
        return self.forward(answer)