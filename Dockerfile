FROM python:3.8-slim

RUN pip3 install --upgrade pip
RUN pip3 install virtualenv
ADD requirements.txt .
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y ghostscript
RUN pip3 install ocrmypdf
RUN apt-get install -y tesseract-ocr

RUN useradd -ms /bin/bash user1
USER user1
WORKDIR /home/user1

CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver

