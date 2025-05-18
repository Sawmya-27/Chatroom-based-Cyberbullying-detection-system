import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

# Load the correct CSV file path
csv_path = 'cyberbullying_dataset_v2/cyberbullying_detection_dataset.csv'  # or provide absolute path if needed
df = pd.read_csv(csv_path)
df.columns = df.columns.str.strip()

# Convert label column to string (fixes the error)
df['label'] = df['label'].astype(str)

# Make sure image paths are correct
df['filename'] = df['filename'].apply(lambda x: os.path.join(os.path.dirname(csv_path), x))


# Image preprocessing
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = datagen.flow_from_dataframe(
    dataframe=df,
    x_col='filename',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='training',
    shuffle=True
)

val_data = datagen.flow_from_dataframe(
    dataframe=df,
    x_col='filename',
    y_col='label',
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary',
    subset='validation',
    shuffle=True
)

# Build the MobileNetV2 model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(64, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer=Adam(1e-4), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_data, validation_data=val_data, epochs=5)

# Save the trained model
os.makedirs('models', exist_ok=True)
model.save('models/image_model.h5')
print("✅ Model saved to models/image_model.h5")
