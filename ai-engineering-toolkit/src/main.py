{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from fastapi import FastAPI, HTTPException, Depends\
from fastapi.middleware.cors import CORSMiddleware\
from typing import List\
import uvicorn\
\
app = FastAPI(title="AI Service API")\
\
# Add CORS middleware\
app.add_middleware(\
    CORSMiddleware,\
    allow_origins=["*"],\
    allow_credentials=True,\
    allow_methods=["*"],\
    allow_headers=["*"],\
)\
\
# Dependencies\
async def get_api_key(api_key: str = Header(...)):\
    if api_key != settings.API_KEY:\
        raise HTTPException(status_code=401, detail="Invalid API key")\
    return api_key\
\
# Routes\
@app.post("/ai/generate", response_model=GenerationResponse)\
async def generate_text(\
    request: GenerationRequest,\
    api_key: str = Depends(get_api_key)\
):\
    try:\
        result = await process_generation(request)\
        return result\
    except Exception as e:\
        raise HTTPException(status_code=500, detail=str(e))\
\
# Health check endpoint\
@app.get("/health")\
async def health_check():\
    return \{"status": "healthy"\}\
\
if __name__ == "__main__":\
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)}