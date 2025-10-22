FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# все файлы проекта
COPY . .

# Запуск
CMD ["python", "main.py"]