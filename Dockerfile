FROM nvidia/cuda:latest

WORKDIR /app

# Installing Python3 and Pip3
RUN apt-get update
RUN apt-get update && apt-get install -y python3-pip virtualenv
RUN pip3 install setuptools pip --upgrade --force-reinstall

RUN pip3 install cython==0.29.14
RUN pip3 install h5py==2.10.0
RUN pip3 install keras==2.2.4
RUN pip3 install matplotlib==3.1.3
RUN pip3 install numpy>=1.14
RUN pip3 install opencv-python>=3.3.0
RUN pip3 install pillow==7.0.0
RUN pip3 install tqdm==4.40.2
RUN pip3 install tensorflow==1.14.0
RUN pip3 install simpleitk==1.2.4

# fix opencv import issue
RUN apt-get install libsm6 libxext6 libxrender-dev -y

COPY code/keras_retinanet /app/keras_retinanet
COPY code/setup-env.sh /app/setup-env.sh
COPY code/setup.py /app/setup.py

# TODO make alias python work as to not change setup-env script
RUN sh /app/setup-env.sh

COPY code /app/code
COPY model /app/model
COPY listen.py /app/listen.py