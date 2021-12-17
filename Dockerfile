FROM nvidia/opengl:1.2-glvnd-runtime-ubuntu16.04 AS base
RUN apt-get update && \
    apt-get install -y git wget python python-pip cmake-curses-gui mayavi2

RUN wget -O- http://neuro.debian.net/lists/xenial.us-ca.full | tee /etc/apt/sources.list.d/neurodebian.sources.list \
    && apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xA5D32F012649A5A9

RUN apt-get update && \
    apt-get install -y fsl ants dcm2niix mrtrix3

RUN pip install pathlib
RUN pip install cython setuptools==44.1.1 decorator==4.3.0 ordered-set==3.1.1 pyyaml
RUN pip install numpy==1.16.6 scipy==1.2.2 hjson pyparsing==2.4.7 future networkx==2.2 scikits.bootstrap
RUN pip install kiwisolver==1.1.0 matplotlib==2.2.5 pandas==0.24.2 nibabel==2.5.2 dipy==0.12.0 SQLAlchemy==1.3.0 Pillow==6.2.2 nipype==0.11.0 seaborn==0.7.0

WORKDIR /apps
    
RUN wget https://www.slicer.org/slicer3-downloads/Release/linux-x86_64/Slicer3-3.6.3-2011-03-04-linux-x86_64.tar.gz &&  \
    tar -xzvf Slicer3-3.6.3-2011-03-04-linux-x86_64.tar.gz && rm Slicer3-3.6.3-2011-03-04-linux-x86_64.tar.gz

#RUN wget http://slicer.kitware.com/midas3/download/item/119825/Slicer-4.3.1-linux-amd64.tar.gz &&  \
#    tar -xzvf Slicer-4.3.1-linux-amd64.tar.gz && rm Slicer-4.3.1-linux-amd64.tar.gz
    
RUN git clone https://github.com/sinkpoint/pynrrd.git \
    && cd pynrrd && python setup.py install

RUN git clone https://github.com/sinkpoint/fascicle.git \
    && cd fascicle && python setup.py install
    
RUN git clone https://github.com/sinkpoint/hodaie-teem.git \
    && cd hodaie-teem && mkdir build && cd build \
    && cmake .. && make -j `nproc` && make install \
    && cd /usr/local/bin && ln -s tend tend2

RUN git clone https://github.com/sinkpoint/neuro-scripts.git \
    && cd /usr/bin && ln -s dcm2niix dcm2nii

COPY default.bashrc /etc/profile.d/sagit.bashrc

ENV APP_PATH /apps
ENV HLAB_SCRIPT_PATH ${APP_PATH}/neuro-scripts
ENV SLICER3_HOME ${APP_PATH}}/Slicer3-3.6.3-2011-03-04-linux-x86_64
ENV SLICER4_HOME ${APP_PATH}}/Slicer-4.3.1-linux-amd64
ENV ANTSPATH /usr/lib/ants/
ENV MRTRIX3_PATH /usr/lib/mrtrix/bin
ENV PATH ${PATH}:${HLAB_SCRIPT_PATH}:${HLAB_SCRIPT_PATH}/motion_correction
ENV PATH ${PATH}:$MRTRIX3_PATH:$ANTSPATH
ENV FREESURFER_HOME ${APP_PATH}/freesurfer
ENV NRRD_STATE_KEYVALUEPAIRS_PROPAGATE 1

FROM base AS dev

RUN apt-get install -y vim screen 
WORKDIR /dev

FROM base AS deploy

RUN apt-get install -y vim screen 
WORKDIR /apps
RUN git clone https://github.com/sinkpoint/sagit.git \
    && cd sagit && python setup.py install    
