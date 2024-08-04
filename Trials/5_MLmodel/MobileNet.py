import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Conv2D, BatchNormalization, ReLU, GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# Load MobileNetV2 without the top layer
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Add custom layers on top of MobileNetV2
x = base_model.output
x = Conv2D(512, kernel_size=(3, 3), padding='same')(x)
x = BatchNormalization()(x)
x = ReLU()(x)

# Add more convolutional layers if needed
x = Conv2D(256, kernel_size=(3, 3), padding='same')(x)
x = BatchNormalization()(x)
x = ReLU()(x)

# Pooling layer to reduce dimensions
x = GlobalAveragePooling2D()(x)

# Fully connected layer
x = Dense(1024, activation='relu')(x)

# Final layer for detection
num_classes = 1  # For binary classification (sheet vs. no sheet)
predictions = Conv2D(num_classes, kernel_size=(1, 1), activation='sigmoid')(x)

# Create the complete model
model = Model(inputs=base_model.input, outputs=predictions)

datagen = ImageDataGenerator(
    rescale=1.0/255,  # Normalize pixel values to [0, 1]
    validation_split=0.2  # Split data into training and validation
)

train_generator = datagen.flow_from_directory(
    'path/to/dataset',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    'path/to/dataset',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)


model.compile(optimizer=Adam(lr=1e-4), loss='binary_crossentropy', metrics=['accuracy'])