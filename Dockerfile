# Usa una versione moderna di Python. La 3.9 o 3.10 è stabile.
FROM python:3.9-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Monta la cartella del modello come volume
VOLUME /app/model

# Copia i file dell'applicazione e le dipendenze
COPY app.py .
COPY requirements.txt .

# --- NUOVO PASSAGGIO CRUCIALE: Installazione da repository ufficiale ---
# Installiamo tflite-runtime e le altre dipendenze, 
# dicendo a pip di cercare il binario di TFLite nel repository di Google.
RUN pip install --no-cache-dir \
    tflite-runtime \
    --extra-index-url https://www.piwheels.org/simple \
    --find-links https://github.com/google-coral/pycoral/releases \
    -r requirements.txt

# La porta su cui è in ascolto l'API (deve corrispondere a app.run nel codice)
EXPOSE 5000

# Comando per avviare il server Flask
#CMD ["python", "app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
