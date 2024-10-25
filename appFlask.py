from __future__ import division, print_function

# Keras / TensorFlow
from keras.models import load_model
from keras.applications.imagenet_utils import preprocess_input

# Flask
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

# Librerías adicionales
import os
import numpy as np
import cv2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Flask
def crear_app():
    width_shape = 224
    height_shape = 224

    # Lista de nombres de aves
    names = ['CATHARTES AURA', 'COEREBA FLAVEOLA', 'COLUMBA LIVIA', 'CORAGYPS ATRATUS', 'CROTOPHAGA SULCIROSTRIS', 
             'CYANOCORAX YNCAS', 'EGRETTA THULA', 'FALCO PEREGRINUS', 'FALCO SPARVERIUS', 'HIRUNDO RUSTICA', 
             'PANDION HALIAETUS', 'PILHERODIUS PILEATUS', 'PITANGUS SULPHURATUS', 'PYRRHOMYIAS CINNAMOMEUS', 
             'RYNCHOPS NIGER', 'SETOPHAGA FUSCA', 'SYNALLAXIS AZARAE', 'TYRANNUS MELANCHOLICUS']

    # Definimos una instancia de Flask
    app = Flask(__name__)

    # Cargar el modelo preentrenado desde una ruta segura
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/optimizado.keras')

    # Verificar si el modelo existe
    if not os.path.exists(MODEL_PATH):
        raise ValueError(f"El modelo no se encontró en la ruta especificada: {MODEL_PATH}")

    # Cargar el modelo
    model = load_model(MODEL_PATH)
    print('Modelo cargado exitosamente. Verificar http://127.0.0.1:5000/')

    # Función para predecir a partir de una imagen
    def model_predict(img_path, model):
        try:
            img = cv2.resize(cv2.imread(img_path), (width_shape, height_shape), interpolation=cv2.INTER_AREA)
            x = np.asarray(img)
            x = preprocess_input(x)
            x = np.expand_dims(x, axis=0)
            
            preds = model.predict(x)
            return preds
        except Exception as e:
            print(f"Error en la predicción: {e}")
            return None

    # Ruta principal
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    # Ruta de predicción
    @app.route('/predict', methods=['POST'])
    def upload():
        if request.method == 'POST':
            # Validar si el archivo está presente
            if 'file' not in request.files:
                return jsonify({'error': 'No se encontró archivo para cargar.'}), 400

            f = request.files['file']

            # Validar tipo de archivo
            if f.filename == '' or not f.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                return jsonify({'error': 'Tipo de archivo no permitido. Solo se permiten imágenes (.png, .jpg, .jpeg)'}), 400

            # Guardar el archivo de manera segura
            basepath = os.path.dirname(__file__)
            upload_dir = os.path.join(basepath, 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            file_path = os.path.join(upload_dir, secure_filename(f.filename))
            f.save(file_path)

            # Realizar predicción
            preds = model_predict(file_path, model)
            if preds is None:
                return jsonify({'error': 'Ocurrió un error durante la predicción.'}), 500

            # Enviar el resultado de la predicción
            result = names[np.argmax(preds)]
            return jsonify({'result': result})
        return jsonify({'error': 'Método no permitido'}), 405

    return app


if __name__ == '__main__':
    app = crear_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
