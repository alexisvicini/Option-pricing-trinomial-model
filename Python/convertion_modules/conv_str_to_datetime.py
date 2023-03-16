# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 16:06:55 2022

@author: vicin
"""
from datetime import datetime
def str_to_datetime(date_str):
    format_list = ["%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y %H:%M:%S", "%d/%m/%y %H:%M:%S", "%m/%d/%Y %H:%M:%S", "%m/%d/%y %H:%M:%S", "%Y-m-d %H:%M:%S"]
    for f in format_list:
        try:
            date_str = datetime.strptime(date_str, f)
            break
        except Exception as e:
            continue
    return date_str
