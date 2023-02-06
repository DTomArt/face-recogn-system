FROM nvcr.io/nvidia/l4t-tensorflow:r32.7.1-tf2.7-py3

ENV PATH "${PATH}:/home/tomart/.local/bin"

RUN apt-get update

RUN pip3 install --upgrade pip && pip3 install opencv-python-headless

COPY ./requirements.txt /home/tomart/webapp/requirements.txt

RUN cd /home/tomart/webapp/ && pip3 install -r requirements.txt

COPY . /home/tomart/webapp/

WORKDIR /home/tomart/webapp

RUN chmod g+x ./face_recogn_app.py

CMD [ "python3", "-u", "face_recogn_app.py"]
