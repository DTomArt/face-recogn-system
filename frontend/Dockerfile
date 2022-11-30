FROM tensorflow/tensorflow:2.11.0rc1-gpu

ENV PATH "${PATH}:/home/tomart/.local/bin"

RUN apt-get update && apt-get install -y python3.8 python3-pip

COPY ./requirements.txt /home/tomart/frontend/requirements.txt

RUN cd /home/tomart/frontend/ && pip3 install -r requirements.txt

COPY . /home/tomart/frontend/

WORKDIR /home/tomart/frontend

RUN chmod g+x ./frontend.py

CMD [ "./frontend.py" ]