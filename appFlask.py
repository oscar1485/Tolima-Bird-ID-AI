from __future__ import division, print_function

# Keras
from keras.models import load_model
from keras.applications.imagenet_utils import preprocess_input

# Flask 
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify

import os
import numpy as np
import cv2
from dotenv import load_dotenv



def crear_app():
    width_shape = 224
    height_shape = 224

    names = ['CATHARTES AURA', 'COEREBA FLAVEOLA', 'COLUMBA LIVIA', 'CORAGYPS ATRATUS','CROTOPHAGA SULCIROSTRIS', 'CYANOCORAX YNCAS',
            'EGRETTA THULA', 'FALCO PEREGRINUS','FALCO SPARVERIUS', 'HIRUNDO RUSTICA', 'PANDION HALIAETUS', 'PILHERODIUS PILEATUS',
            'PITANGUS SULPHURATUS','PYRRHOMYIAS CINNAMOMEUS', 'RYNCHOPS NIGER', 'SETOPHAGA FUSCA','SYNALLAXIS AZARAE', 'TYRANNUS MELANCHOLICUS']

    # Definimos una instancia de Flask
    app = Flask(__name__)

    # Configurar la versión de Bun
    os.environ["BUN_VERSION"] = "1.1.0"

    # Path del modelo preentrenado
    MODEL_PATH = 'models/optimizado.keras'

    # Cargamos el modelo preentrenado
    model = load_model(MODEL_PATH)

    print('Modelo cargado exitosamente. Verificar http://127.0.0.1:10000/')

    # Realizamos la predicción usando la imagen cargada y el modelo
    def model_predict(img_path, model):

        img=cv2.resize(cv2.imread(img_path), (width_shape, height_shape), interpolation = cv2.INTER_AREA)
        x=np.asarray(img)
        x=preprocess_input(x)
        x = np.expand_dims(x,axis=0)
        
        preds = model.predict(x)
        return preds


    @app.route('/', methods=['GET'])
    def index():
        # Página principal
        return render_template('index.html')


    @app.route('/predict', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            try:
                # Obtiene el archivo del request
                f = request.files['file']

                # Graba el archivo en ./uploads
                basepath = os.path.dirname(__file__)
                file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
                f.save(file_path)

                # Predicción
                preds = model_predict(file_path, model)  # Asegúrate de que esta función esté definida

                # Obtener la clase con mayor probabilidad
                pred_class = names[np.argmax(preds)]
                print('PREDICCIÓN:', pred_class)

                # Enviamos el resultado de la predicción en formato JSON
                return jsonify({"predicción": pred_class}), 200
            except Exception as e:
                print(f'Error en la predicción: {str(e)}')
                return jsonify({"error": "Error en la predicción. Intente nuevamente."}), 500

        return jsonify({"message": "Método no permitido."}), 405  # Manejo para métodos GET
    return app



if __name__ == '__main__':
    app = crear_app()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)