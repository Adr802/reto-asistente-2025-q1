FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos locales al contenedor
COPY . /app

# Copia el archivo de dependencias al contenedor
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente al contenedor
COPY . /app/

EXPOSE 5000

CMD ["python", "main.py"]