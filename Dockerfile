# Use imagem Python leve
FROM python:3.12-slim

# Instala dependências do sistema e Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    wget \
    curl \
    unzip \
    gnupg \
    && apt-get clean

# Define variáveis de ambiente para localização do Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Cria diretório de trabalho e copia arquivos
WORKDIR /app
COPY . /app

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando de entrada
CMD ["python", "main.py"]
