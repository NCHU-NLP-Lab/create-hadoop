FROM tensorflow/tensorflow:1.14.0-gpu-py3-jupyter
LABEL maintainer="p208p2002@gmail.com"

# add new key
RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

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
