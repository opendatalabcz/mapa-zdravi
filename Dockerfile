FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src/app /code/app

CMD ["python3", "src/main.py"]  
# "python3" "-m" "webbrowser" "http://127.0.0.1:5000"