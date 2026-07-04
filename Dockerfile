FROM python:3.11-slim

# Utilizator non-root obligatoriu pentru Hugging Face
RUN useradd -m -u 1000 user
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R user:user /app
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user:user . .

EXPOSE 7860

# Pornire curată fără flag-uri care pot bloca proxy-ul intern HF
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
]
