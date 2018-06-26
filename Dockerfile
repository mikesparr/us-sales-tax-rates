FROM python:alpine3.6

RUN apk update

WORKDIR /usr/src/app
COPY . .

RUN pip install -r requirements.txt

CMD ["/usr/src/app/run"]
