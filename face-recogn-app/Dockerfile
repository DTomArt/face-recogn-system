FROM tensorflow/tensorflow:nightly-gpu

RUN apt-get update && apt-get install -y python3.8 python3-pip

RUN pip3 install opencv-python-headless

ENV PATH "${PATH}:/home/tomart/.local/bin"

COPY . /home/tomart/webapp/

RUN cd /home/tomart/webapp/ && pip3 install -r requirements.txt

WORKDIR /home/tomart/webapp

RUN chmod g+x ./face_recogn_app.py

CMD [ "./face_recogn_app.py" ]