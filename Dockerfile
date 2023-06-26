FROM python:3.9.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "--bind 0.0.0.0:8080", "--worker-class aiohttp.GunicornWebWorker" ,"--workers", "5" ,"--threads", "2" ,"--timeout", "0", "--reload"]
