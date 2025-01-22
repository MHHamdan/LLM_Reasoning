{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from pydantic_settings import BaseSettings\
from dotenv import load_dotenv\
import os\
\
# Load environment variables\
load_dotenv()\
\
class Settings(BaseSettings):\
    # API Configurations\
    API_VERSION: str = "v1"\
    API_PREFIX: str = "/api"\
    DEBUG: bool = False\
    \
    # AI Model Configurations\
    OPENAI_API_KEY: str = Field(..., env='OPENAI_API_KEY')\
    DEFAULT_MODEL: str = "gpt-3.5-turbo"\
    MAX_TOKENS: int = 1000\
    \
    # Database Configurations\
    DATABASE_URL: str = Field(..., env='DATABASE_URL')\
    \
    # Vector Database Configurations\
    PINECONE_API_KEY: str = Field(..., env='PINECONE_API_KEY')\
    PINECONE_ENVIRONMENT: str = Field(..., env='PINECONE_ENVIRONMENT')\
    \
    class Config:\
        env_file = ".env"\
\
# Create settings instance\
settings = Settings()\
\
# Usage example\
if __name__ == "__main__":\
    print(f"API Version: \{settings.API_VERSION\}")\
    print(f"Debug Mode: \{settings.DEBUG\}")}