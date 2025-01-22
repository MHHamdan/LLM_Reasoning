{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from celery import Celery\
from celery.schedules import crontab\
import time\
\
# Initialize Celery\
celery_app = Celery(\
    'ai_tasks',\
    broker='redis://localhost:6379/0',\
    backend='redis://localhost:6379/1'\
)\
\
# Configure Celery\
celery_app.conf.update(\
    result_expires=3600,  # Results expire in 1 hour\
    task_serializer='json',\
    accept_content=['json'],\
    result_serializer='json',\
    timezone='UTC',\
    enable_utc=True,\
)\
\
# Define periodic tasks\
celery_app.conf.beat_schedule = \{\
    'update-embeddings-daily': \{\
        'task': 'celery_tasks.update_embeddings',\
        'schedule': crontab(hour=0, minute=0)  # Run daily at midnight\
    \}\
\}\
\
@celery_app.task(bind=True, retry_backoff=True)\
def process_document(self, document_id: str):\
    try:\
        # Simulate document processing\
        time.sleep(5)\
        return \{"status": "completed", "document_id": document_id\}\
    except Exception as exc:\
        self.retry(exc=exc, countdown=60)  # Retry after 1 minute\
\
@celery_app.task\
def update_embeddings():\
    # Update document embeddings\
    return \{"status": "embeddings updated"\}\
\
# Task for handling AI model inference\
@celery_app.task(rate_limit='10/m')  # Limit to 10 tasks per minute\
def ai_inference(input_text: str):\
    # Your AI inference code here\
    return \{"result": "processed"\}}