{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from pymongo import MongoClient\
from typing import Dict, List, Optional\
from datetime import datetime\
\
class MongoDBService:\
    def __init__(self, connection_uri: str):\
        self.client = MongoClient(connection_uri)\
        self.db = self.client['ai_service']\
    \
    def store_model_results(\
        self,\
        user_id: str,\
        input_text: str,\
        output: str,\
        model_name: str,\
        metadata: Optional[Dict] = None\
    ):\
        """Store AI model results"""\
        collection = self.db.model_results\
        \
        document = \{\
            'user_id': user_id,\
            'input_text': input_text,\
            'output': output,\
            'model_name': model_name,\
            'timestamp': datetime.utcnow(),\
            'metadata': metadata or \{\}\
        \}\
        \
        return collection.insert_one(document)\
    \
    def get_user_history(\
        self,\
        user_id: str,\
        limit: int = 10\
    ) -> List[Dict]:\
        """Retrieve user's interaction history"""\
        collection = self.db.model_results\
        \
        cursor = collection.find(\
            \{'user_id': user_id\}\
        ).sort(\
            'timestamp', -1\
        ).limit(limit)\
        \
        return list(cursor)\
    \
    def aggregate_model_performance(\
        self,\
        model_name: str,\
        time_range: Dict\
    ) -> Dict:\
        """Aggregate model performance metrics"""\
        collection = self.db.model_results\
        \
        pipeline = [\
            \{\
                '$match': \{\
                    'model_name': model_name,\
                    'timestamp': \{\
                        '$gte': time_range['start'],\
                        '$lte': time_range['end']\
                    \}\
                \}\
            \},\
            \{\
                '$group': \{\
                    '_id': None,\
                    'total_requests': \{'$sum': 1\},\
                    'avg_latency': \{'$avg': '$metadata.latency'\},\
                    'success_rate': \{\
                        '$avg': \{\
                            '$cond': [\
                                \{'$eq': ['$metadata.status', 'success']\},\
                                1,\
                                0\
                            ]\
                        \}\
                    \}\
                \}\
            \}\
        ]\
        \
        result = list(collection.aggregate(pipeline))\
        return result[0] if result else None\
\
# Example usage\
if __name__ == "__main__":\
    mongodb_service = MongoDBService("mongodb://localhost:27017")\
    \
    # Store results\
    mongodb_service.store_model_results(\
        user_id="user123",\
        input_text="Sample input",\
        output="Sample output",\
        model_name="gpt-3.5-turbo",\
        metadata=\{\
            'latency': 0.5,\
            'status': 'success',\
            'tokens_used': 150\
        \}\
    )}