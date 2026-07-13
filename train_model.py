import pandas as pd
import os
import matplotlib.pyplot as plt
import joblib

# Load dataset
df = pd.read_csv("data/dataset/squat_dataset.csv")
print('='*50)
print('Dataset Shape:')
print('='*50)
print(df.shape)

X= df.drop(columns=['exercise','label'])
y= df['label']
print('\nFeature Shape:', X.shape)
print('Label Shape:', y.shape)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

encoder= LabelEncoder()
y= encoder.fit_transform(y)
X_train, X_test, y_train, y_test= train_test_split(X, y,
test_size=0.2, random_state=42, stratify=y)

scaler= StandardScaler()
X_train= scaler.fit_transform(X_train)
X_test= scaler.transform(X_test)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

model= Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
history= model.fit(
    X_train,y_train,
    epochs=50,
    batch_size=16,
    validation_data=(X_test,y_test)
)
loss, accuracy = model.evaluate(X_test, y_test)

print("\nTest Accuracy:", accuracy)
print("Test Loss:", loss)

os.makedirs("models", exist_ok=True)

model.save("models/squat_classifier.keras")
print("\nModel Saved Successfully!")

# Save the scaler
joblib.dump(scaler, "models/scaler.pkl")
print("Scaler Saved Successfully!")

plt.figure(figsize=(8,5))

plt.plot(history.history["accuracy"], label="Training Accuracy")
plt.plot(history.history["val_accuracy"], label="Validation Accuracy")

plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.legend()

plt.savefig("models/accuracy.png")
plt.show()

plt.figure(figsize=(8,5))

plt.plot(history.history["loss"], label="Training Loss")
plt.plot(history.history["val_loss"], label="Validation Loss")

plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.legend()

plt.savefig("models/loss.png")
plt.show()