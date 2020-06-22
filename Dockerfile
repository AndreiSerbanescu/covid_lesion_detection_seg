FROM nvidia/cuda:10.0-cudnn7-devel

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
RUN pip3 install tensorflow-gpu==1.14.0
RUN pip3 install simpleitk==1.2.4

# fix opencv import issue
RUN apt-get install libsm6 libxext6 libxrender-dev -y

COPY files/source/code/keras_retinanet /app/keras_retinanet
COPY files/source/code/setup-env.sh /app/setup-env.sh
COPY files/source/code/setup.py /app/setup.py

sRUN sh /app/setup-env.sh

RUN mkdir /app/data_share
ENV DATA_SHARE_PATH /app/data_share

COPY files/source/ /app/
COPY files/interface/ /app/

ENV LD_LIBRARY_PATH /usr/local/cuda-10.0:/usr/local/nvidia/lib:/usr/local/nvidia/lib64

CMD ["python3","-u","/app/run_container_jip.py"]