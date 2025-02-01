# Вибираємо офіційний образ Python
FROM python:3.10

# Встановлюємо робочу директорію
WORKDIR /app

# Спочатку копіюємо тільки requirements.txt, щоб використовувати кеш
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Тепер копіюємо всі файли проєкту
COPY . .

# Очікуємо запуск MySQL перед стартом FastAPI
CMD ["sh", "-c", "sleep 10 && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
