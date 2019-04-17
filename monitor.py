#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import fcntl
import logging
import logging.config
import os, sys
import pkgutil
from monitor import *
from LawManService import LawManService

current_dir = os.path.dirname(__file__)
pidfile = open(os.path.realpath(__file__), "r")
################################################
# logging config
monitor_log = os.path.abspath(os.path.join(current_dir, "monitor.log"))
logger = logging.getLogger()
handler = logging.FileHandler(monitor_log)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
try:

    # 创建一个排他锁,为了避免同时操作文件，需要程序自己来检查该文件是否已经被加锁。这里如果检查到加锁了，进程会被阻塞
    fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    ################################################
    cf = ConfigParser.ConfigParser()

    ################################################
    # monitor server detail data
    monitor_content_dir = os.path.abspath(os.path.join(current_dir, "monitor"))
    monitor_modules = [name for _, name, _ in pkgutil.iter_modules([monitor_content_dir])]
    monitor_content = {}
    is_send=0
    for monitor_module in monitor_modules:
        module_class = eval(monitor_module + "." + monitor_module)()
        data = module_class.display()
        for key in data:
            monitor_content[key] = data[key]
            if data['is_send']==1:
               is_send=1

    if is_send==1:
       lawManService = LawManService()
       lawManService.submitException(monitor_content)

    sys.exit(1)
except Exception as ex:
    logger.exception(ex)
    sys.exit(1)
