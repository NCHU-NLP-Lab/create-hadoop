FROM tensorflow/tensorflow:1.14.0-gpu-py3-jupyter
LABEL maintainer="p208p2002@gmail.com"

RUN apt-get update 
RUN apt-get install -y sudo \ 
                        apt-utils \
                        default-jdk \
                        wget \
                        vim \
                        git

# ip、ping
RUN apt-get install -y net-tools \
                        iputils-ping

# pip3
RUN apt-get install -y python3-pip

# ssh
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd

# script for create user
COPY script_files/docker_start.sh /docker_start.sh
RUN chmod 777 /docker_start.sh

# pytorch
RUN pip install https://download.pytorch.org/whl/cu100/torch-1.3.0%2Bcu100-cp36-cp36m-linux_x86_64.whl

# jupyter
COPY config_files/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# avoid scp error
RUN rm /etc/bash.bashrc
RUN touch /etc/bash.bashrc

# utf-8 zh_TW
RUN apt-get install -y locales
RUN locale-gen en_US.utf8
RUN echo 'export LANGUAGE="en_US.utf8"' >> /etc/bash.bashrc
RUN echo 'export LANG="en_US.utf8"' >> /etc/bash.bashrc
RUN echo 'export LC_ALL="en_US.utf8"' >> /etc/bash.bashrc
RUN update-locale LANG=en_US.utf8

#
ENTRYPOINT /docker_start.sh && /bin/bash