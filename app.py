from flask import Flask, request, jsonify
import tensorflow.keras as keras
from PIL import Image
import numpy as np
import io
import time
import requests
import os

app = Flask(__name__)

# Carica il modello e le etichette
def load_model():
    global MODEL, CLASS_NAMES
    try:
        MODEL = keras.models.load_model('/model/keras_model.h5', compile=False)
        CLASS_NAMES = open("/model/labels.txt", "r").read().splitlines()
    except Exception as e:
        print(f"Errore nel caricamento del modello: {e}")
        MODEL = None
        CLASS_NAMES = []

load_model()

def download_image(url: str, token: str = None, dest_dir: str = './tmp'):
    """
    Scarica l'immagine dall'URL e restituisce il path del file salvato.
    """
    os.makedirs(dest_dir, exist_ok=True)
    if token:
        sep = '&' if '?' in url else '?'
        site = f"{url}{sep}token={token}"
    else:
        site = url
    filename = f"{int(time.time()*1000)}.jpg"
    file_path = os.path.join(dest_dir, filename)
    resp = requests.get(site, timeout=15)
    resp.raise_for_status()
    with open(file_path, 'wb') as f:
        f.write(resp.content)
    return file_path

@app.route('/predict', methods=['GET'])
def predict():
    if not MODEL:
        return jsonify({"error": "Modello non caricato"}), 500

    url = request.args.get('url')
    token = request.args.get('token')
    if not url:
        return jsonify({"error": "Parametro 'url' richiesto per GET"}), 400

    tmp_file = None
    try:
        tmp_file = download_image(url, token)

        # 2. Pre-elaborazione dell'immagine (come richiesto da Teachable Machine)
        # 2.1. Apri l'immagine
        image = Image.open(tmp_file).convert("RGB")

        # 2.2. Ridimensiona a 224x224 (dimensioni standard per TM)
        image = image.resize((224, 224))
    
        # 2.3. Converti in array NumPy e normalizza
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
    
        # 3. Previsione
        prediction = MODEL.predict(data)
    
        # 4. Formattazione della risposta JSON
        predicted_index = np.argmax(prediction)
        predicted_class = CLASS_NAMES[predicted_index].strip()
        confidence = float(prediction[0][predicted_index])
        
        # Crea un oggetto per mostrare tutte le probabilità
        scores = {CLASS_NAMES[i].strip(): float(prediction[0][i]) for i in range(len(CLASS_NAMES))}

        response = {
            "stato_cancello": predicted_class,
            "confidenza": confidence,
            "probabilita_complete": scores
        }
        return jsonify(response)
    except requests.RequestException as e:
        return jsonify({"error": f"Errore download immagine: {e}"}), 400
    except Exception as e:
        return jsonify({"error": f"Errore durante la predizione: {e}"}), 500
    finally:
        if tmp_file and os.path.isfile(tmp_file):
            try:
                os.remove(tmp_file)
            except Exception:
                pass

if __name__ == '__main__':
    # Usare un server WSGI come Gunicorn per la produzione
    # Qui usiamo la modalità debug di Flask per semplicità
    app.run(debug=True, host='0.0.0.0', port=5000)