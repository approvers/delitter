FROM alpine
RUN mkdir /src
COPY . /src
WORKDIR /src
RUN apk add python3 python3-dev musl-dev curl gcc
RUN curl -kL https://bootstrap.pypa.io/get-pip.py | python3
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]