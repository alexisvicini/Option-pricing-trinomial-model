# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:35:15 2022

@author: vicin
"""
import os, sys
from datetime import datetime, date, timedelta

path = os.getcwd()

#Chemin à modifier selon l'emplacement où se situent les répertoires contenant les fichiers à importer
sys.path.append(path + "\class_modules")
sys.path.append(path + "\data_config")
sys.path.append(path + "\build")
sys.path.append(path + "\convertion_modules")

from Default_dates import *
from conv_str_to_datetime import *

from Node import *
from Tree import *

class Contract():    
        
    def __init__(self, callput = "Call", EU_US = "EU", strike = 100, MaturityDate = TomDate):
        matdate_convert = str_to_datetime(MaturityDate)
        self.MaturityDate = matdate_convert
        self.Strike = strike

        if callput.upper().startswith("C"):
            self.option_type = "Call"
        else:
            self.option_type = "Put"
        
        if not (EU_US.upper().startswith("E")): #Prend en compte différentes entrées possibles pour l'utilisateur en n'obligeant pas un format précis sur la donnée saisie: American, american, US, us, 
            self.option_EA = "American"
        else:
            self.option_EA = "European"

    def PayOff(self, n:Node):
        if self.option_type == "Call":
            return max(n.StockPrice - self.Strike, 0)
        else:
            return max(self.Strike - n.StockPrice, 0)
        

#def PricerRec(n:Node, t:Tree, contract:Contract):
def PricerRec(n, t, contract):
    #Si le prix de l'option est déjà calculé sur le noeud alors retourner la valeur
    if n.hasOptionValue:
        return(n.Optvalue)
    else:
        #Si on arrive à la maturité, alors le prix est égal au payoff
        if n.NextMid == None:
            res = contract.PayOff(n)
        else:
            #Parcours les noeuds NextUp
            if n.NextUp == None:
                upval = 0
            else:
                upval = PricerRec(n.NextUp, t, contract)
                
            #Parcours les noeuds NextDown
            if n.NextDown == None:
                downval = 0
            else:
                downval = PricerRec(n.NextDown, t, contract)
            
            #Calcul de la valeur de l'option pour le noeud mid
            midval = PricerRec(n.NextMid, t, contract)
            
            #Calcul du prix de l'option
            res = (downval * n.Proba_down + upval * n.Proba_up + midval * n.Proba_mid) / t.DF

            # Si l'option est américaine, on retourne le max entre le res et le payoff
            if contract.option_EA == "American":
                res = max(res, contract.PayOff(n))
        n.Optvalue = res
        n.hasOptionValue = True
        return(n.Optvalue)
    
    
def PricerNonRec(trunk:Node, t:Tree, contract:Contract):
        
    n = trunk
    #On parcours les noeuds pour arriver aux noeuds de la maturité
    while not n.NextMid == None:
        n = n.NextMid
    
    tronc = n
    n.Optvalue = contract.PayOff(n)
    
    #Parcours les noeuds NodeUp et NodeDown de la maturitŽ
    while not n.NodeUp == None: 
        n = n.NodeUp
        n.Optvalue = contract.PayOff(n)
    
    n = tronc
    while not n.NodeDown == None:
        n = n.NodeDown
        n.Optvalue = contract.PayOff(n)

    #on recule à une date avant
    while not tronc.PrevNode == None:
        tronc = tronc.PrevNode
        n = tronc
        n.Optvalue = res(n, t, contract)
        #Parcours les noeuds NodeUp et NodeDown
        while not n.NodeUp == None:
            n = n.NodeUp
            n.Optvalue = res(n, t, contract)
        
        n = tronc
        while not n.NodeDown == None:
            n = n.NodeDown
            n.Optvalue = res(n, t, contract)
        
    
    return(n.Optvalue)

#def res(n:Node, t:Tree, contract:Contract):
def res(n, t, contract):

    if n.NextUp == None: 
        upval = 0
    else:
        upval = n.NextUp.Optvalue
    
    if n.NextDown == None:
        downval = 0
    else:
        downval = n.NextDown.Optvalue
    
    
    res = (downval * n.Proba_down + upval * n.Proba_up + n.NextMid.Optvalue * n.Proba_mid) / t.DF
    if contract.option_EA == "American":
        return(max(res, PayOff(n)))
    else:
        return(res)