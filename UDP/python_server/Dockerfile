# Usa una imagen base de Python 3.10 Slim por ser ligera y adecuada para muchos proyectos
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Actualiza los paquetes del sistema y instala las dependencias necesarias para psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala Flask, psycopg2-binary y python-dotenv directamente usando pip
RUN pip install --upgrade pip && \
    pip install Flask psycopg2-binary python-dotenv && \
    pip install flask-cors

# Copia el resto de tu aplicación al contenedor
# Asegúrate de que .dockerignore esté configurado para no incluir directorios innecesarios
COPY . .

# Utiliza flask para ejecutar la aplicación para aprovechar el reloader en desarrollo
CMD ["flask", "run", "--host=0.0.0.0"]
