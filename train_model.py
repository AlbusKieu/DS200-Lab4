from pyspark.sql import SparkSession
import tensorflow as tf
import numpy as np
from PIL import Image
import os
import sys

# Fix UnicodeEncodeError
sys.stdout.reconfigure(encoding='utf-8')

CLASS_NAMES = ['cloudy', 'desert', 'green_area', 'water']
CLASS_INDEX = {name: i for i, name in enumerate(CLASS_NAMES)}

def preprocess_image(img_path):
    img = Image.open(img_path).resize((64, 64)).convert('RGB')
    return np.array(img) / 255.0

def load_images_numpy(folder):
    images = []
    labels = []
    for label in os.listdir(folder):
        label_folder = os.path.join(folder, label)
        if not os.path.isdir(label_folder): continue
        for fname in os.listdir(label_folder):
            if not fname.endswith('.jpg'): continue
            img = preprocess_image(os.path.join(label_folder, fname))
            images.append(img)
            labels.append(CLASS_INDEX[label])
    return np.array(images), np.array(labels)

def train_model(X, y):
    # Use Input layer to define input shape
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(64, 64, 3)),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(len(CLASS_NAMES), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=5, validation_split=0.2)
    model.save("satellite_model.h5")

if __name__ == '__main__':
    spark = SparkSession.builder.appName("SatelliteClassification").getOrCreate()
    img_folder = 'received_data'
    images, labels = load_images_numpy(img_folder)
    train_model(images, labels)
    spark.stop()