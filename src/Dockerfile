FROM python:3.7

RUN mkdir /code
WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["python3", "main.py", "--host", "0.0.0.0", "--port", "80"]  

CMD ["waitress-serve", "--port=8080",  "--call", "app:create_app"]  


# "python3" "-m" "webbrowser" "http://127.0.0.1:5000"