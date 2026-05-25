FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılık dosyalarını kopyala
COPY requirements.txt .

# Bağımlılıkları ve gunicorn'u kur
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Tüm proje dosyalarını kopyala
COPY . .

# Ortam değişkenleri
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 5000 portunu dışarı aç
EXPOSE 5000

# Uygulamayı gunicorn ile başlat
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
