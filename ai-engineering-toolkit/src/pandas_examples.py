{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import pandas as pd\
import numpy as np\
from typing import List, Dict\
\
class DataAnalyzer:\
    def __init__(self, data_path: str = None):\
        self.df = pd.read_csv(data_path) if data_path else None\
    \
    def load_data(self, data: List[Dict]):\
        """Load data from list of dictionaries"""\
        self.df = pd.DataFrame(data)\
    \
    def process_ai_results(self, results_df: pd.DataFrame):\
        """Process AI model results"""\
        # Basic statistics\
        stats = \{\
            'mean_confidence': results_df['confidence'].mean(),\
            'success_rate': (results_df['status'] == 'success').mean(),\
            'avg_latency': results_df['latency'].mean()\
        \}\
        \
        # Time-based analysis\
        if 'timestamp' in results_df.columns:\
            results_df['timestamp'] = pd.to_datetime(results_df['timestamp'])\
            hourly_stats = results_df.set_index('timestamp').resample('H').agg(\{\
                'confidence': 'mean',\
                'latency': 'mean',\
                'status': lambda x: (x == 'success').mean()\
            \})\
        \
        return stats, hourly_stats\
    \
    def prepare_training_data(self, text_column: str, label_column: str):\
        """Prepare data for AI model training"""\
        # Basic text preprocessing\
        processed_df = self.df.copy()\
        processed_df[text_column] = processed_df[text_column].fillna('')\
        \
        # Create feature matrices\
        X = processed_df[text_column].values\
        y = processed_df[label_column].values\
        \
        return X, y\
    \
    def analyze_model_performance(self, predictions: List, actuals: List):\
        """Analyze model performance metrics"""\
        results = pd.DataFrame(\{\
            'predicted': predictions,\
            'actual': actuals\
        \})\
        \
        # Calculate metrics\
        accuracy = (results['predicted'] == results['actual']).mean()\
        \
        # Create confusion matrix\
        confusion_matrix = pd.crosstab(\
            results['actual'], \
            results['predicted'], \
            normalize='index'\
        )\
        \
        return \{\
            'accuracy': accuracy,\
            'confusion_matrix': confusion_matrix\
        \}\
\
# Usage example\
if __name__ == "__main__":\
    # Create sample data\
    sample_data = [\
        \{'text': 'Sample 1', 'label': 'positive', 'confidence': 0.9\},\
        \{'text': 'Sample 2', 'label': 'negative', 'confidence': 0.8\},\
    ]\
    \
    analyzer = DataAnalyzer()\
    analyzer.load_data(sample_data)\
    \
    # Process results\
    results_df = pd.DataFrame(\{\
        'confidence': [0.9, 0.8, 0.7],\
        'status': ['success', 'success', 'failure'],\
        'latency': [0.1, 0.2, 0.3],\
        'timestamp': pd.date_range(start='2024-01-01', periods=3)\
    \})\
    \
    stats, hourly_stats = analyzer.process_ai_results(results_df)\
    print("Performance Stats:", stats)}