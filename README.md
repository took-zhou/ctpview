# RUN 容器镜像

## 主要用于搭建可执行程序的运行环境

## 运行容器
### 命令行方式

`docker run --name=[name] -p [port:port]  -v [宿主机目录]:[容器目录] -it [image-id] /bin/bash`

比如 `docker run --name=run -e http_ip=192.168.0.102 -e http_port=8095 -e package=2021-10-28.tar -p 11331:11332 -v /data/simnow-workhours:/home/tsaodai -it [image-id] /bin/bash`  
建议统一windows和aliyun run容器的挂载目录，开发和长期运行都将升级包拷贝到/data/simnow-workhours目录下，
实现测试程序升级
### docker-compose.yml 文件运行
样例：

version: "3"
services:

  ctp_dev:
    restart: always
    image: "192.168.0.102:8098/tsaodai/marktrade:latest"
    devices:
      - /dev/mem:/dev/mem
    environment:
      - http_ip=192.168.0.102
      - http_port=8095
      - package=2021-10-28.tar
    ports:
      - "11337:11332"
      - "8096:8888"
    volumes:
      - /home/zhoufan/code/quantation:/share
      - /data/simnow-workhours_zhoufan:/home/tsaodai
    tty: true
    stdin_open: true
    privileged: true
    networks:
      xizhou:
        ipv4_address: 192.168.16.3

#docker network create --subnet=192.168.16.0/24 xizhou
networks:
  xizhou:
    external: true

在docker-compose.yml同目录下，执行docker-compose up命令会自动生成容器（docker-compose up -d后台运行容器命令）。

## 使用容器
容器生成后，需要将升级包拷贝到/data/simnow-workhours目录下。升级包是通过compile容器通过python build.py pack命令生成，
生成目录在output/pack下，比如：output/pack/2020-05-24

### 使用容器常用操作：

1. 进入容器 docker exec -it [容器id] /bin/bash
2. 修改/etc/marktrade/marktrade.conf文件里面PROJPATH变量，指定到目标升级包
3. update marktrade 更新升级包到容器

## 疑问
邮箱zhoufan@cdsslh.com或微信18556936316联系。