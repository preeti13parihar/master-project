FROM python:3.8-slim

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y
RUN apt-get install nano

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt 

EXPOSE 9091

RUN chmod 777 start.sh

CMD [ "/app/start.sh" ]
# CMD ["gunicorn", "--bind", ":9091", "--workers", "3", "foodconnect.wsgi"]