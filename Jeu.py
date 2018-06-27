# -*- coding: utf-8 -*-

import pygame, sys, math, random
from pygame.locals import *

from Textures import *
from Classes import *
from Mapping import *
from PNJs import *
from Menu import *
from Save import*

pygame.mixer.init(44100, 0, 2, 2048)

pygame.init()

def jouer_musique(nom, infini=False):
    pygame.mixer.music.load("Musique/Music/%s.mp3" % nom)
    pygame.mixer.music.play(loops=-1 if infini else 0)

def charger_son(nom):
    return pygame.mixer.Sound("Musique/Sound/%s.wav" % nom)

def jouer_son(son, volume):
    s = son.play(loops=0)
    s.set_volume(volume)

def ChargerFenetreJeu():
    
    global Fenetre_Jeu, Hauteur_Jeu, Largeur_Jeu, Titre_Jeu
    
    Hauteur_Jeu, Largeur_Jeu = 600, 800
    Titre_Jeu = "Bac RPG TTS"
    pygame.display.set_caption(Titre_Jeu)
    Fenetre_Jeu = pygame.display.set_mode((Largeur_Jeu, Hauteur_Jeu), HWSURFACE|DOUBLEBUF)

ChargerFenetreJeu()
#---#
#Chambre = Mapping.Charger_Map("maps/ChambreTest.map")
#Salon = Mapping.Charger_Map("maps/SalonTest.map")
#---#

AllPortailsFIXE = {
    # NOUVEAU: On peut mettre un tuple (x,y,z...) dans les coordonnées d'origines, qui signifie soit l'un soit l'autre
    #Chambre//Salon
    'StairsChambreToSalon' : ['ChambreTest', 'SalonTest', [9, 6], [0, 3], None],
    'StairsSalonToChambre' : ['SalonTest', 'ChambreTest', [8, 3], [0, 0], None],
    #Salon//Ville de Depart
    'SalonToDepart' : ['SalonTest', 'Foret13', [(5,6), 12], [-16, -5], "Porte"],
    'DepartToSalon' : ['Foret13', 'SalonTest', [(21,22), 18], [0, 3], "Porte"],
    #Labo//Ville de Depart
    'DepartToLabo' : ['Foret13', 'Labo7', [(38,39), 19], [15, 0], "Porte"],
    'LaboToDepart' : ['Labo7', 'Foret13', [(7,8), 16], [-16, -5], "Porte"],
    #RandomHouse//Ville de Depart
    'RandSalonToDepart' : ['randomsalon', 'Foret13', [(5,6), 11], [-16, -5], "Porte"],
    'DepartToRandSalon' : ['Foret13', 'randomsalon', [(27,28), 24], [6, 10], "Porte"],
    #DepartToEglise1#
    'Eglise1ToDepart1' : ['Eglise1', 'Foret13', [(15,16), 18], [-16, -4], "Porte"],
    'DepartToEglise1' : ['Foret13', 'Eglise1', [(21,22), 33], [-10, 12], "Porte"],
    #Eglise2ToEglise1#
    'Eglise1ToEglise21' : ['Eglise1', 'Eglise2', [(20,21), 9], [-3, 12], "Echelle"],
    'Eglise2ToEglise11' : ['Eglise2', 'Eglise1', [(10,11), 9], [-10, 12], "Echelle"],
    #VilleToEglise1#
    'Eglise2ToVille1' : ['Eglise2', 'Ville5', [(15,16), 18], [-16, -3], None],
    'VilleToEglise21' : ['Ville5', 'Eglise2', [(45,46), 38], [14, 18], None],
}

AllPortails = {}
for nom, data in AllPortailsFIXE.items():
    # Ce truc compliqué transforme les coordonnées (x,y) ou x et y ne sont pas des tuple en tuple
    # par exemple:
    # (1, 2) ==> ((1,), (2,))
    # ((1, 2), 3) ==> ((1, 2), (3,))
    data[2] = (lambda x, y: ((x if isinstance(x, tuple) else (x,)), (y if isinstance(y, tuple) else (y,))))(*data[2])
    AllPortails[nom] = data

