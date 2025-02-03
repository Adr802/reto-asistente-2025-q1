FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos locales al contenedor
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]