# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 14:15:31 2022

@author: vicin
"""
from datetime import datetime, date, timedelta
from conv_str_to_datetime import *

now = datetime.now()
NowDate = str_to_datetime(now.strftime("%d/%m/%Y"))
TomDate = NowDate + timedelta(days = 1)