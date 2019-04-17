#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil


class cpu:
    name = 'cpu'
    is_send = 0

    def display(self):
        return {self.name: self.calculate(), 'is_send': self.is_send}

    def calculate(self, interval=1):
        cpu = []
        for percent in psutil.cpu_percent(interval, percpu=True):
            cpu.append({'percent': percent})
            if percent > 90:
                self.is_send = 1
        return cpu
