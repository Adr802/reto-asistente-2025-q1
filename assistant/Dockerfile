# Usa la imagen base de Python 3.11
FROM python:3.11

# Establece el entorno no interactivo para evitar prompts durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualiza los repositorios e instala Tesseract OCR y Ghostscript
RUN apt-get update && \
    apt-get install -y tesseract-ocr ghostscript && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establece la variable de entorno TESSDATA_PREFIX
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias al contenedor
COPY requirements.txt /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente al contenedor
COPY . /app/

# Expone el puerto 5000
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]
