import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Dropout,
    BatchNormalization
)
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint
)

# ------------------------------------
# Load Dataset
# ------------------------------------

df = pd.read_csv("data/dataset/pushup_dataset.csv")

print("\nDataset Shape:", df.shape)

X = df.drop("label", axis=1)
y = df["label"]

# ------------------------------------
# Label Encoding
# ------------------------------------

encoder = LabelEncoder()

y = encoder.fit_transform(y)

# ------------------------------------
# Train Test Split
# ------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y

)

# ------------------------------------
# Feature Scaling
# ------------------------------------

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ------------------------------------
# ANN
# ------------------------------------

model = Sequential([

    Dense(256, activation="relu", input_shape=(132,)),
    BatchNormalization(),
    Dropout(0.30),

    Dense(128, activation="relu"),
    BatchNormalization(),
    Dropout(0.30),

    Dense(64, activation="relu"),

    Dense(2, activation="softmax")

])

model.compile(

    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]

)

# ------------------------------------
# Callbacks
# ------------------------------------

early = EarlyStopping(

    monitor="val_loss",
    patience=15,
    restore_best_weights=True

)

checkpoint = ModelCheckpoint(

    "models/pushup_ann.keras",
    save_best_only=True

)

# ------------------------------------
# Train
# ------------------------------------

history = model.fit(

    X_train,
    y_train,

    validation_split=0.20,

    epochs=100,

    batch_size=32,

    callbacks=[early, checkpoint],

    verbose=1

)

# ------------------------------------
# Evaluation
# ------------------------------------

pred = model.predict(X_test)

pred = np.argmax(pred, axis=1)

print("\nAccuracy")
print(accuracy_score(y_test, pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, pred))

print("\nClassification Report")
print(classification_report(
    y_test,
    pred,
    target_names=encoder.classes_
))

# ------------------------------------
# Save Preprocessing
# ------------------------------------

joblib.dump(
    scaler,
    "models/pushup_scaler.pkl"
)

joblib.dump(
    encoder,
    "models/pushup_label_encoder.pkl"
)

print("\nModel Saved Successfully!")