"""
Mock ML model for meat inspection.
In production, replace with actual trained model (TensorFlow, PyTorch, etc.)
"""

import random
import time
from PIL import Image
import io
import numpy as np

class MeatInspectionModel:
    """Mock ML model simulating meat quality detection"""
    
    MEAT_TYPES = ['chicken', 'beef', 'mutton', 'fish', 'pork']
    FRESHNESS_LEVELS = ['fresh', 'moderate', 'spoiled']
    
    def __init__(self, model_version='1.0'):
        self.model_version = model_version
        self.is_loaded = True
    
    def _analyze_image_features(self, image_bytes):
        """
        Analyze image features (color, texture, etc.)
        This is a mock implementation that reads image dimensions and basic stats
        """
        try:
            img = Image.open(io.BytesIO(image_bytes))
            img_array = np.array(img)
            
            # Fake feature extraction based on image properties
            # In reality, this would use CNN feature extraction
            mean_color = np.mean(img_array, axis=(0, 1))
            variance = np.var(img_array)
            
            return {
                'mean_color': mean_color,
                'variance': variance,
                'shape': img_array.shape
            }
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {}
    
    def predict(self, image_bytes):
        """
        Run inference on image and return predictions
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            dict with keys: meat_type, meat_confidence, freshness, freshness_confidence
        """
        start_time = time.time()
        
        try:
            # Extract mock features
            features = self._analyze_image_features(image_bytes)
            
            # Deterministic random based on image data hash (reproducible)
            seed = hash(image_bytes[:100]) % (2**32)
            random.seed(seed)
            
            # Predict meat type
            meat_type = random.choice(self.MEAT_TYPES)
            
            # Confidence varies: higher confidence for "chicken" and "beef"
            if meat_type in ['chicken', 'beef']:
                meat_confidence = 0.78 + random.random() * 0.18
            else:
                meat_confidence = 0.65 + random.random() * 0.25
            
            # Predict freshness
            freshness = random.choice(self.FRESHNESS_LEVELS)
            
            # Confidence varies by freshness
            if freshness == 'fresh':
                freshness_confidence = 0.80 + random.random() * 0.15
            elif freshness == 'moderate':
                freshness_confidence = 0.60 + random.random() * 0.25
            else:  # spoiled
                freshness_confidence = 0.70 + random.random() * 0.20
            
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            return {
                'meat_type': meat_type,
                'meat_confidence': min(0.99, meat_confidence),
                'freshness': freshness,
                'freshness_confidence': min(0.99, freshness_confidence),
                'processing_time_ms': processing_time_ms,
                'model_version': self.model_version
            }
        
        except Exception as e:
            print(f"Prediction error: {e}")
            # Fallback prediction
            return {
                'meat_type': random.choice(self.MEAT_TYPES),
                'meat_confidence': 0.65,
                'freshness': random.choice(self.FRESHNESS_LEVELS),
                'freshness_confidence': 0.70,
                'processing_time_ms': 0,
                'model_version': self.model_version
            }

# Global model instance
_model = None

def get_model():
    """Get or initialize the ML model"""
    global _model
    if _model is None:
        _model = MeatInspectionModel()
    return _model
