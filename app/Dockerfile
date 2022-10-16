FROM tensorflow/tensorflow:nightly-gpu

RUN apt-get update #&& apt-get install -y python3 python3-pip sudo 

RUN pip3 install opencv-python-headless && pip3 install scipy

ENV PATH "${PATH}:/home/tomart/.local/bin"

COPY . /home/tomart/app/

RUN cd /home/tomart/app/ && pip3 install -r requirements.txt

WORKDIR /home/tomart/app

CMD ["python3", "multitarget_facerecognition_learn.py"]
