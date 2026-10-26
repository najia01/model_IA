# 1. Image de base légère demandée par le brief
FROM python:3.11-slim

# 2. On définit le dossier de travail à l'intérieur de la boîte
WORKDIR /app

# 3. On copie d'abord la liste des dépendances et on les installe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. On copie le code source et le modèle
COPY src/ ./src/
COPY Model/ ./Model/

# 5. On indique le port sur lequel l'API va écouter
EXPOSE 8000

# 6. La commande pour démarrer le serveur (l'API)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]