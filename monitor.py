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

CURRENT_DIR = os.path.dirname(__file__)
pidfile = open(os.path.realpath(__file__), "r")
################################################
# logging config
LOG_FILE = os.path.abspath(os.path.join(CURRENT_DIR, "logger.conf"))
logging.config.fileConfig(LOG_FILE)
logger = logging.getLogger("monitor")
MONITOR_LOG = os.path.abspath(os.path.join(CURRENT_DIR, "monitor.log"))
logger.addHandler(logging.FileHandler(MONITOR_LOG));

try:

    # 创建一个排他锁,并且所被锁住其他进程不会阻塞
    fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    ################################################
    cf = ConfigParser.ConfigParser()
    ################################################
    # common config
    COMMON_FILE = os.path.abspath(os.path.join(CURRENT_DIR, "common.conf"))
    cf.read(COMMON_FILE)
    server_monitor_name = cf.get("common", "server_monitor_name")
    all_servers_info_set = cf.get("common", "all_servers_info_set")
    server_monitor_log_num = cf.get("common", "server_monitor_log_num")
    ################################################
    # server config
    SERVER_FILE = os.path.abspath(os.path.join(CURRENT_DIR, "server.conf"))
    cf.read(SERVER_FILE)
    server_name = cf.get("server", "server_name")
    server_ip = cf.get("server", "server_ip")
    server_monitor_name = server_name + "_" + server_monitor_name

    ################################################
    # redis config
    REDIS_FILE = os.path.abspath(os.path.join(CURRENT_DIR, "redis.conf"))
    cf.read(REDIS_FILE)
    redis_ip = cf.get("redis", "redis_ip")
    redis_port = cf.get("redis", "redis_port")
    redis_auth = cf.get("redis", "redis_auth")

    if redis_auth is None:
        r = redis.Redis(host=redis_ip, port=redis_port, db=0)
    else:
        r = redis.Redis(host=redis_ip, port=redis_port, password=redis_auth, db=0)

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
    MONITOR_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "monitor"))
    monitor_modules = [name for _, name, _ in pkgutil.iter_modules([MONITOR_DIR])]
    monitor_content = {}
    for monitor_module in monitor_modules:
        module_class = eval(monitor_module + "." + monitor_module)()
        data = module_class.display()
        for key in data:
            monitor_content[key] = data[key]
    monitor_content['time'] = time.mktime(datetime.datetime.now().timetuple())
    r.set(server_monitor_name, json.dumps(monitor_content))

    # add history log
    server_monitor_log_name = server_monitor_name + "_log"
    now_log_llen = r.llen(server_monitor_log_name)
    if (int(now_log_llen) < int(server_monitor_log_num)):
        r.lpush(server_monitor_log_name, json.dumps(monitor_content))
    else:
        r.brpop(server_monitor_log_name)
        r.lpush(server_monitor_log_name, json.dumps(monitor_content))

    sys.exit(1)
except Exception as ex:
    logger.exception(ex)
    sys.exit(1)
