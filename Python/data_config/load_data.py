# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:57:46 2022

@author: vicin
"""
import yaml, sys, os
from datetime import datetime, timedelta

path = os.getcwd()

#Chemin à modifier selon l'emplacement où se situent les répertoires contenant les fichiers à importer
sys.path.append(path + "\convertion_modules")

from Default_dates import *
from conv_str_to_datetime import *

def load(path):
    with open(path, 'r') as f:
        file = yaml.load(f) #"file" ->type dictionnaire
        
    Nature = file.get("Nature")
    Type = file.get("Type")
    Maturity_Date = file.get("Maturity_Date")
    Pricing_Date = file.get("Pricing_Date")
    Stock_price = file.get("Stock_price")
    Strike = file.get("Strike")
    Div_Date = file.get("Div_Date")
    Div_Date = str_to_datetime(Div_Date)
    Div_Amount = file.get("Div_Amount")
    Int_rate = file.get("Int_rate")
    Volatility = file.get("Volatility")
    NSteps = file.get("NSteps")
    Multiplicator = file.get("Multiplicator")

    if Pricing_Date == None:
        Pricing_Date = NowDate
    else:
        Pricing_Date = str_to_datetime(Pricing_Date)
        
    if Maturity_Date == None:
        Maturity_Date = TomDate
    else:
        Maturity_Date = str_to_datetime(Maturity_Date)

    if NSteps == None or NSteps == 0:
        NSteps = 1
    else:
        NSteps = int(NSteps)
    """
    for key, value in file.items():
        print(f"{key}: {value}")
    """
    return Nature, Type, Maturity_Date, Pricing_Date, Stock_price, Strike, Div_Date, Div_Amount, Int_rate, Volatility, NSteps, Multiplicator
        