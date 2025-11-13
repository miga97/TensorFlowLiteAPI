# Usa un'immagine Python di base con TensorFlow preinstallato o un ambiente leggero
# python:3.9-slim è un buon compromesso
FROM python:3.8-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Monta la cartella del modello come volume
VOLUME /app/model

# Copia i file dell'applicazione e le dipendenze
COPY app.py .
COPY requirements.txt .

# Installa le dipendenze Python (TensorFlow è grande, potrebbe richiedere tempo)
RUN pip install --no-cache-dir -r requirements.txt

# La porta su cui è in ascolto l'API (deve corrispondere a app.run nel codice)
EXPOSE 5000

# Comando per avviare il server Flask
#CMD ["python", "app.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
