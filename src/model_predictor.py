import joblib
import pandas as pd
import tensorflow as tf
import numpy as np


class ModelPredictor:

    def __init__(self):

        # Load trained model
        self.model = tf.keras.models.load_model(
            "models/squat_classifier.keras"
        )

        # Load scaler
        self.scaler = joblib.load(
            "models/scaler.pkl"
        )

    def predict(self, landmarks):

        # Extract x and y coordinates
        features = []

        for landmark in landmarks:
            features.extend([
                landmark.x,
                landmark.y
            ])

        # Create DataFrame with original feature names
        feature_df = pd.DataFrame(
            [features],
            columns=self.scaler.feature_names_in_
        )

        # Scale features
        scaled_features = self.scaler.transform(feature_df)

        # TensorFlow prefers float32
        scaled_features = np.asarray(
            scaled_features,
            dtype=np.float32
        )

        # Predict
        probability = float(
            self.model.predict(
                scaled_features,
                verbose=0
            )[0][0]
        )

        if probability >= 0.5:
            return "UP", probability * 100

        return "DOWN", (1 - probability) * 100