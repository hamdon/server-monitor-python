#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import psutil
import os


class disk:
    name = 'disk'
    is_send = 0

    def display(self):
        return {self.name: self.calculate(), 'is_send': self.is_send}

    def calculate(self):
        parts = psutil.disk_partitions()
        partitions = []

        for part in parts:
            if not 'loop' in part.device:
                usage = psutil.disk_usage(part.mountpoint)
                inodes = os.statvfs(part.mountpoint)
                if usage.percent > 90:
                    self.is_send=1
                partitions.append({
                   'device': part.device,
                   'mountpoint': part.mountpoint,
                   'total': self.size_format(usage.total),
                   'used': self.size_format(usage.used),
                   'free': self.size_format(usage.free),
                   'percent': usage.percent,
                   'unit':self.size_unit(usage.total),
           'inode_total_number':inodes.f_files,
           'inode_free_number':inodes.f_ffree
                })

        return partitions
    
    def size_unit(self,b):
        if b < 1000:
            return 'B'
        elif 1000 <= b < 1000000:
            return 'KB'
        elif 1000000 <= b < 1000000000:
            return 'MB'
        elif 1000000000 <= b < 1000000000000:
            return 'GB'
        elif 1000000000000 <= b:
            return 'TB'

    def size_format(self,b):
        result='0'
        if b < 1000:
            result='%i' % b
        elif 1000 <= b < 1000000:
            result='%.1f' % float(b/1000)
        elif 1000000 <= b < 1000000000:
            result='%.1f' % float(b/1000000)
        elif 1000000000 <= b < 1000000000000:
            result='%.1f' % float(b/1000000000)
        elif 1000000000000 <= b:
            result='%.1f' % float(b/1000000000000)
        return float(result)
