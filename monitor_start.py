#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import time

cf = ConfigParser.ConfigParser()
current_dir = os.path.dirname(__file__)
################################################
run_file=os.path.abspath(os.path.join(current_dir, "monitor.py"))
while True:
    os.system("python " + run_file)
    # common config
    common_conf_file = os.path.abspath(os.path.join(current_dir, "common.conf"))
    cf.read(common_conf_file)
    server_monitor_time_interval = cf.get("common", "server_monitor_time_interval")
    time.sleep(float(server_monitor_time_interval))