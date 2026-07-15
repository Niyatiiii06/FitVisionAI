import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

# ======================================
# Load Dataset
# ======================================

df = pd.read_csv("data/dataset/squat_dataset.csv")

print("=" * 50)
print("Dataset Shape")
print("=" * 50)
print(df.shape)

X = df.drop(columns=["exercise", "label"])
y = df["label"]

# ======================================
# Label Encoding
# ======================================

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# ======================================
# Train Test Split
# ======================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ======================================
# Feature Scaling
# ======================================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ======================================
# ANN Model
# ======================================

model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(32, activation="relu"),
    Dense(16, activation="relu"),
    Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

history = model.fit(
    X_train,
    y_train,
    epochs=50,
    batch_size=16,
    validation_data=(X_test, y_test),
    callbacks=[early_stop]
)

# ======================================
# Evaluation
# ======================================

loss, accuracy = model.evaluate(X_test, y_test)

print("\nAccuracy :", accuracy)
print("Loss :", loss)

predictions = (model.predict(X_test) > 0.5).astype(int)

print("\nConfusion Matrix")
print(confusion_matrix(y_test, predictions))

print("\nClassification Report")
print(classification_report(y_test, predictions))

# ======================================
# Save Model
# ======================================

os.makedirs("models", exist_ok=True)

model.save("models/squat_ann.keras")

joblib.dump(
    scaler,
    "models/squat_scaler.pkl"
)

joblib.dump(
    label_encoder,
    "models/squat_label_encoder.pkl"
)

print("\nModel Saved")
print("Scaler Saved")
print("Label Encoder Saved")

# ======================================
# Accuracy Plot
# ======================================

plt.figure(figsize=(8,5))

plt.plot(history.history["accuracy"], label="Train")
plt.plot(history.history["val_accuracy"], label="Validation")

plt.title("Squat ANN Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.legend()

plt.savefig("models/accuracy.png")

# ======================================
# Loss Plot
# ======================================

plt.figure(figsize=(8,5))

plt.plot(history.history["loss"], label="Train")
plt.plot(history.history["val_loss"], label="Validation")

plt.title("Squat ANN Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.legend()

plt.savefig("models/loss.png")

plt.show()