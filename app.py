from flask import Flask, request, jsonify
from tensorflow import lite as tflite
from PIL import Image
import numpy as np
import time
import requests
import os
import logging

# Configurazione logger (opzionale ma utile)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Variabili Globali
GLOBAL_INTERPRETER = None
INPUT_DETAILS = None
OUTPUT_DETAILS = None
CLASS_NAMES = []

# Carica il modello TFLite e le etichette
def load_model():
    global GLOBAL_INTERPRETER, INPUT_DETAILS, OUTPUT_DETAILS, CLASS_NAMES
    
    # Nomi dei file TFLite (supponendo che tu li abbia copiati nella directory /model)
    MODEL_PATH = '/model/converted_tflite_fp32.tflite'
    LABELS_PATH = '/model/labels.txt'

    try:
        # 1. Carica l'interprete TFLite
        GLOBAL_INTERPRETER = tflite.Interpreter(model_path=MODEL_PATH)
        GLOBAL_INTERPRETER.allocate_tensors()
        
        # 2. Ottieni dettagli degli input/output per la previsione
        INPUT_DETAILS = GLOBAL_INTERPRETER.get_input_details()
        OUTPUT_DETAILS = GLOBAL_INTERPRETER.get_output_details()
        
        # 3. Carica i nomi delle classi
        CLASS_NAMES = open(LABELS_PATH, "r").read().splitlines()
        
        logging.info("Modello TFLite caricato con successo")
        
    except Exception as e:
        logging.error(f"Errore nel caricamento del modello TFLite: {e}")
        GLOBAL_INTERPRETER = None
        CLASS_NAMES = []

def download_image(url: str, token: str = None, dest_dir: str = './tmp'):
    logging.info("Scarico l'immagine da: %s", url)
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
    if not GLOBAL_INTERPRETER:
        return jsonify({"error": "Modello TFLite non caricato"}), 500

    url = request.args.get('url')
    token = request.args.get('token')
    if not url:
        return jsonify({"error": "Parametro 'url' richiesto per GET"}), 400

    tmp_file = None
    try:
        tmp_file = download_image(url, token)

        # 2. Pre-elaborazione dell'immagine (uguale a Keras, dimensioni 224x224)
        image = Image.open(tmp_file).convert("RGB")
        image = image.resize((224, 224))
        
        # 2.3. Converti in array NumPy e normalizza
        # La forma e il tipo di dato devono corrispondere all'input_details
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_array = np.asarray(image)
        # Normalizzazione: (Valore / 127.0) - 1.0
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1.0
        data[0] = normalized_image_array
        
        # --- MODIFICHE ALLA PREVISIONE (TFLite) ---
        
        # 3. Esegue la previsione
        # Imposta l'input
        GLOBAL_INTERPRETER.set_tensor(INPUT_DETAILS[0]['index'], data)
        # Esegue l'inferenza
        GLOBAL_INTERPRETER.invoke()
        # Ottiene l'output
        prediction = GLOBAL_INTERPRETER.get_tensor(OUTPUT_DETAILS[0]['index'])
        
        # -------------------------------------------    
        # 4. Formattazione della risposta JSON (stesso formato di prima)
        predicted_index = np.argmax(prediction)
        predicted_class = CLASS_NAMES[predicted_index].strip()
        confidence = float(prediction[0][predicted_index])
        
        scores = {CLASS_NAMES[i].strip(): float(prediction[0][i]) for i in range(len(CLASS_NAMES))}

        response = {
            "stato": predicted_class,
            "confidenza": confidence,
            "probabilita_complete": scores
        }
        logging.info("Predizione completata con successo")
        return jsonify(response)
    
    except requests.RequestException as e:
        logging.error("Errore download immagine: %s", e)
        return jsonify({"error": f"Errore download immagine: {e}"}), 400
    except Exception as e:
        logging.error("Errore durante la predizione: %s", e)
        return jsonify({"error": f"Errore durante la predizione: {e}"}), 500
    finally:
        if tmp_file and os.path.isfile(tmp_file):
            try:
                os.remove(tmp_file)
            except Exception:
                logging.error("Errore durante la rimozione del file temporaneo: %s", tmp_file)
                pass


load_model() # Carica il modello TFLite all'avvio

if __name__ == '__main__':
    # Usare Gunicorn per la produzione (l'avvio di Flask è solo per il debug locale)
    logging.info("Avvio dell'app Flask (modalità Debug)")
    app.run(debug=True, host='0.0.0.0', port=5000)