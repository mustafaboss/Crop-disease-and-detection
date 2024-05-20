from PIL import Image
import tensorflow as tf
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

# Load the retrained model
retrained_model = tf.keras.models.load_model('retrained_model.h5')

def preprocess_image(image):
    # Open the image using Pillow
    img = Image.open(image)

    # Convert the image to a NumPy array
    img_array = tf.keras.preprocessing.image.img_to_array(img)

    # Resize the image to the input size expected by the retrained model
    target_size = (224, 224)
    img_array = tf.image.resize(img_array, size=target_size)

    # Expand the dimensions to match the expected input shape (batch size of 1)
    img_array = tf.expand_dims(img_array, 0)

    # Preprocess the image using the retrained model's preprocessing function
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # Predict disease class probabilities using the retrained model
    predictions = retrained_model.predict(img_array)

    # Assuming your model output is softmax activation, get the predicted class index
    predicted_class_index = tf.argmax(predictions[0]).numpy()

    # Decode the predicted class index to get the class label
    classes = [
        'Tomato_Septoria_leaf_spot',
        'Tomato_Spider_mites_Two_spotted_spider_mite'
    ]
    disease_type = classes[predicted_class_index]

    # Get the confidence score for the predicted class
    confidence = predictions[0][predicted_class_index]

    # Convert the NumPy array back to a PIL Image
    processed_img = tf.keras.preprocessing.image.array_to_img(img_array[0])

    # Save the processed image to a BytesIO buffer
    buffer = BytesIO()
    processed_img.save(buffer, format='JPEG')

    # Create an InMemoryUploadedFile from the buffer
    return InMemoryUploadedFile(buffer, None, 'image.jpg', 'image/jpeg', buffer.tell(), None), disease_type, confidence
