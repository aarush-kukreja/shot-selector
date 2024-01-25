import argparse
import joblib
from pathlib import Path
from src.models.model import PromptStrategyModel
from src.utils.logger import setup_logger
from src.utils.helpers import load_config

logger = setup_logger(__name__)

class CLI:
    def __init__(self):
        self.config = load_config('src/config/config.yaml')
        self.model = self._load_or_create_model()
        self.setup_commands()
        
    def _load_or_create_model(self):
        """Load trained model if exists, otherwise create new one"""
        model_path = Path(self.config['model']['save_dir']) / f"{self.config['model']['name']}.joblib"
        if model_path.exists():
            logger.info(f"Loading trained model from {model_path}")
            return joblib.load(model_path)
        else:
            logger.info("No trained model found, creating new model")
            return PromptStrategyModel(self.config)
    
    def setup_commands(self):
        """Set up CLI command parser"""
        self.parser = argparse.ArgumentParser(
            description='Shot-Selector'
        )
        
        self.parser.add_argument(
            '--prompt',
            type=str,
            help='Input prompt text for strategy prediction'
        )
        
        self.parser.add_argument(
            '--train',
            action='store_true',
            help='Train the model with available data'
        )
        
        self.parser.add_argument(
            '--evaluate',
            action='store_true',
            help='Evaluate model performance'
        )
    
    def run(self):
        """Run the CLI application"""
        args = self.parser.parse_args()
        
        if args.prompt:
            self._handle_prediction(args.prompt)
        elif args.train:
            self._handle_training()
        elif args.evaluate:
            self._handle_evaluation()
        else:
            self._interactive_mode()
    
    def _handle_prediction(self, prompt_text):
        """Handle prediction for a single prompt"""
        try:
            # Check if model needs training
            if not hasattr(self.model, 'vectorizer') or not hasattr(self.model.vectorizer, 'vocabulary_'):
                logger.warning("Model not trained, training now...")
                self._handle_training()
                
            result = self.model.predict(prompt_text)
            self._display_result(result)
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            print(f"Error making prediction: {str(e)}")
    
    def _handle_training(self):
        """Handle model training"""
        try:
            from src.models.train import train_model
            self.model, _ = train_model(config_path='src/config/config.yaml')
            print("Model training completed successfully")
        except Exception as e:
            logger.error(f"Training error: {str(e)}")
            print(f"Error during training: {str(e)}")
    
    def _handle_evaluation(self):
        """Handle model evaluation"""
        try:
            from src.models.evaluate import evaluate_model
            result = evaluate_model()
            print("\nModel Evaluation Results:")
            print(f"Accuracy: {result['accuracy']:.2%}")
            print(f"F1 Score: {result['f1_score']:.2%}")
        except Exception as e:
            logger.error(f"Evaluation error: {str(e)}")
            print(f"Error during evaluation: {str(e)}")
    
    def _interactive_mode(self):
        """Run interactive mode for prompt input"""
        print("Welcome to the Prompting Strategy Selector")
        print("Enter 'quit' to exit")
        
        while True:
            prompt = input("\nEnter your prompt: ").strip()
            
            if prompt.lower() == 'quit':
                break
                
            if prompt:
                self._handle_prediction(prompt)
    
    def _display_result(self, result):
        """Display prediction results"""
        print("\nPrediction Results:")
        print("-" * 50)
        strategy_mapping = {
            0: "Zero-shot",
            1: "One-shot",
            2: "Two-shot",
            3: "Three-shot"
        }
        strategy_text = strategy_mapping[result['strategy']]
        print(f"Recommended Strategy: {strategy_text}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Explanation: {result['explanation']}")
        print("-" * 50)
