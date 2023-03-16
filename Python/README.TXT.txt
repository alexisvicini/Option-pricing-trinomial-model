****************************************************************************************
* Présentation des différents répertoires et fichiers pour le projet "Arbre trinomial" *
****************************************************************************************

Note importante: L'utilisation des modules "os" et "sys" dans ce projet permettent initialement la localisation du fichier "main" au lancement de ce même fichier et, par la suite, 
l'ajout de répertoires prédéfinis où se trouvent l'enemble des autres fichiers nécessaires à la bonne exécution de ce fichier. Nous vous prions ainsi de ne pas modifier
le nom des sous-répertoires du projet, ceci conduisant directement à une erreur lors de l'import des fichiers.

***************
* data_config *
***************

"data_config" présente deux fichiers "config" et "load_data".

- Dans "config", l'utilisateur a la possibilité de saisir et modifier toutes les données initiales du projet (nature et type de l'option, date de pricing, maturité, prix spot et prix d'exercice, etc.)
- Dans "load_data", le code présent est utilisé pour extraire les données de "config" et les utiliser par la suite dans les autres fichiers.


**********************
* convertion_modules *
**********************

"convertion_modules" présente deux fichiers "conv_str_to_datetime" et "Default_dates".

Les deux fichiers sont des fichiers de formattage. "conv_str_to_datetime" permet de forcer le type d'une variable en convertisant explicitement une chaîne de caractère en 
datetime pour, par la suite, manipuler des écarts entre dates.
Le second fichier "Default_dates" est un fichier ayant pour but d'initialiser et affecter des valeurs par défaut à nos variables initiales (présentes dans "config") si manquantes.


*****************
* class_modules *
*****************

"class_modules" abrite les quatre fichiers racines de notre projet correspondant aux modules de classe: Contract, Market, Node et Tree.
