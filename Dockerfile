FROM python:3.8.5-buster
RUN mkdir /src
COPY . /src
WORKDIR /src
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
