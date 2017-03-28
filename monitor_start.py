#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import time

cf = ConfigParser.ConfigParser()
CURRENT_DIR = os.path.dirname(__file__)
################################################
RUN_FILE=os.path.abspath(os.path.join(CURRENT_DIR, "monitor.py"))
while True:
    os.system("python "+ RUN_FILE)
    # common config
    COMMON_FILE = os.path.abspath(os.path.join(CURRENT_DIR, "common.conf"))
    cf.read(COMMON_FILE)
    server_monitor_time_interval = cf.get("common", "server_monitor_time_interval")
    time.sleep(server_monitor_time_interval)