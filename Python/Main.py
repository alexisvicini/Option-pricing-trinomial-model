# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:07:23 2022

@author: vicin
"""

####################
#Import des modules#
####################

import os, sys, time

#Récupération du répertoire courant du fichier "main"
path = os.path.dirname(__file__)
os.chdir(path) #Affectation du chemin comme répertoire de travail

#Ajout des chemins nécessaires à l'import des fichiers dans "sys"
sys.path.append(path + "\class_modules")
sys.path.append(path + "\data_config")
sys.path.append(path + "\build")
sys.path.append(path + "\convertion_modules")

"""

IL PEUT ETRE IMPORTANT DE RUN LE FICHIER "Node.py" AVANT
LANCER LE FICHIER "Main.py" POUR PERMETTRE DE RECONNAITRE
LA FONCTION "CreateNodeTrunk"

"""

from Node import *
from Tree import *
from Contract import *
from Market import *
from load_data import * 
from conv_str_to_datetime import *

#############
# Load Data #
#############
"""
Les données intiiales sont situées dans un document .yaml et peuvent être modifiées directement à l'intérieur.
Le fichier se nomme "config.yaml" et se trouve sous le répertoire "data_config"
"""

#Chemin permettant d'accéder au fichier de configuration avec les données initiales à importer
config_path = path + "\data_config\config.yaml"

callput, EU_US, Maturity_Date, Pricing_Date, Stock_price, Strike, Div_Date, Div_Amount, Int_rate, Volatility, Nb_Steps, Multiplicator = load(config_path )

#################
# Print of data #
#################

print("***********\n* DONNEES *\n***********")
print("\nCall / Put: " + str(callput))
print("EU / US: " + str(EU_US))
print("Maturity date: " + str(Maturity_Date))
print("Pricing date: " + str(Pricing_Date))
print("Stock price: " + str(Stock_price))
print("Dividend amount: " + str(Div_Amount))
print("Dividend date: " + str(Div_Date))
print("Number of step(s): " + str(Nb_Steps) + '\n')

################################################
# Construction d'un noeud racine et de l'arbre #
################################################

#Construction des objets market de classe Market de contract de classe Contract
market = Market(Stock_price, Div_Date, Div_Amount, Int_rate, Volatility)
contract = Contract(callput, EU_US, Strike, Maturity_Date)

#Construction de l'arbre, d'un noeud racine et affectation de la racine à cet arbre
tree = Tree(market, Pricing_Date, Maturity_Date, Nb_Steps, Multiplicator)
root = Node(tree, Stock_price, Pricing_Date)
tree.SetRootTree(root)

print("**************\n* BUILD TREE *\n**************")

#Construction de l'arbre et de tous les noeuds
start = time.time()
tree.buildTree()
tps_build_tree = time.time() - start
print("\nTemps nécessaire pour construire l'arbre: " + str(round(tps_build_tree, 4)) + "s")

print("\n***********\n* PRICING *\n***********")

start = time.time()
res = round(PricerRec(root, tree, contract), 4)
tps_pricer = time.time() - start
print("\nTemps nécessaire pour le pricing récursif: " + str(round(tps_pricer, 4)) + "s")
print("\nValeur du " + str(callput) + " " + str(EU_US) + ": " + str(res) + '\n\n')



start = time.time()
res = round(PricerNonRec(root, tree, contract), 4)
tps_pricer = time.time() - start
print("\nTemps nécessaire pour le pricing non récursif: " + str(round(tps_pricer, 4)) + "s")
print("\nValeur du " + str(callput) + " " + str(EU_US) + ": " + str(res) + '\n\n')
