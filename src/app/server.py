from flask import Flask, request, jsonify
from src.models.model import PromptStrategyModel
from src.utils.logger import setup_logger
from src.utils.helpers import load_config
import joblib
from pathlib import Path

logger = setup_logger(__name__)
app = Flask(__name__)

# Load configuration and model at startup
config = load_config('src/config/config.yaml')
model_path = Path(config['model']['save_dir']) / f"{config['model']['name']}.joblib"
model = joblib.load(model_path)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint for making predictions"""
    try:
        data = request.json
        
        if not data or 'prompt' not in data:
            return jsonify({
                "error": "Missing 'prompt' in request body"
            }), 400
            
        prompt_text = data['prompt']
        result = model.predict(prompt_text)
        
        return jsonify({
            "status": "success",
            "prediction": {
                "strategy": "one-shot" if result['strategy'] == 0 else "chain-of-thought",
                "confidence": result['confidence'],
                "explanation": result['explanation']
            }
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Endpoint for batch predictions"""
    try:
        data = request.json
        
        if not data or 'prompts' not in data:
            return jsonify({
                "error": "Missing 'prompts' in request body"
            }), 400
            
        prompts = data['prompts']
        results = []
        
        for prompt in prompts:
            result = model.predict(prompt)
            results.append({
                "prompt": prompt,
                "strategy": "one-shot" if result['strategy'] == 0 else "chain-of-thought",
                "confidence": result['confidence'],
                "explanation": result['explanation']
            })
            
        return jsonify({
            "status": "success",
            "predictions": results
        })
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
