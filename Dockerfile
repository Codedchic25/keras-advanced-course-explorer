FROM python:3.11-slim

# Creează utilizatorul cu UID 1000 cerut obligatoriu de Hugging Face Spaces
RUN useradd -m -u 1000 user
WORKDIR /app

# Instalează dependințele de sistem necesare ca root
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Schimbă proprietarul folderului de lucru înainte de a copia fișierele
RUN chown -R user:user /app

# Treci pe utilizatorul non-root
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

# Copiază și instalează dependințele Python
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copiază restul codului sursă
COPY --chown=user:user . .

EXPOSE 7860

# Pornire directă Streamlit conform specificațiilor oficiale Hugging Face
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]

