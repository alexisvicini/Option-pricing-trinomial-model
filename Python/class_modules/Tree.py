# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 14:37:05 2022

@author: vicin
"""
import os, sys
from math import sqrt, exp

path = os.getcwd()

#Chemin à modifier selon l'emplacement où se situent les répertoires contenant les fichiers à importer
sys.path.append(path + "\class_modules")
sys.path.append(path + "\data_config")
sys.path.append(path + "\build")
sys.path.append(path + "\convertion_modules")

from Node import *
from Node import CreateNodeTrunk
from Market import *
from conv_str_to_datetime import *
from Default_dates import *


class Tree():
    def __init__(self, market:Market, pricingDate = NowDate, matuDate = TomDate, nsteps = 1, mult = sqrt(3)):
        self.PricingDate = str_to_datetime(pricingDate)
        self.MatuDate = str_to_datetime(matuDate)
        self.NSteps = int(nsteps)
        self.multiplicator = mult 
        timelapse = self.MatuDate - self.PricingDate
        self.deltaT = float((timelapse.days / self.NSteps) / 365)
        self.market = market
        self.Root = 0 #Valeur initiale (par défaut) de la racine 
        self.alpha = exp((self.market.Rate * self.deltaT) + market.Volatility * float(self.multiplicator) * sqrt(self.deltaT))
        self.DF = exp(self.market.Rate * self.deltaT)
        self.div = 0

    #def SetRootTree(self, node:Node):
    def SetRootTree(self, node):
        self.Root = node
        
    def buildTree(self):
        trunk = self.Root
        time = self.PricingDate
        dt = self.deltaT * 365
        
        #Parcours des nbsteps pour construire l'arbre
        for i in range(self.NSteps):
            diff_time = (self.market.Div_Date - time).days
            diff_time_dt = ((time + timedelta(days = dt)) - self.market.Div_Date).days

            #Condition pour le dividende a l'ex date
            if (diff_time > 0 and diff_time_dt > 0):
                self.div = self.market.Div_Amount
            else:
                self.div = 0

            #Incrementation du temps
            time += timedelta(days = dt)
            
            #Creation des noeuds next pour le noeud du Trunk
            CreateNodeTrunk(trunk, self, time)

            #Récupère dans n le tronc, qui sert de noeud curseur pour parcourir vers le haut
            n = trunk
            #Parcours les noeuds en haut de n
            while not n.NodeUp == None:
                n.NodeUp.NodeDown = n
                n = n.NodeUp
                n.BuildNodes(n.NodeDown.NextUp, self, time)

            n = trunk
            #Parcours les noeuds en bas de n
            while not n.NodeDown == None:
                n.NodeDown.NodeUp = n
                n = n.NodeDown
                n.BuildNodes(n.NodeUp.NextDown, self, time)

            #Prunning
            Pruning(trunk)
            trunk = trunk.NextMid
            
            
#def Clear(n:Node):       
def Clear(n):
    if not n.NextDown == None:
        if n.NextDown.Proba_cum < 2 * 10 ^ (-8):
            n.NextDown = None
            n.NextMid.NodeDown = None
            
    if not n.NextUp == None:
        if n.NextUp.Proba_cum < 2 * 10 ^ (-8):
            n.NextUp = None
            n.NextMid.NodeUp = None
        
#def Pruning(trunk:Node):
def Pruning(trunk):
    n = trunk
    while not n.NodeUp == None:
        n = n.NodeUp
    Clear(n)
    
    n = trunk
    while not n.NodeDown == None:
        n = n.NodeDown
    Clear(n)
