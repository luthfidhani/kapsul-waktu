# Gunakan base image Python
FROM python:3.9-slim-bullseye AS base

# Set working directory
WORKDIR /app

# Salin file dependensi ke dalam image
COPY requirements.txt .

# Install dependensi
RUN pip install -r requirements.txt

# Salin seluruh proyek ke dalam image
COPY . .

# Expose port yang digunakan oleh aplikasi
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD python app/main.py run --reload
