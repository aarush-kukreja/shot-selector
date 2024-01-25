from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from src.utils.logger import setup_logger  # Updated import

logger = setup_logger(__name__)

class PromptStrategyModel:
    def __init__(self, config):
        self.config = config
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english'
        )
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        
    def extract_features(self, text):
        """Extract features from prompt text"""
        features = np.zeros((1, 2))  # Create a 2D array for features
        features[0, 0] = len(text.split())  # Length
        features[0, 1] = np.mean([len(word) for word in text.split()])  # Average word length
        return features
        
    def fit(self, X, y):
        """Train the model"""
        logger.info("Training prompt strategy model")
        # Transform text to TF-IDF features
        X_tfidf = self.vectorizer.fit_transform(X['prompt_text'])
        
        # Extract additional features for all texts
        additional_features = np.vstack([
            self.extract_features(text)[0] for text in X['prompt_text']
        ])
        
        # Combine features
        X_combined = np.hstack([X_tfidf.toarray(), additional_features])
        
        # Train model
        self.model.fit(X_combined, y)
        logger.info("Model training completed")
        
    def predict(self, prompt_text):
        """Predict the best prompting strategy"""
        if self.model is None:
            raise ValueError("Model not trained yet")
            
        # Transform text
        X_tfidf = self.vectorizer.transform([prompt_text])
        
        # Extract additional features
        additional_features = self.extract_features(prompt_text)
        
        # Combine features
        X_combined = np.hstack([X_tfidf.toarray(), additional_features])
        
        # Make prediction
        strategy = self.model.predict(X_combined)[0]
        confidence = np.max(self.model.predict_proba(X_combined)[0])
        
        return {
            'strategy': strategy,
            'confidence': confidence,
            'explanation': self._generate_explanation(strategy, confidence)
        }
        
    def _generate_explanation(self, strategy, confidence):
        """Generate human-readable explanation for the prediction"""
        strategy_mapping = {
            0: "Zero-shot",
            1: "One-shot",
            2: "Two-shot",
            3: "Three-shot"
        }
        
        base_explanation = f"{strategy_mapping[strategy]} prompting is recommended"
        confidence_level = "high" if confidence > 0.8 else "moderate" if confidence > 0.6 else "low"
        
        return f"{base_explanation} with {confidence_level} confidence ({confidence:.2%})"
