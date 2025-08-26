# Escolhe imagem base
FROM python:3.13

# Diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . /app

# Instala as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expõe a porta usada pelo Django
EXPOSE 2000

# Comando para rodar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:2000"]