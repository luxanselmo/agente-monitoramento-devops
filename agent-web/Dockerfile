FROM python:3.10-slim

WORKDIR /app

COPY main.py .

RUN apt-get update && \
    apt-get install -y iputils-ping && \
    pip install requests psycopg2-binary

CMD ["python", "main.py"]
