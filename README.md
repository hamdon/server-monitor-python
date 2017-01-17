# server-monitor-python
server infrastructure monitor

服务器环境：
linux
python2.6、 python2.7
需要安装python的redis和psutil
命令：
sudo easy_install redis
sudo easy_install psutil

如果报错：
1、fatal error: Python.h: No such file or directory
要安装一下python-devel
centos:
sudo yum install python-devel

2、-bash: easy_install: command not found
执行：wget https://bootstrap.pypa.io/ez_setup.py -O - | python

代码目录结构：
.
├── logger.conf         //日志配置文件
├── monitor              //监控内容的目录
│   ├── cpu.py           //监控cpu使用情况
│   ├── disk.py           //监控磁盘使用情况
│   ├── __init__.py       //包管理文件
│   └── memory.py     //监控内存使用情况
├── monitor.log          //代码执行过程产生的错误记录日志
├── monitor.py           //主监控执行程序
├── redis.conf             //redis配置文件
└── server.conf           //本机服务器基本信息配置文件
