FROM python:3.9-slim
WORKDIR /app

FROM python:3.9-slim

# Instala dependências para locales
RUN apt-get update && apt-get install -y locales

# Configura o locale pt_BR.UTF-8
RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen pt_BR.UTF-8 && \
    update-locale LANG=pt_BR.UTF-8

COPY requiriments.txt requiriments.txt
RUN pip install -r requiriments.txt

COPY . .

EXPOSE 8080
EXPOSE 8081
CMD [ "gunicorn", "--bind", "0.0.0.0:8081", "wsgi:app"]