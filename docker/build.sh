#!/usr/bin/env bash

apt-get update -y
# apt-get -y install sshpass
pip3 install -r /tmp/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


# export PATH = xx
