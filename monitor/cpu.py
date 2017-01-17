#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil
class cpu:
    name='cpu'
    def display(self):
	return {self.name:self.calculate()}
    def calculate(self,interval=1):
       cpu=[];
       for percent in psutil.cpu_percent(interval,percpu=True):
	cpu.append({'percent':percent})
       return cpu
