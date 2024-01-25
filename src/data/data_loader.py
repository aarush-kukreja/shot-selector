import pandas as pd
import json
from pathlib import Path
from src.utils.logger import setup_logger  # Updated import

logger = setup_logger(__name__)

class DataLoader:
    def __init__(self, config):
        self.config = config
        self.data_dir = Path(config.get('data_dir', 'data'))
        
    def load_raw_data(self, file_path):
        """Load raw data from specified path"""
        logger.info(f"Loading raw data from {file_path}")
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    return pd.DataFrame(json.load(f))
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
            
    def save_processed_data(self, data, file_name):
        """Save processed data to the processed directory"""
        processed_dir = self.data_dir / 'processed'
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = processed_dir / file_name
        data.to_csv(file_path, index=False)
        logger.info(f"Saved processed data to {file_path}")
        
    def load_training_data(self):
        """Load training data with prompts and their optimal strategies"""
        training_data_path = self.data_dir / 'processed' / 'training_data.csv'
        if not training_data_path.exists():
            logger.error("Training data not found")
            raise FileNotFoundError("Training data file not found")
            
        return pd.read_csv(training_data_path)
