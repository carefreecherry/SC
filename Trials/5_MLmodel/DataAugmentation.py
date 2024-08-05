import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array

# Create an ImageDataGenerator object with desired augmentations
datagen = ImageDataGenerator(
    rotation_range=90,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Load and augment an image
img_path = 'images/2.jpeg'
img = cv2.imread(img_path)
x = img_to_array(img)  # Convert image to numpy array
x = x.reshape((1,) + x.shape)  # Reshape image array

# Generate and save augmented images
i = 0
for batch in datagen.flow(x, batch_size=1, save_to_dir='Trials/5_MLmodel/preview', save_prefix='frame_2', save_format='jpeg'):
    i += 1
    if i > 1:  # Generate 20 augmented images per original image
        break
