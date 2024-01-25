from src.data.data_loader import DataLoader
from src.data.data_preprocessing import DataPreprocessor
from src.models.model import PromptStrategyModel
from src.utils.logger import setup_logger
from src.utils.helpers import load_config
import joblib
from pathlib import Path

logger = setup_logger(__name__)

def train_model(config_path='src/config/config.yaml'):
    """Train the prompt strategy selection model"""
    logger.info("Starting model training pipeline")
    
    # Load configuration
    config = load_config(config_path)
    
    try:
        # Initialize components
        data_loader = DataLoader(config)
        preprocessor = DataPreprocessor(config)
        model = PromptStrategyModel(config)
        
        # Load and preprocess data
        raw_data = data_loader.load_raw_data(config['data']['training_data_path'])
        processed_data = preprocessor.preprocess(raw_data)
        
        # Split data
        train_data, test_data = preprocessor.split_data(processed_data)
        
        # Train model
        X_train = train_data[['prompt_text']]
        y_train = train_data['strategy']
        model.fit(X_train, y_train)
        
        # Save model
        model_dir = Path(config['model']['save_dir'])
        model_dir.mkdir(parents=True, exist_ok=True)
        model_path = model_dir / f"{config['model']['name']}.joblib"
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Save preprocessed data for evaluation
        data_loader.save_processed_data(test_data, 'test_data.csv')
        
        return model, test_data
        
    except Exception as e:
        logger.error(f"Error during model training: {str(e)}")
        raise

if __name__ == "__main__":
    train_model()
