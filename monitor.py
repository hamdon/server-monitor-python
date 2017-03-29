#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import redis
import json
import fcntl
import logging
import logging.config
import string, os, sys
import pkgutil
import datetime
import time
from monitor import *

current_dir = os.path.dirname(__file__)
pidfile = open(os.path.realpath(__file__), "r")
################################################
# logging config
logger_conf_file = os.path.abspath(os.path.join(current_dir, "logger.conf"))
logging.config.fileConfig(logger_conf_file)
logger = logging.getLogger("monitor")
monitor_log = os.path.abspath(os.path.join(current_dir, "monitor.log"))
logger.addHandler(logging.FileHandler(monitor_log))

try:

    # 创建一个排他锁,为了避免同时操作文件，需要程序自己来检查该文件是否已经被加锁。这里如果检查到加锁了，进程会被阻塞
    fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    ################################################
    cf = ConfigParser.ConfigParser()
    ################################################
    # common config
    common_conf_file = os.path.abspath(os.path.join(current_dir, "common.conf"))
    cf.read(common_conf_file)
    server_monitor_name = cf.get("common", "server_monitor_name")
    all_servers_info_set = cf.get("common", "all_servers_info_set")
    server_monitor_log_num = cf.get("common", "server_monitor_log_num")
    ################################################
    # server config
    server_conf_file = os.path.abspath(os.path.join(current_dir, "server.conf"))
    cf.read(server_conf_file)
    server_name = cf.get("server", "server_name")
    server_ip = cf.get("server", "server_ip")
    server_monitor_name = server_name + "_" + server_monitor_name

    ################################################
    # redis config
    redis_conf_file = os.path.abspath(os.path.join(current_dir, "redis.conf"))
    cf.read(redis_conf_file)
    redis_ip = cf.get("redis", "redis_ip")
    redis_port = cf.get("redis", "redis_port")
    redis_auth = cf.get("redis", "redis_auth")

    if redis_auth is None:
        pool = redis.ConnectionPool(host=redis_ip, port=redis_port, db=0)
    else:
        pool = redis.ConnectionPool(host=redis_ip, port=redis_port, password=redis_auth, db=0)
    r = redis.Redis(connection_pool=pool)
    ################################################
    # monitor server list
    all_servers = r.get(all_servers_info_set)
    if all_servers is None:
        s = {}
    else:
        s = json.loads(all_servers)
    if server_name not in s or s[server_name] is None:
        s[server_name] = {'ip': server_ip, 'data': server_monitor_name}
        t = json.dumps(s)
        r.set(all_servers_info_set, t)

    ################################################
    # monitor server detail data
    monitor_content_dir = os.path.abspath(os.path.join(current_dir, "monitor"))
    monitor_modules = [name for _, name, _ in pkgutil.iter_modules([monitor_content_dir])]
    monitor_content = {}
    for monitor_module in monitor_modules:
        module_class = eval(monitor_module + "." + monitor_module)()
        data = module_class.display()
        for key in data:
            monitor_content[key] = data[key]
    monitor_content['time'] = time.mktime(datetime.datetime.now().timetuple())
    r.set(server_monitor_name, json.dumps(monitor_content))

    # add history log
    server_monitor_history_name = server_monitor_name + "_log"
    now_log_count = r.llen(server_monitor_history_name)
    if (int(now_log_count) < int(server_monitor_log_num)):
        r.lpush(server_monitor_history_name, json.dumps(monitor_content))
    else:
        r.brpop(server_monitor_history_name)
        r.lpush(server_monitor_history_name, json.dumps(monitor_content))

    sys.exit(1)
except Exception as ex:
    logger.exception(ex)
    sys.exit(1)
