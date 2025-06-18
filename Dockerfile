FROM python:3.12

RUN apt-get update && \
    apt-get install -y --no-install-recommends git &&\
    rm -rf /var/lib/apt/lists/*



RUN git clone https://github.com/CULPR1/atlas-fastapi.git/app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "user_main.py"] if using docker compose




