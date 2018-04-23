FROM ubuntu

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y dist-upgrade && apt-get install -y \
    apt-utils \
    build-essential \
    bzip2 \
    software-properties-common \
    vim \
    wget

RUN cd ~ && wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN cd ~ && bash Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm ~/Miniconda3-latest-Linux-x86_64.sh
ENV PATH /miniconda/bin:${PATH}
RUN conda update -y conda
RUN conda install -y pip
RUN pip install --upgrade pip
RUN pip install Cython
RUN conda install pandas scipy scikit-learn numpy
RUN pip install dash==0.21.0
RUN pip install dash-renderer==0.12.1
RUN pip install dash-html-components==0.10.0
RUN pip install dash-core-components==0.22.1
RUN pip install plotly --upgrade

RUN cd ~
COPY app.py  /root/
COPY model  /root/
COPY data  /root/

WORKDIR /root/
EXPOSE 8080

CMD ["/miniconda/bin/python", "app.py"]
