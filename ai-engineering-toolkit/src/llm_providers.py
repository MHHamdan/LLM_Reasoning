{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from typing import Dict, Optional\
import anthropic\
import cohere\
from tenacity import retry, stop_after_attempt, wait_exponential\
\
class AnthropicProvider:\
    def __init__(self, api_key: str):\
        self.client = anthropic.Client(api_key=api_key)\
    \
    @retry(\
        stop=stop_after_attempt(3),\
        wait=wait_exponential(multiplier=1, min=4, max=10)\
    )\
    async def generate(\
        self,\
        prompt: str,\
        max_tokens: int = 1000,\
        temperature: float = 0.7\
    ) -> Dict:\
        response = await self.client.messages.create(\
            model="claude-3-opus-20240229",\
            max_tokens=max_tokens,\
            temperature=temperature,\
            messages=[\{"role": "user", "content": prompt\}]\
        )\
        \
        return \{\
            'text': response.content,\
            'usage': response.usage\
        \}\
\
class CohereProvider:\
    def __init__(self, api_key: str):\
        self.client = cohere.Client(api_key)\
    \
    @retry(\
        stop=stop_after_attempt(3),\
        wait=wait_exponential(multiplier=1, min=4, max=10)\
    )\
    async def generate(\
        self,\
        prompt: str,\
        max_tokens: int = 1000,\
        temperature: float = 0.7\
    ) -> Dict:\
        response = await self.client.generate(\
            prompt=prompt,\
            max_tokens=max_tokens,\
            temperature=temperature\
        )\
        \
        return \{\
            'text': response.generations[0].text,\
            'tokens_used': response.meta.billed_tokens\
        \}\
\
# Unified interface for all providers\
class LLMProviderFactory:\
    def __init__(self):\
        self.providers = \{\}\
    \
    def register_provider(\
        self,\
        name: str,\
        provider: any,\
        api_key: str\
    ):\
        self.providers[name] =}