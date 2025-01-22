{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey\
from sqlalchemy.ext.declarative import declarative_base\
from sqlalchemy.orm import sessionmaker, relationship\
from datetime import datetime\
\
# Create database engine\
DATABASE_URL = "postgresql://user:password@localhost/dbname"\
engine = create_engine(DATABASE_URL)\
\
# Create declarative base\
Base = declarative_base()\
\
# Define models\
class User(Base):\
    __tablename__ = "users"\
    \
    id = Column(Integer, primary_key=True)\
    username = Column(String, unique=True, nullable=False)\
    email = Column(String, unique=True, nullable=False)\
    created_at = Column(DateTime, default=datetime.utcnow)\
    queries = relationship("AIQuery", back_populates="user")\
\
class AIQuery(Base):\
    __tablename__ = "ai_queries"\
    \
    id = Column(Integer, primary_key=True)\
    user_id = Column(Integer, ForeignKey("users.id"))\
    query_text = Column(String, nullable=False)\
    result = Column(String)\
    created_at = Column(DateTime, default=datetime.utcnow)\
    user = relationship("User", back_populates="queries")\
\
# Create tables\
Base.metadata.create_all(engine)\
\
# Create session factory\
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)\
\
# Database dependency\
def get_db():\
    db = SessionLocal()\
    try:\
        yield db\
    finally:\
        db.close()}