FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

RUN pip3 install --upgrade pip
RUN pip3 install virtualenv
ADD requirements.txt .
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y ghostscript
RUN pip3 install ocrmypdf
RUN apt-get install -y tesseract-ocr

RUN groupadd --gid 1000 group1 && useradd --uid 1000 --groups group1 -ms /bin/bash user1
USER user1
WORKDIR /home/user1

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
