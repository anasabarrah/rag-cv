# Image de base — Python 3.11 sur Linux léger
FROM python:3.11-slim

# Dossier de travail dans le container
WORKDIR /app

# Copie les fichiers dans le container
COPY . .

# Installe les dépendances
RUN pip install groq fastapi uvicorn pdfplumber

# Le port sur lequel l'app tourne
EXPOSE 8000

# Commande pour lancer l'app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]