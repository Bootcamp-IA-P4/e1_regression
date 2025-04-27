# e1_regression/Dockerfile

FROM python:3.13-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Asegura que el directorio donde pip instala ejecutables esté en el PATH
ENV PATH="/usr/local/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config libmariadb-dev libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Comando para ejecutar la aplicación usando Gunicorn
# ¡Volvemos a la forma de lista (exec form) AHORA que el PATH está configurado!
# En tu Dockerfile, como último recurso o para depurar:
CMD ["/usr/local/bin/gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "main:create_app()"]
# O si usas la instancia 'app' directamente:
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]