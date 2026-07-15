import joblib
import numpy as np
import tensorflow as tf


class ModelPredictor:

    def __init__(self, exercise):

        self.exercise = exercise

        if exercise == "squat":

            self.model = tf.keras.models.load_model(
                "models/squat_ann.keras"
            )

            self.scaler = joblib.load(
                "models/squat_scaler.pkl"
            )

        elif exercise == "pushup":

            self.model = tf.keras.models.load_model(
                "models/pushup_ann.keras"
            )

            self.scaler = joblib.load(
                "models/pushup_scaler.pkl"
            )

            self.encoder = joblib.load(
                "models/pushup_label_encoder.pkl"
            )

        else:
            raise ValueError(
                f"Unsupported exercise: {exercise}"
            )

    def predict(self, landmarks):

        sample = []

        for point in landmarks:

            sample.extend([
                point.x,
                point.y,
                point.z,
                point.visibility
            ])

        sample = np.array(sample).reshape(1, -1)

        sample = self.scaler.transform(sample)

        prediction = self.model.predict(
            sample,
            verbose=0
        )[0]

        # -----------------------------
        # Squat (Binary Sigmoid)
        # -----------------------------
        if self.exercise == "squat":

            probability = float(prediction[0])

            if probability >= 0.5:
                state = "UP"
                confidence = probability * 100
            else:
                state = "DOWN"
                confidence = (1 - probability) * 100

        # -----------------------------
        # Push-up (Softmax)
        # -----------------------------
        else:

            index = np.argmax(prediction)

            state = self.encoder.inverse_transform(
                [index]
            )[0]

            confidence = float(prediction[index] * 100)

        return state, confidence