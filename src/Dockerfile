FROM python:3.7

RUN mkdir /code
WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["waitress-serve", "--port=3000",  "--call", "app:create_app"]  
