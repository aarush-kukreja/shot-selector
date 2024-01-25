import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src.utils.logger import setup_logger  # Updated import

logger = setup_logger(__name__)

class DataPreprocessor:
    def __init__(self, config):
        self.config = config
        
    def preprocess(self, data):
        """Preprocess the input data"""
        logger.info("Starting data preprocessing")
        
        # Clean text
        data['prompt_text'] = data['prompt_text'].apply(self._clean_text)
        
        # Add feature columns
        data['prompt_length'] = data['prompt_text'].apply(lambda x: len(x.split()))
        data['complexity_score'] = data['prompt_text'].apply(self._calculate_complexity)
        
        # Convert strategy labels to numeric
        strategy_mapping = {
            'zero-shot': 0,
            'one-shot': 1,
            'two-shot': 2,
            'three-shot': 3
        }
        
        data['strategy'] = data['optimal_strategy'].map(strategy_mapping)
        
        logger.info("Data preprocessing completed")
        return data
        
    def _clean_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
        
    def _calculate_complexity(self, text):
        """Calculate complexity score for a prompt"""
        words = text.split()
        avg_word_length = np.mean([len(word) for word in words])
        sentence_count = text.count('.') + text.count('?') + text.count('!')
        
        if sentence_count == 0:
            sentence_count = 1
            
        avg_sentence_length = len(words) / sentence_count
        
        # Normalize scores
        complexity = (avg_word_length * 0.5) + (avg_sentence_length * 0.5)
        return complexity
        
    def split_data(self, data, test_size=0.2, random_state=42):
        """Split data into training and testing sets"""
        return train_test_split(
            data, 
            test_size=test_size, 
            random_state=random_state,
            stratify=data['strategy']
        )
