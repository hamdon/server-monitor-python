#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import redis
import json
import logging
import logging.config
import string,os,sys
import pkgutil
import datetime
import time
from monitor import *

################################################
#logging config

logging.config.fileConfig("logger.conf")
logger = logging.getLogger("monitor")

try:

    cf = ConfigParser.ConfigParser()

################################################
#server config
    cf.read("server.conf")
    server_name=cf.get("server","server_name")
    server_ip=cf.get("server","server_ip")
    server_monitor_name=server_name+"_"+cf.get("server","server_monitor_name")
    all_servers_info_set=cf.get("server","all_servers_info_set")

################################################
#redis config
    cf.read("redis.conf")
    redis_ip=cf.get("redis","redis_ip")
    redis_port=cf.get("redis","redis_port")
    redis_auth=cf.get("redis","redis_auth")

    if redis_auth is None:
        r=redis.Redis(host=redis_ip,port=redis_port,db=0)
    else:
        r=redis.Redis(host=redis_ip,port=redis_port,password=redis_auth,db=0)

################################################
#monitor server list
    all_servers=r.get(all_servers_info_set)
    if all_servers is None:
        s={}
    else:
        s=json.loads(all_servers)
    if server_name not in s or s[server_name] is None:
       s[server_name]={'ip':server_ip,'data':server_monitor_name}
       t=json.dumps(s)
       r.set(all_servers_info_set,t)

################################################
#monitor server detail data
    monitor_modules=[name for _, name, _ in pkgutil.iter_modules(['monitor'])]
    monitor_content={}
    for monitor_module in monitor_modules:
         module_class=eval(monitor_module+"."+monitor_module)()
         data=module_class.display()
         for key in data:
              monitor_content[key]=data[key]
    monitor_content['time']=time.mktime(datetime.datetime.now().timetuple())
    r.set(server_monitor_name,json.dumps(monitor_content))

except Exception,ex:
     logger.exception(ex)





