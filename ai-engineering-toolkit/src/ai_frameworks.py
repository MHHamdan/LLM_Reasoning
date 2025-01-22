{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from langchain.chat_models import ChatOpenAI\
from langchain.prompts import ChatPromptTemplate\
from langchain.schema import StrOutputParser\
from langchain.schema.runnable import Runnable\
from llama_index import VectorStoreIndex, SimpleDirectoryReader\
import dspy\
\
# LangChain implementation\
class LangChainService:\
    def __init__(self, openai_api_key: str):\
        self.llm = ChatOpenAI(openai_api_key=openai_api_key)\
        \
    def create_chain(self) -> Runnable:\
        prompt = ChatPromptTemplate.from_messages([\
            ("system", "You are a helpful AI assistant."),\
            ("user", "\{input\}")\
        ])\
        \
        chain = prompt | self.llm | StrOutputParser()\
        return chain\
    \
    async def process_input(self, user_input: str) -> str:\
        chain = self.create_chain()\
        result = await chain.ainvoke(\{"input": user_input\})\
        return result\
\
# LlamaIndex implementation\
class LlamaIndexService:\
    def __init__(self, documents_dir: str):\
        documents = SimpleDirectoryReader(documents_dir).load_data()\
        self.index = VectorStoreIndex.from_documents(documents)\
        \
    def query_documents(self, query: str) -> str:\
        query_engine = self.index.as_query_engine()\
        response = query_engine.query(query)\
        return response.response\
\
# DSPy implementation\
class DSPyModule(dspy.Module):\
    def __init__(self):\
        super().__init__()\
        self.gen = dspy.ChainOfThought("question -> answer")\
    \
    def forward(self, question: str) -> str:\
        pred = self.gen(question=question)\
        return pred.answer}