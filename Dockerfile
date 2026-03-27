# 1. Python tabanlı bir imaj kullanıyoruz
FROM python:3.10-slim

# 2. Çalışma dizini oluştur
WORKDIR /app

# 3. Gerekli sistem kütüphanelerini kur (PDF işleme vb. için)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Kütüphane listesini kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Tüm proje kodlarını içeri aktar
COPY . .

# 6. Streamlit için portu aç
EXPOSE 8501

# 7. Uygulamayı başlat
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]