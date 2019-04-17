#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import psutil
class memory:
    name='memory'
	is_send=0
    def display(self):
      return {self.name:self.calculate(),'is_send':self.is_send} 
    def calculate(self):
       phymem=psutil.virtual_memory()
       swapmem=psutil.swap_memory()
	   if phymem.percent>95:
          self.is_send=1
       return {
		'physical':{
			'percent':phymem.percent,
	 		'available':self.size_format(phymem.available),
			'used':self.size_format(phymem.used),
			'total':self.size_format(phymem.total),
			'free':self.size_format(phymem.free),
			'unit':'M'
		    	},
		'swap':{	   	
			'total':self.size_format(swapmem.total),
			'percent':swapmem.percent,
			'used':self.size_format(swapmem.used),
			'free':self.size_format(swapmem.free),
			'unit':'M'
			}
	       }
    def size_format(self,b):
        return float('%1.f' % float(b/1024/1024))
     
