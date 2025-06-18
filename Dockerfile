FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

CMD [nohup python3 user_main.py > logs_user.txt 2>&1 &\ nohup python3 seller_main.py > logs_seller.txt 2>&1 &]

