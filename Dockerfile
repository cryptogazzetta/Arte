# Use uma imagem base do Python
FROM python:3.8-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o script para o contêiner
COPY main.py .

# Comando para executar o scraper quando o contêiner for iniciado
CMD ["python3", "main.py"]