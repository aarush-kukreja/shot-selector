import pytest
import numpy as np
from src.models.model import PromptStrategyModel
from src.utils.helpers import load_config

@pytest.fixture
def model():
    config = load_config('src/config/config.yaml')
    return PromptStrategyModel(config)

@pytest.fixture
def sample_data():
    return {
        'prompt_text': [
            "What is the capital of France?",
            "Explain the process of photosynthesis step by step.",
            "Calculate 2 + 2."
        ],
        'strategy': [0, 1, 0]  # 0 for one-shot, 1 for chain-of-thought
    }

def test_model_initialization(model):
    assert model is not None
    assert model.vectorizer is not None
    assert model.model is not None

def test_feature_extraction(model):
    text = "This is a sample prompt text."
    features = model.extract_features(text)
    
    assert 'length' in features
    assert 'avg_word_length' in features
    assert features['length'] == 6  # number of words
    assert isinstance(features['avg_word_length'], float)

def test_prediction_format(model, sample_data):
    # Train the model with sample data
    X = {'prompt_text': sample_data['prompt_text']}
    y = sample_data['strategy']
    model.fit(X, y)
    
    # Test prediction
    result = model.predict("What is the capital of Spain?")
    
    assert isinstance(result, dict)
    assert 'strategy' in result
    assert 'confidence' in result
    assert 'explanation' in result
    assert isinstance(result['confidence'], float)
    assert 0 <= result['confidence'] <= 1

def test_explanation_generation(model):
    # Test one-shot explanation
    one_shot_exp = model._generate_explanation('one-shot', 0.9)
    assert "One-shot prompting is recommended" in one_shot_exp
    assert "high confidence" in one_shot_exp
    
    # Test chain-of-thought explanation
    cot_exp = model._generate_explanation('chain-of-thought', 0.6)
    assert "Chain-of-thought reasoning is recommended" in cot_exp
    assert "moderate confidence" in cot_exp
