{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import instructor\
from openai import OpenAI\
from typing import List, Optional\
\
# Initialize OpenAI client with instructor\
client = instructor.patch(OpenAI())\
\
# Define output structures\
class GenerationResult(BaseModel):\
    text: str\
    confidence: float\
    tokens_used: int\
    \
class AnalysisResult(BaseModel):\
    sentiment: str\
    key_points: List[str]\
    summary: str\
\
# LLM integration class\
class LLMService:\
    def __init__(self, api_key: str):\
        self.client = OpenAI(api_key=api_key)\
    \
    async def generate_text(\
        self, \
        prompt: str, \
        temperature: float = 0.7\
    ) -> GenerationResult:\
        response = await self.client.chat.completions.create(\
            model="gpt-3.5-turbo",\
            messages=[\{"role": "user", "content": prompt\}],\
            temperature=temperature\
        )\
        \
        return GenerationResult(\
            text=response.choices[0].message.content,\
            confidence=response.choices[0].finish_reason == "stop",\
            tokens_used=response.usage.total_tokens\
        )\
    \
    async def analyze_text(self, text: str) -> AnalysisResult:\
        # Use instructor for structured output\
        return await self.client.chat.completions.create(\
            model="gpt-3.5-turbo",\
            response_model=AnalysisResult,\
            messages=[\{\
                "role": "user", \
                "content": f"Analyze this text: \{text\}"\
            \}]\
        )}