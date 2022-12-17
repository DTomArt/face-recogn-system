FROM python:3.9

ENV PATH "${PATH}:/home/tomart/.local/bin"

RUN apt-get update

COPY ./requirements.txt /front/requirements.txt

RUN cd /front/ && pip3 install -r requirements.txt

COPY . /front/

WORKDIR /front

RUN chmod g+x ./frontend.py

CMD [ "python", "-u", "frontend.py"]