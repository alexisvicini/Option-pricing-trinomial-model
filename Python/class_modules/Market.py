# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:06:10 2022

@author: vicin
"""

class Market:
    def __init__(self, S = 100, DivDate = None, DivAmount = None, r = 0.01, vol = 0.1):
        self.StockPrice = float(S)
        self.Div_Date = DivDate
        self.Div_Amount = float(DivAmount)
        self.Rate = float(r)
        self.Volatility = float(vol)