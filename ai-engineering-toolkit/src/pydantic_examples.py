{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from datetime import datetime\
from typing import List, Optional\
from pydantic import BaseModel, Field, EmailStr\
\
# Data validation for AI model input\
class ModelInput(BaseModel):\
    text: str = Field(..., min_length=1, max_length=1000)\
    temperature: float = Field(0.7, ge=0, le=1)\
    max_tokens: int = Field(100, ge=1)\
    \
    class Config:\
        json_schema_extra = \{\
            "example": \{\
                "text": "Translate this to French",\
                "temperature": 0.7,\
                "max_tokens": 100\
            \}\
        \}\
\
# Data validation for user data\
class User(BaseModel):\
    username: str = Field(..., min_length=3)\
    email: EmailStr\
    active: bool = True\
    created_at: datetime = Field(default_factory=datetime.now)\
    ai_preferences: Optional[dict] = None\
\
# Example usage\
def process_model_input(input_data: ModelInput):\
    # Your processing logic here\
    return \{"processed": input_data.dict()\}\
\
# Example implementation\
if __name__ == "__main__":\
    # Valid input\
    valid_input = ModelInput(\
        text="Hello, world!",\
        temperature=0.8,\
        max_tokens=50\
    )\
    print(valid_input.dict())\
\
    # Will raise validation error\
    try:\
        invalid_input = ModelInput(\
            text="",  # Too short\
            temperature=1.5,  # Too high\
            max_tokens=0  # Too low\
        )\
    except Exception as e:\
        print(f"Validation error: \{e\}")}