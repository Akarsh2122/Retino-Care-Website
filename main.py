from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import tensorflow as tf
from efficientnet.tfkeras import EfficientNetB0
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model('diabetic_eye_weights1.h5', compile=False)
disease_classes = {0 : 'No DR', 1 : 'Mild DR', 2 : 'Moderate DR', 3 : 'Severe DR', 4 : 'Proliferative DR'}

def process_image(image):
    img = cv2.resize(image, (256, 256))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    
    predictions = model.predict(img)
    predicted_class = np.argmax(predictions[0])
    
    return disease_classes[predicted_class]

@app.post("/predict")
async def predict(firstName: str = Form(...), lastName: str = Form(...), photo: UploadFile = File(...)):
    image = cv2.imdecode(np.frombuffer(await photo.read(), np.uint8), cv2.IMREAD_COLOR)
    
    result = process_image(image)
    
    return JSONResponse(content={"result": result, "firstName": firstName, "lastName": lastName})
