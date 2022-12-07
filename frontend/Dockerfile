FROM python:3.9

ENV PATH "${PATH}:/home/tomart/.local/bin"

RUN apt-get update

COPY ./requirements.txt /home/tomart/frontend/requirements.txt

RUN cd /home/tomart/frontend/ && pip3 install -r requirements.txt

COPY . /home/tomart/frontend/

WORKDIR /home/tomart/frontend

RUN chmod g+x ./frontend.py

CMD [ "./frontend.py" ]