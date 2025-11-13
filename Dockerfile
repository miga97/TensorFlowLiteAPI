# Usa una versione moderna di Python. La 3.9 o 3.10 è stabile.
FROM python:3.9-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Monta la cartella del modello come volume
VOLUME /app/model

# Copia i file dell'applicazione e le dipendenze
COPY app.py .
COPY requirements.txt .

# --- NUOVO PASSAGGIO CRUCIALE: Installazione forzata di tflite-runtime ---
# Installiamo una versione di tflite-runtime per Linux x86_64 e Python 3.9
# Questa versione è il runtime leggero che risolve il problema AVX
RUN pip install --no-cache-dir \
    https://github.com/google-coral/pycoral/releases/download/v2.0.0/tflite_runtime-2.5.0-cp39-cp39-linux_x86_64.whl \
    -r requirements.txt

# La porta su cui è in ascolto l'API (deve corrispondere a app.run nel codice)
EXPOSE 5000

# Comando per avviare il server Flask
#CMD ["python", "app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
