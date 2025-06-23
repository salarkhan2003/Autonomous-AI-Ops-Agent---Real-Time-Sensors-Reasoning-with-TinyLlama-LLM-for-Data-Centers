import pandas as pd
import numpy as np
import random
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Set model path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "anomaly_model.tflite")


def train_model():
    # Generate synthetic data
    data = []
    for _ in range(1000):
        temp = random.uniform(20, 40)
        voltage = random.uniform(3.3, 5.0)
        current = random.uniform(100, 1000)
        anomaly = 1 if temp > 35 or current > 800 else 0
        data.append([temp, voltage, current, anomaly])
    df = pd.DataFrame(data, columns=["temp", "voltage", "current", "anomaly"])
    df.to_csv(os.path.join(BASE_DIR, "data", "data_center_data.csv"), index=False)

    # Train decision tree
    X = df[["temp", "voltage", "current"]]
    y = df["anomaly"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X_train, y_train)
    print(f"Accuracy: {model.score(X_test, y_test)}")

    # Train neural network for TensorFlow Lite
    keras_model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(3,)),  # Explicit Input layer
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])
    keras_model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    keras_model.fit(X_train, y_train, epochs=10)

    # Convert to TensorFlow Lite
    converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
    tflite_model = converter.convert()

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        f.write(tflite_model)
    print(f"Model saved to: {MODEL_PATH}")


def detect_anomaly(data):
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_data = np.array([[data["temp"], data["voltage"], data["current"]]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()
    anomaly = interpreter.get_tensor(output_details[0]["index"])
    anomaly_type = "overheating" if data["temp"] > 35 else "current_spike" if data["current"] > 800 else None
    return anomaly_type if anomaly[0] > 0.5 else None


if __name__ == "__main__":
    train_model()

    # Example of using detect_anomaly
    sample_data = {
        "temp": 36,  # Example temperature
        "voltage": 4.0,  # Example voltage
        "current": 850  # Example current
    }
    anomaly_type = detect_anomaly(sample_data)
    print(f"Detected anomaly type: {anomaly_type}")
