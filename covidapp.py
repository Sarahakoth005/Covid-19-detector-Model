pip install streamlit

import streamlit as st
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img


model = load_model('path_to_save_model')


def preprocess_image(image):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    resized_image = cv2.resize(gray, (224, 224))
   
    normalized_image = resized_image / 255.0
    
    batched_image = np.expand_dims(normalized_image, axis=0)
    return batched_image

def main():
    st.title('COVID-19 X-ray Image Prediction')
    st.write('Upload an X-ray image and get the COVID-19 prediction.')

    uploaded_file = st.file_uploader("Choose an X-ray image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        
        image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        st.image(image, channels="BGR")

    
        preprocessed_image = preprocess_image(image)

        
        prediction = model.predict(preprocessed_image)
        predicted_class = 'COVID-19' if prediction[0][0] > 0.5 else 'Normal'

        st.write(f'Prediction: {predicted_class}')
        st.write(f'Confidence: {prediction[0][0]:.2f}')

if __name__ == '__main__':
    main()

