import tensorflow as tf
import numpy as np
# from tensorflow.keras.preprocessing import image
from PIL import Image
import os

class MLModelHandler:
    def __init__(self, model_path=None):
        """
        Initialize ML model for melanoma detection
        
        Args:
            model_path (str, optional): Path to pre-trained model
        """
        if model_path is None:
            # Get absolute path to models directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'models', 'melanoma_model.h5')
        
        try:
            self.model = tf.keras.models.load_model(model_path)
            print(f"✅ Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def preprocess_image(self, img_path):
        """
        Preprocess image for model prediction
        
        Args:
            img_path (str): Path to image file
        
        Returns:
            np.array: Preprocessed image array
        """
        try:
            # img = image.load_img(img_path, target_size=(224, 224))
            # img_array = image.img_to_array(img)
            # img_array = np.expand_dims(img_array, axis=0) / 255.0
            # return img_array
            with Image.open(img_path) as img:
                img = img.resize((224, 224))
                img_array = np.array(img)
                img_array = img_array.astype('float32') / 255.0
                return np.expand_dims(img_array, axis=0)
        except Exception as e:
            print(f"Image preprocessing error: {e}")
            return None
    
    def predict(self, img_path):
        """
        Predict melanoma probability
        
        Args:
            img_path (str): Path to image file
        
        Returns:
            float: Probability of melanoma
        """
        # if self.model is None:
        #     raise ValueError("Model not loaded")
        
        # preprocessed_img = self.preprocess_image(img_path)
        
        # if preprocessed_img is None:
        #     raise ValueError("Image preprocessing failed")
        
        # prediction = self.model.predict(preprocessed_img)
        # return float(prediction[0][0])
        if self.model is None:
            raise ValueError("Model not initialized")
        
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image not found: {img_path}")
            
        try:
            preprocessed_img = self.preprocess_image(img_path)
            prediction = self.model.predict(preprocessed_img, verbose=0)
            return float(prediction[0][0])
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")