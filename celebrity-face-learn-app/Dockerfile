FROM tensorflow/tensorflow:2.11.0rc1-gpu

ENV PATH "${PATH}:/home/tomart/.local/bin"

RUN apt-get update

RUN pip3 install opencv-python-headless && pip3 install scipy

COPY ./requirements.txt /home/tomart/app/requirements.txt

RUN cd /home/tomart/app/ && pip3 install -r requirements.txt

COPY . /home/tomart/app/

WORKDIR /home/tomart/app

CMD ["python3", "multitarget_facerecognition_learn.py"]
