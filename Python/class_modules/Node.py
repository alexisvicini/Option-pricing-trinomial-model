# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:36:30 2022

@author: vicin
"""
import os, sys
from datetime import datetime, date, timedelta
from math import exp

path = os.getcwd()

#Chemin à modifier selon l'emplacement où se situent les répertoires contenant les fichiers à importer
sys.path.append(path + "\class_modules")
sys.path.append(path + "\data_config")
sys.path.append(path + "\build")
sys.path.append(path + "\convertion_modules")

from Tree import *
from Market import *
from Default_dates import *
      
class Node():
    #def __init__(self, tree:Tree, stockprice = 100, time = NowDate):
    def __init__(self, tree, stockprice = 100, time = NowDate):
        self.StockPrice = stockprice 
        self.t = tree
        self.time = time
        self.NextMid = None
        self.NextUp = None 
        self.NextDown = None 
        self.NodeUp = None
        self.NodeMid = None
        self.NodeDown = None
        self.PrevNode = None #Noeuf précédent (par défaut None)
        self.Proba_down = 0
        self.Proba_up = 0
        self.Proba_mid = 0
        self.Proba_cum = 1
        self.hasOptionValue = False
        self.Optvalue = 0
        self.forward = 0
                
    def ComputeProba(self):
        esp = self.StockPrice * self.t.DF - self.t.market.Div_Amount
        var = (self.StockPrice ** 2) * exp(2 * self.t.market.Rate * self.t.deltaT) * (exp((self.t.market.Volatility ** 2) * self.t.deltaT) - 1)
        
        #Calcul des probabilités
        self.Proba_down = ((self.NextMid.StockPrice ** (-2)) * (var + esp ** 2) - 1 - (self.t.alpha + 1) * (self.NextMid.StockPrice ** (-1) * esp - 1)) / ((1 - self.t.alpha) * (self.t.alpha ** (-2) - 1))
        self.Proba_up = (self.NextMid.StockPrice ** (-1) * esp - 1 - (self.t.alpha ** (-1) - 1) * self.Proba_down) / (self.t.alpha - 1)
        self.Proba_mid = 1 - self.Proba_down - self.Proba_up
        
        #Calcul des probabilités cumulées
        if not self.NextUp == None:
            self.NextUp.Proba_cum += self.Proba_cum * self.Proba_up
        if not self.NextDown == None:
            self.NextDown.Proba_cum +=  self.Proba_cum * self.Proba_down
        if not self.NextMid == None:
            self.NextMid.Proba_cum += self.Proba_cum * self.Proba_mid


    #def SetNextMid(self, node:Node):
    def SetNextMid(self, node):
        self.NextMid = node
        
    #def SetNextUp(self, node:Node):
    def SetNextUp(self, node):
        self.NextUp = node
    
    #def SetNextDown(self, node:Node):
    def SetNextDown(self, node):
        self.NextDown = node

    def Forward(self):
        return(self.StockPrice * self.t.DF - self.t.market.Div_Amount)
    
    #def BuildNodes(self, n2:Node, t:Tree, time):
    def BuildNodes(self, n2, t, time):
        n = NextMidNode(n2, t, time)
        self.NextMid = n      
        self.NextUp = moveUp(n, t, time)
        self.NextDown = moveDown(n, t, time)
        
        connexionV(self)
        self.ComputeProba()
    
#def connexionV(n:Node):
def connexionV(n):
    n.NextMid.NodeUp = n.NextUp
    n.NextMid.NodeDown = n.NextDown
    n.NextUp.NodeDown = n.NextMid
    n.NextDown.NodeUp = n.NextMid

#def CreateNodeTrunk(n:Node, t:Tree, time):
def CreateNodeTrunk(n, t, time):
    #Création des noeuds Next
       
    if n.NextMid == None:
        n.NextMid = Node(t, n.Forward(), time)
        
    if n.NextUp == None:
        n.NextUp = Node(t, n.Forward() * n.t.alpha, time)
    
    if n.NextDown == None:
        n.NextDown = Node(t, n.Forward() / n.t.alpha, time)

    n.NextMid.PrevNode = n

    #Etablir les connexions verticales entre les noeuds
    connexionV(n)
    
    #Calcul des probas des branches
    n.ComputeProba()

#def NextMidNode(n:Node, t:Tree, time):
def NextMidNode(n, t, time):
       
    #while (is_none == 0 and n.Forward() > (n.StockPrice * (1 + t.alpha) / 2)):
    while n.Forward() > (n.StockPrice * (1 + t.alpha) / 2):
        n = moveUp(n, t, time)

    while n.Forward() < n.StockPrice * (1 + 1 / t.alpha) / 2:
        n = moveDown(n, t, time)
    return n

#def moveUp(n:Node, t:Tree, time):
def moveUp(n, t, time):
    if n.NodeUp== None:    
        n.NodeUp = Node(t, n.StockPrice * t.alpha, time)
    return(n.NodeUp)

#def moveDown(n:Node, t:Tree, time):
def moveDown(n, t, time):
    if n.NodeDown == None:
        n.NodeDown = Node(t, n.StockPrice / t.alpha, time)
    return(n.NodeDown)


