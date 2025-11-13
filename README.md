# TensorFlowAPI

API per classificazione immagini basata su un modello esportato da Teachable Machine / Keras.

Nota: l'app carica il modello da dentro il container nella cartella `/model`. Non inserire i modelli nell'immagine: monta una cartella dal host.

## Requisiti
- Python 3.11+
- Dipendenze: `pip install -r requirements.txt`
- File modello richiesti nella cartella montata:
  - `keras_model.h5`
  - `labels.txt` (una etichetta per riga, lo stesso ordine usato durante l'export)

## Avvio in locale (sviluppo)
1. Assicurati che `keras_model.h5` e `labels.txt` siano in una cartella `model/` accanto al repository (opzionale).
2. Installa dipendenze:
   ```
   pip install -r requirements.txt
   ```
3. Avvia il server (sviluppo):
   ```
   python app.py
   ```
   Il server ascolta su `0.0.0.0:5000`.

Per produzione si consiglia di usare un WSGI server come Gunicorn:
```
gunicorn --bind 0.0.0.0:5000 app:app
```

Assicurati che la cartella host contenga `keras_model.h5` e `labels.txt`.

## Endpoint
GET /predict

Parametri query:
- url (required) — URL dell'immagine da processare
- token (optional) — token aggiunto all'URL se necessario (aggiunto come query param)
  
Esempio:
```
GET http://127.0.0.1:5000/predict?url=https://example.com/image.jpg
```

Codici di errore comuni:
- 400 — parametro `url` mancante o errore nel download dell'immagine
- 500 — modello non caricato o errore interno di predizione

## Note implementative
- L'app crea file temporanei in `./tmp` per il download delle immagini e li rimuove dopo l'elaborazione.
- L'app carica il modello al bootstrap da `/model/keras_model.h5` e `labels.txt`.
- Il preprocessing segue lo schema di Teachable Machine: resize a 224x224, normalizzazione `(pixel/127.0)-1`.
- Se il modello non viene caricato all'avvio, l'endpoint restituirà errore 500 con messaggio appropriato.

## Troubleshooting
- Controlla che i nomi dei file siano esatti (`keras_model.h5`, `labels.txt`).
- Se usi Docker su Windows, verifica i permessi di condivisione della cartella montata.
- Per test locali senza Docker, copia i file `keras_model.h5` e `labels.txt` in una cartella `model` e avvia `python app.py`.