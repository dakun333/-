#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 19:13:57 2018

@author: zsk
"""
import logging,sys

class MyLogger:
    def __init__(self):
        self.logger = logging.getLogger('my_logger')
        self.fromatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
           
        self.file_handler = logging.FileHandler('my_logger.log')
        self.file_handler.setFormatter(self.fromatter)
        
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setFormatter(self.fromatter)
        
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        
    
    def closeLog(self):
        self.logger.removeHandler(self.file_handler)
        self.logger.removeHandler(self.console_handler)
        
if __name__ == "__main__":
    a = MyLogger()
    b,c = a.createLog()
    a.logger.debug("Message is debug")
    a.logger.info("Message is info")
    a.logger.error("Message is error")
    a.closeLog()
    
        