#---#

#---PERSO---#
Nom = "LeoG"
Current = "Face0"
ChoixPerso = 0
Pos_PxFIXE = 0
Pos_PyFIXE = 0
TP = False
#---#


#---DIALOGUE BOX---#
DialogueBox = pygame.image.load("Textures/Detail/DialogueBox.png")
DialogueBox = pygame.transform.scale(DialogueBox, (760, 120))
DialogueSurface = pygame.Surface((760, 150), pygame.HWSURFACE|pygame.SRCALPHA)
DialogueSurface.blit(DialogueBox, (0, 0))
DialogueSurfaceLargeur, DialogueSurfaceHauteur = 760, 150
#---#



#########################################################################
### TOUS LES DIALOGUES ET PNJs SONT MAINTENANT DANS LE FICHIER PNJ.py ###
#########################################################################

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#Pos_Px = (Largeur_Jeu/2 - Modules.Axe_x ) / Background.TailleGrid
#Pos_Py = (Hauteur_Jeu/2 - Modules.Axe_y +25) / Background.TailleGrid

def play():

    global AllPortails
    global Nom, Current, ChoixPerso, Pos_PxFIXE, Pos_PyFIXE, TP
    global DialogueBox, DialogueSurface, DialogueSurfaceLargeur, DialogueSurfaceHauteur

    #---MAPS---#
    #MapName = Maps.CurrentMapName
    Mapping = MappingClass()
    Map = Mapping.Charger_Map("maps/{}.map".format(Maps.CurrentMapName))
    #CurrentMap = "{}".format(MapName)
    Terrain = Map[0]
    Decor = Map[1]
    #----------#

    #---REDMARK---#
    REDMARK = "Close"
    #---#

    #---SONS---#
    # son.play(0, 0) #
    bruit_de_porte = charger_son("porte")
    bruit_de_echelle = charger_son("echelle")
    #---#

    Pos_P = 0
    Dep_PyH, Dep_PyB, Dep_PxD, Dep_PxG = 0, 0, 0, 0
    Continuer = True

    # Démarrer le son
    jouer_musique("Ambiance", infini=True)

    pygame.key.set_repeat(1,10)
    
    while Continuer:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Continuer = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Continuer = False
                elif event.key == pygame.K_KP4:
                    NomSave = input("Nom Save:")
                    ecrire_fichier("Save/" + NomSave + ".json", Quest)
                    ecrire_fichier("Save/" + NomSave + ".json", Modules)
                elif event.key == pygame.K_KP5:
                    NomSave = input("Nom Save:")
                    charger_fichier("Save/" + NomSave + ".json")
                    
                elif event.key == pygame.K_z or event.key == pygame.K_UP and not Modules.DialogueOn:
                    Modules.Deplacement = "haut"
                    Pos_P = 1
                    #Modules.Mouvement('haut')
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN and not Modules.DialogueOn:
                    Modules.Deplacement = "bas"
                    Pos_P = 2
                    #Modules.Mouvement('bas')
                elif event.key == pygame.K_q or event.key == pygame.K_LEFT and not Modules.DialogueOn:
                    Modules.Deplacement = "gauche"
                    Pos_P = 3
                    #Modules.Mouvement('gauche')
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT and not Modules.DialogueOn:
                    Modules.Deplacement = "droite"
                    Pos_P = 4
                    #Modules.Mouvement('droite')
                elif event.key == pygame.K_KP1 and not Modules.DialogueOn:
                    REDMARK = "Open"
                elif event.key == pygame.K_KP2 and not Modules.DialogueOn:
                    REDMARK = "Close"
                elif event.key == pygame.K_KP3 and not Modules.DialogueOn:
                    CurrentMap = input("CurrentMap :")

            elif event.type == pygame.KEYUP:
                
                Modules.Deplacement = ""
                if event.key == pygame.K_p:
                    ChoixPerso += 1
                    if ChoixPerso == len(Gestuel.Personnages):
                        ChoixPerso = 0
                    #Nom = Gestuel.Personnages(ChoixPerso)
                    Nom = Gestuel.Personnages[ChoixPerso]

                elif event.key == pygame.K_RETURN:
                    if Modules.DialogueOn:
                        if Modules.ActiveDialogue.Page < len(Modules.ActiveDialogue.Texte) - 1:
                            Modules.ActiveDialogue.Page += 1
                        else:
                            Modules.DialogueOn = False
                            Modules.ActiveDialogue.Page = 0
                            Modules.ActiveDialogue = None
                            for npc in NPC.AllNPCs:
                                npc.Current = npc.CurrentInit
                            
                    else:
                        for npc in NPC.AllNPCs:
                            NPC_x = npc.X / Background.TailleGrid
                            NPC_y = npc.Y / Background.TailleGrid

                            if Pos_Px >= NPC_x - 1 and Pos_Px <= NPC_x + 2 and Pos_Py >= NPC_y and Pos_Py <= NPC_y + 2 and npc.Surface == Maps.CurrentMapName:
                                #print("NPC_y", NPC_y)
                                #print("Pos_Py", Pos_Py)

                                #QUEST BEFORE#
                                if npc.Name == "Ambre":
                                    if Quest.Bento == 2:
                                        npc.Dialogue = Dialogue(Texte = DAmbre3)
                                        Quest.Bento = 3
                                    if Quest.Bento == 1:
                                        npc.Dialogue = Dialogue(Texte = DAmbre2)
                                        Quest.Bento = 2
                                if npc.Name == "Julien":
                                    if Quest.Julien == 1:
                                        npc.Dialogue = Dialogue(Texte = DJulien2)
                                    else:
                                        Quest.Julien = 1
                                if npc.Name == "VictorD":
                                    Mots = CharlesARandom(npc.Name)
                                    npc.Dialogue = Dialogue(Texte = [("*fixe votre poche sournoisement* ...","Regardez {}!".format(Mots[0])), ("vous vous retournez","Vous venez de perdre {}.".format(Mots[1]))])
                                
                                        
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                #if npc.Name == "Ambre":
                                if npc.Name == "Ines":
                                    if Quest.Bento == 2 or Quest.Bento == 3:
                                        npc.Dialogue = Dialogue(Texte = DInes3)
                                        
                                if npc.Name == "CharlesA":
                                    npc.Dialogue = Dialogue(Texte = CharlesARandom(npc.Name))
                                    
                                if npc.Name == "Fabien":
                                    if Quest.Fabien == True:
                                        npc.Dialogue = Dialogue(Texte = DFabien2)
                                    else:
                                        Quest.Fabien = True
                                        
                                #DIALOGUE BASE#
                                if Current == "Dos0" and NPC_y > (Pos_Py-2):
                                    Modules.DialogueOn = True
                                    Modules.ActiveDialogue = npc.Dialogue
                                    npc.Current = "Face0"
                                if Current == "Face0" and NPC_y < Pos_Py:
                                    Modules.DialogueOn = True
                                    Modules.ActiveDialogue = npc.Dialogue
                                    npc.Current = "Dos0"
                                if Current == "Gauche0" and NPC_x < Pos_Px:
                                    Modules.DialogueOn = True
                                    Modules.ActiveDialogue = npc.Dialogue
                                    npc.Current = "Droite0"
                                if Current == "Droite0" and NPC_x > Pos_Px:
                                    Modules.DialogueOn = True
                                    Modules.ActiveDialogue = npc.Dialogue
                                    npc.Current = "Gauche0"
                                #---#
                                    
                                #QUEST AFTER#
                                    
                                if npc.Name == "Ines":
                                    if Quest.Maman == 0:
                                        Quest.Maman = 1
                                        Quest.Bento = 1
                                        npc.Dialogue = Dialogue(Texte = DInes2)
                                
                                    
                                    
                            
        pygame.time.wait(1)
        if Modules.Deplacement == "haut":
            if not Background.Obs((round(Pos_Px+float(0.4)), math.floor(Pos_Py))) and not Background.Obs((round(Pos_Px-float(0.4)), math.floor(Pos_Py))):
                Modules.Axe_y += 1.5
                Modules.Axe_yINIT += 1.5
        elif Modules.Deplacement == "bas":
            if not Background.Obs((round(Pos_Px+float(0.4)), math.ceil(Pos_Py-float(0.3)))) and not Background.Obs((round(Pos_Px-float(0.4)), math.ceil(Pos_Py-float(0.3)))):
                Modules.Axe_y -= 1.5
                Modules.Axe_yINIT -= 1.5
        elif Modules.Deplacement == "gauche":
            if not Background.Obs((math.floor(Pos_Px), round(Pos_Py-float(0.4))))and not Background.Obs((math.floor(Pos_Px), round(Pos_Py+float(0.1)))):
                Modules.Axe_x += 1.5
                Modules.Axe_xINIT += 1.5
        elif Modules.Deplacement == "droite":
            if not Background.Obs((math.ceil(Pos_Px), round(Pos_Py-float(0.4)))) and not Background.Obs((math.ceil(Pos_Px), round(Pos_Py+float(0.1)))):
                Modules.Axe_x -= 1.5
                Modules.Axe_xINIT -= 1.5

        Pos_Px = (Largeur_Jeu/2 - Modules.Axe_x ) / Background.TailleGrid
        Pos_Py = (Hauteur_Jeu/2 - Modules.Axe_y +25) / Background.TailleGrid
        #print(math.ceil(Pos_Px), round(Pos_Py))
        Fenetre_Jeu.fill((0, 0, 0))

        #----PORTAIL----#
        #DicoPortail = {"
        #for Portail in DicoPortail:
                
        #----CREATION MAP----#

            #------------# VERSION COMPLEXE (+Mapping.py)
        #Fenetre_Jeu.blit(Terrain, (Modules.Axe_x, Modules.Axe_y))
        
        
        #-----PERSO-----#
        Gesture = Gestuel.ChargerGesture(Nom)
        LocPerso = [(round(Pos_Px)), math.floor((Pos_Py)+1)]
        LocPerso2 = [(round(Pos_Px)), math.floor(Pos_Py)+2]
        LocPerso3 = [(round(Pos_Px)), math.floor((Pos_Py))]
        LocPerso4 = [(round(Pos_Px)), math.floor(Pos_Py)-1]

        for nomPortail, Portail in AllPortails.items():
            portail_origin, portail_dest, portail_coordonnes, portail_destination, portail_type = Portail
            if (LocPerso3[0] in portail_coordonnes[0] and LocPerso3[1] in portail_coordonnes[1]) \
                                                               and Maps.CurrentMapName == portail_origin:
                if portail_type == "Porte":
                    # le portail est une porte
                    jouer_son(bruit_de_porte, 0.2)
                elif portail_type == "Echelle":
                    jouer_son(bruit_de_echelle, 0.1)
                print(nomPortail)
                Maps.CurrentMapName = str(portail_dest)
                #CurrentMap = portail_dest
                #print(str(portail_dest))
                Background.Obstacle = []
                Mapping.ObstacleDecor = []
                Background.ObstaclePNJ = []
                Mapping.DecorListe = []
                Modules.Diff = portail_destination
                #print(LocPerso3)
                #print(Modules.Diff)
                Modules.Axe_x = Modules.Axe_xINIT + Modules.Diff[0]*Background.TailleGrid
                #print(Modules.Axe_x, Modules.Axe_xINIT)
                Modules.Axe_y = Modules.Axe_yINIT + Modules.Diff[1]*Background.TailleGrid
                #print(Modules.Axe_y, Modules.Axe_yINIT)
                Map = Mapping.Charger_Map("maps/{}.map".format(Maps.CurrentMapName))
                Terrain = Map[0]
                #Decor = Map[1]

        LocPerso = [(round(Pos_Px)), math.floor((Pos_Py)+1)]
        LocPerso2 = [(round(Pos_Px)), math.floor(Pos_Py)+2]
        LocPerso3 = [(round(Pos_Px)), math.floor((Pos_Py))]
        LocPerso4 = [(round(Pos_Px)), math.floor(Pos_Py)-1]
                
        Fenetre_Jeu.blit(Terrain, (Modules.Axe_x, Modules.Axe_y))
        #print(Modules.Axe_y, Pos_PyFIXE)
        
        #LocPerso3 = [(round(Pos_Px)), math.floor(Pos_Py)]
        #print(LocPerso, LocPerso2, LocPerso3)
        #print(Gesture[Current])
        #print("A", LocPerso2)
        #print("B", LocPerso)
        #Fenetre_Jeu.blit(Gesture[Current], (Largeur_Jeu/2 -16, Hauteur_Jeu/2 -16))
        
        if Modules.Deplacement == "haut":
            if  0<Dep_PyH<25:
                Current = "Dos1"
            elif 25<Dep_PyH<50:
                Current = "Dos0"
            elif 50<Dep_PyH<75:
                Current = "Dos2"
            elif 75<Dep_PyH<100:
                Current = "Dos0"
            else:
                Current = "Dos0"
                if Dep_PyH >= 100:
                    Dep_PyH -= 100
            Dep_PyH += float(0.7)

        
        elif Modules.Deplacement == "bas":
            if 0<Dep_PyB<25:
                Current = "Face1"
            elif 25<Dep_PyB<50:
                Current = "Face0"
            elif 50<Dep_PyB<75:
                Current = "Face2"
            elif 75<Dep_PyB<100:
                Current = "Face0" 
            else:
                Current = "Face0"
                if Dep_PyB >= 100:
                    Dep_PyB -= 100
            Dep_PyB += float(0.7)
            
        elif Modules.Deplacement == "gauche":

            if 0<Dep_PxG<25:
                Current = "Gauche1"
            elif 25<Dep_PxG<50:
                Current = "Gauche0"
            elif 50<Dep_PxG<75:
                Current = "Gauche2" 
            elif 75<Dep_PxG<100:
                Current = "Gauche0" 
            else:
                Current = "Gauche0"
                if Dep_PxG >= 100:
                    Dep_PxG -= 100
            Dep_PxG += float(0.7)
            
        elif Modules.Deplacement == "droite":
            
            if 0<Dep_PxD<25:
                Current = "Droite1"
            elif 25<Dep_PxD<50:
                Current = "Droite0"
            elif 50<Dep_PxD<75:
                Current = "Droite2"
            elif 75<Dep_PxD<100:
                Current = "Droite0"
            else:
                Current = "Droite0"
                if Dep_PxD >= 100:
                    Dep_PxD -= 100
            Dep_PxD += float(0.7)
            #print(Dep_PxD)

        else:
            Dep_PxD = 0
            Dep_PyB = 0
            Dep_PxG = 0
            Dep_PyH = 0
            
            if Pos_P == 1:
                Current = "Dos0"

            elif Pos_P == 2:
                Current = "Face0"
                
            elif Pos_P == 3:
                Current = "Gauche0"

            elif Pos_P == 4:
                Current = "Droite0"
                
        if not LocPerso3 in Background.ObstaclePNJ and not LocPerso4 in Background.ObstaclePNJ:
            Fenetre_Jeu.blit(Gesture[Current], (Largeur_Jeu/2 -16, Hauteur_Jeu/2 -16))
            
        
        #---#

        #PNJs#
        
        if LocPerso in Mapping.ObstacleDecor or LocPerso2 in Mapping.ObstacleDecor:
            
            for Sprite in Mapping.DecorListe:
                Pos_Decor = Sprite[0]
                     
                    #print(LocPerso, Sprite[0])
                Mapping.AjouterDecor(Background.DicoDecors[Sprite[1]], (Pos_Decor[0]+Modules.Axe_x/Background.TailleGrid, Pos_Decor[1]+Modules.Axe_y/Background.TailleGrid), Fenetre_Jeu)
        
        for npc in NPC.AllNPCs:
            if npc.Surface == Maps.CurrentMapName:
                npc.Render(Fenetre_Jeu)
        

        if LocPerso3 in Background.ObstaclePNJ or LocPerso4 in Background.ObstaclePNJ:
            Fenetre_Jeu.blit(Gesture[Current], (Largeur_Jeu/2 -16, Hauteur_Jeu/2 -16))
        
        #---#
        
        if REDMARK == "Open":
            for t in Mapping.ObstacleDecor:
                pygame.draw.rect(Fenetre_Jeu, (0,0,150), (t[0]*Background.TailleGrid + Modules.Axe_x, t[1]*Background.TailleGrid + Modules.Axe_y, Background.TailleGrid, Background.TailleGrid), 3)
            for t in AllPortails.values():
                POS = t[2]
                #print(POS)
                pygame.draw.rect(Fenetre_Jeu, (150,0,150), (POS[0]*Background.TailleGrid + Modules.Axe_x, POS[1]*Background.TailleGrid + Modules.Axe_y, Background.TailleGrid, Background.TailleGrid), 4)
            for t in Background.Obstacle:
                pygame.draw.rect(Fenetre_Jeu, (150,0,0), (t[0]*Background.TailleGrid + Modules.Axe_x, t[1]*Background.TailleGrid + Modules.Axe_y, Background.TailleGrid, Background.TailleGrid), 5)
            for t in Background.ObstaclePNJ:
                pygame.draw.rect(Fenetre_Jeu, (150,150,0), (t[0]*Background.TailleGrid + Modules.Axe_x, t[1]*Background.TailleGrid + Modules.Axe_y, Background.TailleGrid, Background.TailleGrid), 5)
                
            #------------# VERSION INTERMEDIAIRE
        #for X in range(0, 640, TailleGrid):
            #for Y in range(0, 480, TailleGrid):
                #for Decor in MapData:
                    #TileSprite = (Decor[0] * Background.TailleGrid, Decor[1] * Background.TailleGrid)
                    #if (X, Y) == TileSprite:
                        #Fenetre_Jeu.blit(Background.DicoTextures[Decor[2]], (X + Modules.Axe_x, Y + Modules.Axe_y))
            #------------# VERSION SIMPLE
                #Fenetre_Jeu.blit(Background.SolVille, (X + Modules.Axe_x, Y + Modules.Axe_y))
        #DIALOGUE BOX & TEXTE#
        if Modules.DialogueOn:
            Fenetre_Jeu.blit(DialogueSurface, (20, Hauteur_Jeu - DialogueSurfaceHauteur + 15))

        if Modules.ActiveDialogue != None:
            Lignes = Modules.ActiveDialogue.Texte[Modules.ActiveDialogue.Page]

            for Ligne in Lignes:
                Fenetre_Jeu.blit(pygame.font.Font("Font/DTM-Sans.otf", 26).render(Ligne, True, (0, 0, 0)), (50, (Hauteur_Jeu - DialogueSurfaceHauteur) + 33 + (Lignes.index(Ligne)) * 45))
        NPC.Done = True  
        pygame.display.update()

    # FIN DU JEU
    pygame.quit()
    # Sauvegarde
    ecrire_fichier(Fichier_sauvegarde, Quest)
    ecrire_fichier(Fichier_sauvegarde_module, Modules)
    ecrire_fichier(Fichier_sauvegarde_Map, Maps)
    sys.exit()

if __name__ == "__main__":
    # Ceci n'est exécuté qu'au démarrage du jeu
    jouer_musique("Menu_music", infini=True)
    while True:
        retour = menu()
        if retour == "Continue":
            play()
        elif retour == "Reset":
            # Supprimer les fichiers de sauvegarde
            from Classes import supprimer_tout
            supprimer_tout()
        elif retour == "Quitter":
            pygame.quit()
            sys.exit(0)
