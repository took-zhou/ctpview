#基于192.168.0.102:8098/tsaodai/ubuntu1804镜像
FROM 192.168.0.102:8098/tsaodai/ubuntu1804:latest

#维护个人信息
MAINTAINER The run Project <zhoufan@cdsslh.com>

ARG user=tsaodai
ARG group=tsaodai
ARG uid=1000
ARG gid=1000
ARG TSAODAI_HOME=/home/tsaodai
ARG process=marktrade

#创建用户
RUN mkdir -p $TSAODAI_HOME \
  && chown ${uid}:${gid} $TSAODAI_HOME \
  && groupadd -g ${gid} ${group} \
  && useradd -d "$TSAODAI_HOME" -u ${uid} -g ${gid} -m -s /bin/bash ${user}

VOLUME $TSAODAI_HOME

#构建环境目录
RUN mkdir -p /usr/lib/$process && echo "/usr/lib/$process/" >> /etc/ld.so.conf.d/$process.conf && ldconfig

#安装私有python库
COPY requirements.txt /root/requirements.txt
RUN pip install -i https://mirrors.aliyun.com/pypi/simple  -r /root/requirements.txt

#安装依赖文件
RUN apt-get update && apt-get install -y libstdc++6 && apt-get install -y screen && \
  apt-get install -y vim && apt-get install -y net-tools && apt-get install -y sudo && \
  echo $user 'ALL=(ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers &&\
  apt-get install -y iputils-ping && apt-get install -y udev && apt-get install -y dmidecode &&\
  apt-get install -y wget && apt-get install -y iproute2

RUN echo "deb [trusted=yes] http://aptserver.tsaodai.com/debian/ ./" | sudo tee -a /etc/apt/sources.list > /dev/null && \
    apt-get update

#设置环境变量
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

#开放端口
expose 11332

#拷贝文件或目录到镜像中
COPY marktrade.sh /bin/$process.sh

#使用tsaodai用户启动streamlit
USER tsaodai
RUN sudo chmod +x /bin/$process.sh

ENTRYPOINT ["/bin/marktrade.sh"]
