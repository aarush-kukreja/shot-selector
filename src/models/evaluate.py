from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from src.data.data_loader import DataLoader
from src.utils.logger import setup_logger
from src.utils.helpers import load_config
import joblib
from pathlib import Path
import json

logger = setup_logger(__name__)

def evaluate_model(config_path='src/config/config.yaml'):
    """Evaluate the trained model's performance"""
    logger.info("Starting model evaluation")
    
    try:
        # Load configuration
        config = load_config(config_path)
        
        # Load test data
        data_loader = DataLoader(config)
        test_data = data_loader.load_training_data()
        
        # Load model
        model_path = Path(config['model']['save_dir']) / f"{config['model']['name']}.joblib"
        model = joblib.load(model_path)
        
        # Make predictions
        X_test = test_data[['prompt_text']]
        y_true = test_data['strategy']
        
        predictions = []
        for _, row in X_test.iterrows():
            result = model.predict(row['prompt_text'])
            predictions.append(result['strategy'])
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, 
            predictions, 
            average='weighted'
        )
        
        # Prepare evaluation results
        results = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        
        # Save results
        results_dir = Path(config['model']['save_dir']) / 'evaluation'
        results_dir.mkdir(parents=True, exist_ok=True)
        results_path = results_dir / 'evaluation_results.json'
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=4)
        
        logger.info(f"Evaluation results saved to {results_path}")
        return results
        
    except Exception as e:
        logger.error(f"Error during model evaluation: {str(e)}")
        raise

if __name__ == "__main__":
    results = evaluate_model()
    print("\nEvaluation Results:")
    print(f"Accuracy: {results['accuracy']:.2%}")
    print(f"Precision: {results['precision']:.2%}")
    print(f"Recall: {results['recall']:.2%}")
    print(f"F1 Score: {results['f1_score']:.2%}")
