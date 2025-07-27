FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ Copy .env.example to .env inside container
RUN cp .env.example .env

EXPOSE 8501

CMD ["streamlit", "run", "bot.py", "--server.port=8501", "--server.address=0.0.0.0"]
