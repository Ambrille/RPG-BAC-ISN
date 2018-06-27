# -*- coding: utf-8 -*-

import pygame
import os
from Save import *

class SDict(dict):
    """
    Fait qu'on peut faire aussi bien
    
    a = SDict()
        a.b = 0
    que
        a["b"] = 0
    """
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, valeur):
        self[attr] = valeur

class ModulesClass(SDict):

    def __init__(self, *args):
        super(ModulesClass, self).__init__(*args)

    def default(self):
        #global Axe_y, Axe_x
        self.Axe_y = -5
        self.Axe_x = 255
        self.Axe_xINIT = 255
        self.Axe_yINIT = -5
        self.Deplacement = ""

        self.DialogueOn = False
        self.ActiveDialogue = None

        self.Diff_x = 0
        self.Diff_y = 0
        
        #---PNJ---#
        #---#
        
        #if direction == 'haut':
            #self.Axe_y += 1
        #elif direction == 'bas':
            #self.Axe_y -= 1
       # elif direction == 'gauche':
            #self.Axe_x -= 1
        #elif direction == 'droite':
            #self.Axe_x += 1

        #return self.Axe_x, self.Axe_y

class QuestClass(SDict):

    def __init__(self, *args):
        super(QuestClass, self).__init__(*args)

    def default(self):
        #Maison Perso#
        self.Maman = 0
        self.Bento = 0
        #Personnages#
        self.CharlesA = 0
        self.Ambre = 0
        self.Timothee = 0
        self.Soana = 0
        self.Hippolyte = 0
        self.Jean = 0
        self.CharlesV = 0
        self.Sacha = 0
        self.Josephine = 0
        self.Arno = 0
        self.Paul = 0
        self.Amelie = 0
        self.Victor = 0
        self.Tanguy = 0
        self.Adrien = 0
        self.Nicolas = 0
        self.Julie = 0
        self.Ewan = 0
        self.Ryan = 0
        self.LeoG = 0
        self.Marin = 0
        self.VictorA = 0
        self.Alexis = 0
        self.Emma = 0
        self.Victoria = 0
        self.VictorD = 0
        self.Ines = 0
        self.Julien = 0
        self.Clara = 0
        self.Thomas = 0
        self.Martin = 0
        self.Marie = 0
        self.Barthelemy = 0
        self.Fabien = False
        
        

class MapClass(SDict):

    def __init__(self, *args):
        super(MapClass, self).__init__(*args)

    def default(self):
        self.CurrentMapName = "ChambreTest"
### CHARGER ###

if not os.path.exists("Save/"):
    os.mkdir("Save/")

#---QUEST---#
Fichier_sauvegarde = "Save/sauvegarde.json"
try:
    Quest = QuestClass(charger_fichier(Fichier_sauvegarde))
except (OSError, IOError) as e:  # Pas de sauvegarde
    if isinstance(e, ValueError):
        print("FICHIER sauvegarde.json CORROMPU")
    Quest = QuestClass()
    Quest.default()

#---MODULES---#
Fichier_sauvegarde_module = "Save/sauvegarde_module.json"
try:
    Modules = ModulesClass(charger_fichier(Fichier_sauvegarde_module))
except (OSError, IOError) as e:  # Pas de sauvegarde
    if isinstance(e, ValueError):
        print("FICHIER sauvegarde_module.json CORROMPU")
    Modules = ModulesClass()
    Modules.default()

#---MAP---#
Fichier_sauvegarde_Map = "Save/sauvegarde_map.json"
try:
    Maps = MapClass(charger_fichier(Fichier_sauvegarde_Map))
except (OSError, IOError) as e:
    if isinstance(e, ValueError):
        print("FICHIER sauvegarde_map.json CORROMPU")
    Maps = MapClass()
    Maps.default()

def supprimer_tout():
    try:
        os.remove(Fichier_sauvegarde)
    except:
        pass
    try:
        os.remove(Fichier_sauvegarde_module)
    except:
        pass
    try:
        os.remove(Fichier_sauvegarde_Map)
    except:
        pass
    Quest.default()
    Modules.default()
    Maps.default()
