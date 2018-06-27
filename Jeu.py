# -*- coding: utf-8 -*-

import pygame, sys, math, random
from pygame.locals import *

from Textures import *
from Classes import *
from Mapping import *
from PNJs import *
from Menu import *
from Save import*

pygame.init()

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
AllPortails = {}

AllPortailsFIXE = {
                #Chambre//Salon
                'StairsChambreToSalon' : ('ChambreTest', 'SalonTest', [9, 6], [0, 3]),
                'StairsSalonToChambre' : ('SalonTest', 'ChambreTest', [8, 3], [0, 0]),
                #Salon//Ville de Depart
                'SalonToDepart' : ('SalonTest', 'Foret13', [5, 12], [-16, -5]),
                'SalonToDepart2' : ('SalonTest', 'Foret13', [6, 12], [-16, -5]),
                'DepartToSalon' : ('Foret13', 'SalonTest', [21, 18], [0, 3]),
                'DepartToSalon2' : ('Foret13', 'SalonTest', [22, 18], [0, 3]),
                #Labo//Ville de Depart
                'DepartToLabo' : ('Foret13', 'Labo7', [38, 19], [15, 0]),
                'DepartToLabo2' : ('Foret13', 'Labo7', [39, 19], [15, 0]),
                'LaboToDepart' : ('Labo7', 'Foret13', [7, 16], [-16, -5]),
                'LaboToDepart2' : ('Labo7', 'Foret13', [8, 16], [-16, -5]),
                #RandomHouse//Ville de Depart
                'RandSalonToDepart' : ('randomsalon', 'Foret13', [5, 11], [-16, -5]),
                'RandSalonToDepart2' : ('randomsalon', 'Foret13', [6, 11], [-16, -5]),
                'DepartToRandSalon' : ('Foret13', 'randomsalon', [27, 24], [6, 10]),
                'DepartToRandSalon2' : ('Foret13', 'randomsalon', [28, 24], [6, 10]),
                #DepartToEglise1#
                'Eglise1ToDepart1' : ('Eglise1', 'Foret13', [15, 18], [-16, -4]),
                'Eglise1ToDepart2' : ('Eglise1', 'Foret13', [16, 18], [-16, -4]),
                'DepartToEglise1' : ('Foret13', 'Eglise1', [21, 33], [-10, 12]),
                'DepartToEglise2' : ('Foret13', 'Eglise1', [22, 33], [-10, 12]),
                #Eglise2ToEglise1#
                'Eglise1ToEglise21' : ('Eglise1', 'Eglise2', [20, 9], [-3, 12]),
                'Eglise1ToEglise22' : ('Eglise1', 'Eglise2', [21, 9], [-3, 12]),
                'Eglise2ToEglise11' : ('Eglise2', 'Eglise1', [10, 9], [-10, 12]),
                'Eglise2ToEglise22' : ('Eglise2', 'Eglise1', [11, 9], [-10, 12]),
                #VilleToEglise1#
                'Eglise2ToVille1' : ('Eglise2', 'Ville5', [15, 18], [-16, -3]),
                'Eglise2ToVille2' : ('Eglise2', 'Ville5', [16, 18], [-16, -3]),
                'VilleToEglise21' : ('Ville5', 'Eglise2', [45, 38], [14, 18]),
                'VilleToEglise22' : ('Ville5', 'Eglise2', [46, 38], [14, 18]),
                   }

AllPortails = AllPortailsFIXE
PORT = 1
#---#

#MapName = Maps.CurrentMapName
Mapping = MappingClass()

#>>>>>>> ef8fa6c2c155937eeef10c2ca809ec239a5a2849
Map = Mapping.Charger_Map("maps/{}.map".format(Maps.CurrentMapName))
#CurrentMap = "{}".format(MapName)
Terrain = Map[0]
Decor = Map[1]

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

#---REDMARK---#
REDMARK = "Close"
#---#

#PNJ(Nom = "", Pos = (32*1, 32*1), Dialogue = Dialogue(Texte = D), Surface = "", Direction = "Face0")

#---PNJs et DIALOGUES-----------------------------------------------------------------------------------------------------------------------------------------------------------#
def CharlesARandom(npc):
    if npc == "CharlesA":
        Dialogs = [[("l'Aube et le crépuscule...","N'oublie pas...")],[("la vie est tel un kinder...","Pleine de surprise")],
                  [("Tous les jours, toutes les semaines ...","Toujours pareils...")], [("Disparais dans un grondement de tonnerre !","")],
                  [("Mon coeur fut une fois resplendissant tel","une toile vierge...")], [("A chaque jour suffit sa peine...","")],
                  [("L'amitié est le voile protecteur","de la cruauté humaine...")], [("Je n'ai jamais vu la lumière que dans","une simple étincelle...")],
                  [("Certains ont été condamnés à la peine de mort.","..."),("Moi, j'ai été condamné à la","peine de vie ...")],
                  [("L'heure et le crépuscule...","Souviens toi...")], [("Sombre est mon passé...","Cruel est mon avenir...")],
                  [("J'ai fermé les yeux depuis bien longtemps...","Ma vie n'existe que dans les ténèbres...")], [("Cette nature ... Si belle et pourant ...","Si triste et injuste ...")],
                  [("Le vent porte la beauté du courrier","dans les fleurs de cerisier.")]]
        X = random.randint(0, 1)
        DialogueRand = Dialogs[X]
        return DialogueRand
    if npc == "VictorD":
        DialogsMot1 = [", un UFO", "une vache", ", Une licorne", ", Adrien qui trouve son chemin", ", Mr. Charles qui parle anglais", ", une troupe d'unijambistes", ", ma mère avec mon père", ", les dev avaient la flemme", ", J'ai plus d'idées", ", je suis devant vous", ", un ticket de loterie perdant"]
        DialogsMot2 = ["votre dignité", "votre virilité", "votre tête", "votre crédibilité", "espoir", "vos clés... banal ?", "votre temps", "des neuronnes", "vos vêtements... Ou pas", "une partie d'échec", "l'envie de jouer à ce jeu de Merd..."]
        X = random.randint(0, len(DialogsMot1)-1)
        Y = random.randint(0, len(DialogsMot2)-1)
        return (DialogsMot1[X], DialogsMot2[Y])

#CharlesV#
DCharlesV = [("Page 1 Ligne 1", "Page 1 Ligne 2"), ("Page 2 Ligne 1", "")]
DCharlesV1 = [("Je sais pourquoi tu es venu.","C'est dommage pour ton frère, vraiment."),("...",""),("Je suis Charles Verichon, leader de la Team Verichon.",""),
              ("Organisation miliaitre, Yostex, tuer ...","Tu connais déjà nos hobbys."),("Je veux juste l'objet, je peux me passer de ta vie","Le gouvernement deviendrait tout puissant avec ma réussite !"),
              ("...",""),("J'y pense, mais tu ne connais le Yostex que de nom...",""),("C'est une fiole, rien d'autre...","Ah, ça ne paraît pas hein ?"),("Ton frère est mort ..."," .pour un ustensile de cuisine."),
              ("Moi qui croyais que la mort n'a","pas le sens de l'humour."),("Bon, une fiole qui exauce tous les souhaits.","Je te l'accorde"),("Peu importe, ton frère a interféré.","Donc, il est mort."),
              ("Tu imagines bien que l'accès au Yostex est ...","Disons, difficile."),("Une carte et une clé, mais que j'ai faillis","perde à cause de deux bambins."),("Comment ça, tu les veux ?","Viens les chercher alors, j'attends ...")]
CharlesV = PNJ(Nom = "CharlesV", Pos = (32*14, 32*4), Dialogue = Dialogue(Texte = DCharlesV1), Surface = "QG", Direction = "Dos0")
#Jean#
DJean1 = [("Le secret ?", "Je l’ai oublié…")]
DJean2 = [("Le secret ?", "Ah oui !"), ("Yos…", "Je l’ai oublié…")]

Jean = PNJ(Nom = "Jean", Pos = (32*1, 32*1), Dialogue = Dialogue(Texte = DJean1), Surface = "Guilde", Direction = "Face0")
#Ryan#
DRyan1 = [("Mal quelque part ? ", "Si ce n’est pas le cas, je suis  occupé")]

Ryan = PNJ(Nom = "Ryan", Pos = (32*1, 32*1), Dialogue = Dialogue(Texte = DRyan1), Surface = "Guilde", Direction = "Face0")
#Hyppolite#
DHippolyte1 = [("La description correspond", "C'est forcément  lui")]
DHippolyte2 = [("Ecoute le  chef", "Veux-tu ?")]

Hippolyte = PNJ(Nom = "Hippolyte", Pos = (32*1, 32*1), Dialogue = Dialogue(Texte = DHippolyte1), Surface = "Mine", Direction = "Face0")
#Arno#
DArno1 = [("Il a raison...", "Attrapez-le!")]
DArno2 = [("Au rapport chef", "Nous l'avons trouvé et saisi !")]
DArno3 = [("Ecoute le  chef", "Veux-tu ?")]
DArno4 = [("Arno : Monsieur le Maire, vous allez devoir répondre à quelques questions.","Rassurez-vous, on ne veut que parler.")]
DArno5 = [("Arno : Nous sommes justement là pour parler de responsabilités.",  "Notamment la responsabilité civile que vous oubliez en coorpérant avec la Team Chaussecourte."),
          ("Vous allez répondre à nos questions.","Et vous le savez.")]
DArno6 = [("Arno : Comment êtes-vous impliqués avec la Team Chaussecourte ?","")]
DArno7 = [("Arno : Rien de plus ?"," Et T.V alors ?"),  ("Jacques à découvert des immenses transactions entre la Team Chaussecourte et T.V.",  "Qui est T.V ?!")]
DArno8 = [("Où sont-ils ?","VITE !")]

Arno = PNJ(Nom = "Arno", Pos = (32*10, 32*4), Dialogue = Dialogue(Texte = DArno3), Surface = "GrottePetite5", Direction = "Face0")
#Barthelemy#
DBarthelemy1 = [("En effet vous l'avez trouvé", "bien...bien..."), (" Vous avez bien travaillé, vous pouvez disposer maintenant ", "Je veux un interrogatoire, et seul. Je vous tiendrai informés"),
               ("j'ai une requête",  "je cherche un objet très précieux..."), ("Accepterais tu...","de te joindre à ma quête?!"),("Je te donnerai des explications",  "c'est promis!")]
DBarthelemy2 = [("Rejoins-moi plus loin dans la grotte", "Veux-tu?")]

Barthelemy = PNJ(Nom = "Barthelemy", Pos = (32*6, 32*5), Dialogue = Dialogue(Texte = DBarthelemy1), Surface = "GrottePetite5", Direction = "Dos0")
#Paul#
DPaul1 = [("Ta Ta", "Yo Yo")]
DPaul2 = [("Ecoute le  chef", "Veux-tu ?")]

Paul = PNJ(Nom = "Paul", Pos = (32*12, 32*15), Dialogue = Dialogue(Texte = DPaul1), Surface = "Guilde", Direction = "Gauche0")
#Sacha#
DSacha1 = [("Cette homme avec une cape", "Tu ne le trouves pas trop bizarre ?")]

Emma = PNJ(Nom = "Sacha", Pos = (32*32+20, 32*17+16), Dialogue = Dialogue(Texte = DSacha1), Surface = "Hotel4", Direction = "Gauche0")
#Emma#
DEmma1 = [("MMMmmmmh…Cette salade", "Un vraie délice")]

Emma = PNJ(Nom = "Emma", Pos = (32*29+20, 32*17+16), Dialogue = Dialogue(Texte = DEmma1), Surface = "Hotel4", Direction = "Droite0")
#Thomas#
DThomas1 = [("Allez les  filles !", "C’est ma tournée !")]

Thomas = PNJ(Nom = "Thomas", Pos = (32*35+20, 32*13-16), Dialogue = Dialogue(Texte = DThomas1), Surface = "Hotel4", Direction = "Droite0")
#Marie#
DMarie1 = [("Je me  demande...", "Tu fais attention à la couleur de tes chaussettes ?")]
DMarie2  = [("Tiens !", "Autobus !")]
DMarie3  = [("j’ai reçu un porte banane pour mon anniv", "C’est génial !")]
DMarie4  = [("Le patron ?", "Il est très occupé…"),("Bon je vais voir ce que  je peux  faire", "…Le voilà qui arrive !")]

Marie = PNJ(Nom = "Marie", Pos = (32*3, 32*12), Dialogue = Dialogue(Texte = DMarie1), Surface = "Hotel4", Direction = "Face0")
#Joséphine#
DJosephine = [("Si vous saviez comment Marie danse bien...", "C'est elle qui m'a tout appris !"), ("Et regardez comment je danse bien aujourd'hui ~", "*Se concentre sur sa chorégraphie*")]
DJosephine2 = [("Ah mince ! j'ai encore oublié de donner", "mon cadeau pour Marie !...")]

Josephine = PNJ(Nom = "Joséphine", Pos = (32*21, 32*12), Dialogue = Dialogue(Texte = DJosephine), Surface = "Hotel4", Direction = "Face0")
#Julie#
DJulie1 = []
DJulie2 = [("Que puis-je faire pour vous ?", "Un hamburger  peut être ?")]

Julie = PNJ(Nom = "Julie", Pos = (32*28, 32*11), Dialogue = Dialogue(Texte = DJulie2), Surface = "Hotel4", Direction = "Face0")
#Amélie#
DAmelie1 = [("Et une pizza pour Ambre", "")]
DAmelie2 = [("Et une raclette pour Adrien", "")]
DAmelie3 = [("Et un bœuf bourguignon  fraichement aromatisé", "Aux fines herbes sur son lit de  patate")]
DAmelie4 = [("Et... j'ai plus de commandes...", "")]

Amelie = PNJ(Nom = "Amelie", Pos = (3231, 324), Dialogue = Dialogue(Texte = DAmelie1), Surface = "Hotel4", Direction = "Dos0")
#Nicolas#
DNicolas1 = [("Bienvenue dans notre humble établissement", "Que puis-je faire pour vous ?")]

Nicolas = PNJ(Nom = "Nicolas", Pos = (32*19, 32*19), Dialogue = Dialogue(Texte = DNicolas1), Surface = "Hotel4", Direction = "Droite0")
#Victoria#
DVictoria1 = [("Ne nous sous-estimez pas !  ","Nous sommes des femmes fortes et dignes !")]

Victoria = PNJ(Nom = "Victoria", Pos = (3222.5, 327), Dialogue = Dialogue(Texte = DVictoria1), Surface = "QG", Direction = "Gauche0")
#Clara#
DClara1 = [("Vous commencez a troublé nos activités…", "Si j’ai un conseil pour toi, c’est de te calmer !")]

Clara = PNJ(Nom = "Clara", Pos = (32*24, 32*7), Dialogue = Dialogue(Texte = DClara1), Surface = "Mine", Direction = "Droite0")
#Alexis#
DAlexis1 = [("Semper Parati, ludus sauvegardus est.", "Vade retro satanas... Ameeeen!")]

Alexis = PNJ(Nom = "Alexis", Pos = (32*15, 32*7), Dialogue = Dialogue(Texte = DAlexis1), Surface = "Eglise1", Direction = "Face0")
Alexis2 = PNJ(Nom = "Alexis", Pos = (32*15, 32*7), Dialogue = Dialogue(Texte = DAlexis1), Surface = "Eglise2", Direction = "Face0")
#Adrien#
DAdrien1 = [("Je suis perdu...", "Vous pourriez pas m'aider par hasard ?"), ("Je cherche le chemin de la maison de Charles A.", "On est censé se faire un raclette aujourd'hui, je vais être en retard...")]
DAdrien2 = [("Dites, vous auriez pas l'heure par hasard ?...", "Et le jour en passant, ça m'aiderait bien..."), ("Bon, et puis l'année aussi, c'est que j'ai","pas trop la notion du temps moi...", "")]
DAdrien3 = [("Vous ne savez pas où  est passé Victor D. par hasard ?","Je suis sûr qu’il m’a encore donné la mauvaise direction...")]

Adrien1 = PNJ(Nom = "Adrien", Pos = (32*27, 32*29), Dialogue = Dialogue(Texte = DAdrien2), Surface = "Foret13", Direction = "Face0")
Adrien2 = PNJ(Nom = "Adrien", Pos = (32*25, 32*29), Dialogue = Dialogue(Texte = DAdrien1), Surface = "Guilde", Direction = "Face0")
Adrien3 = PNJ(Nom = "Adrien", Pos = (32*25, 32*29), Dialogue = Dialogue(Texte = DAdrien3), Surface = "QGVerichon", Direction = "Face0")
#Soana#
DSoana1 = [("Ou est passé Tanguy ?","…"), ("Il faut que je lui explique une bonne fois pour toute", "à quoi sert un réveil…")]

Soana = PNJ(Nom = "Soana", Pos = (32*6.5, 32*14.5), Dialogue = Dialogue(Texte = DSoana1), Surface = "Mairie", Direction = "Face0")
#Tanguy#
DTanguy1 = [("Tanguy : Parler ?!","Je suppose que vous vous êtes armés pour parler aussi."), ("Vous venez de violer l'accès à un lieu privé.",  "Assumez en la responsabilité !")]
DTanguy2 = [("Tanguy : ...","Je vous écoute ...")]
DTanguy3 = [("Tanguy : ...","Juste ça ? Je m'attendais à pire."),  ("Je ne fais que couvrir leurs transaction financières.", "Rien de plus, rien de moins.")]
DTanguy4 = [(" 'Qui sont' serait plus exact.",  "Vous savez, la Team Verichon..."),("Je suis étonné que vous n'ayez pas trouvé plus tôt."),("C'est une légion miliaire pardi !","Ils travaillent en secret pour le gouvernement !"),("Tout ce qui se passe dans la région, ils le savent !","Je nous donne au maximum 10 minutes à vivre..."),
            ("Ils doivent déjà savoir pour votre intrusion à la Mairie.", "..."),("Ils ne vous laisseront aucune chance si le Yostex est en jeu.", "Ils viennent, tuent, et partent !")]
Tanguy = PNJ(Nom = "Tanguy", Pos = (32*6.5, 32*8), Dialogue = Dialogue(Texte = DTanguy1), Surface = "Mairie", Direction = "Face0")
#VictorD#
DVictorD1 = [("Promis juré craché sur la terre bénie,", "lavé puis ravalé et recraché,"), ("je compte pas vous voler !", "foi de roumain !")]

VictorD = PNJ(Nom = "VictorD", Pos = (32*12, 32*11), Dialogue = Dialogue(Texte = DVictorD1), Surface = "Eglise1", Direction = "Dos0")
#Ewan#


#LeoG#
DLeoG1 = [("Empêchez les de passer !", "L’artefact passe avant tout !")]
DLeoG2 = [("Halte la !","Rendez-vous ou mourrez !")]


#CharlesA#


#Ines#
DInes1 = [("Bonjour Mon Chaton, bien dormi ?", "Le professeur Richard voulait te voir !"), ("Pourrais-tu le rejoindre dans son Labo ?", "C'est juste à côté, et je crois qu'il voulait te montrer des choses ~")]
DInes2 = [("Salut Mon Amour ~", "As-tu  vu le professeur ?"),  ("*Votre mère retourne dans ses pensées*", "")]

Ines = PNJ(Nom = "Ines", Pos = (32*7, 32*9), Dialogue = Dialogue(Texte = DInes1), Surface = "SalonTest", Direction = "Face0")
#Ambre#
DAmbre = [("Bonjour ! Je vois que tu te portes plutot bien ~", "J'adore la nature..."), ("Je pourrais passer des heures à contempler le paysage...", "Pas toi ?")]
DAmbre2 = [("C'est pour moi ça ?", "Tu remercieras ta mère de ma part ! Ca à l'air super bon ! ~"), ("Reviens me voir plus tard si ça te tente !", "")]
DAmbre3 = [("*Ambre est toujours en train de déguster votre Bento...*", "MMMmmmh... Exchellent !")]

Ambre = PNJ(Nom = "Ambre", Pos = (32*25, 32*29), Dialogue = Dialogue(Texte = DAmbre), Surface = "Ambre14", Direction = "Face0")
#Julien#
DJulien1 = [("Ah, Jacques, le grand, le fameux !",""),("Si je te connais ?", "Non bien sûr, ou alors peu."),("J'aime impressionner avec des grands airs.","C'est toujours mieux que la paperasse officielle."),
           ("Je suis bien content que tu sois venu de ton plein gré.","Autrement tu serais venu de force, emballé dans un sac."),("Tu as neutralisé deux de mes Hommes en pleine affaire ...","et je n'aime pas ça."),
           ("D'ailleurs j'ai oublié de me présenter.","Julien Chaussecourte, leader de la Team Chaussecourte."),("On est le gros poisson financier de la région.","Toutes les transaction, légales ou non, passent par nous."),
           ("On est un cartel de drogue si tu veux. Mais, je préfère", "le voir comme une opportunité financière."),("On est tellement riches !","On peut s'offrir la protection du Maire De Lanversin."),("C'est pas beau, ça ?",""),
           ("Le seul obstacle au bon fonctionnement de mon business","..."),("C'est toi.","C'est assez paradoxal que tu cherches autant d'ennuis."),("Si ton frère meurt sous tes yeux, il est peut-être","temps d'arrêter de marcher dans ses pas ...")]
DJulien2 = [("Allez, dégage morveux.", "On te reglera ton compte plus tard...")]

Julien = PNJ(Nom = "Julien", Pos = (32*37, 32*5), Dialogue = Dialogue(Texte = DJulien1), Surface = "Hotel4", Direction = "Face0")
#Fabien#
DFabien1 = [("Oh, Bonjour Jacques !", "Tu es venu ici pour choisir ton Premier Pokem..."), ("Ah mince, c'est le mauvais script...","Du coup ! Oui, je voulais te voir."), ("Tu te rappelles du moment où ton frère est parti ...", "il y a déjà 3 ans ?") ,("Eh bien, il n’est pas  parti sans rien", "laisser derrière  lui"),
                      ("Il a laissé un journal que j’ai soigneusement récupéré", "... j’attendais le bon moment pour te le donner."),("Il y mentionne notamment une grotte,", "Je pense que tu devrais commencer tes recherches par là.")]
DFabien2 = [("Alors Jacques… Cette Grotte ?", "")]

Fabien = PNJ(Nom = "Fabien", Pos = (32*5, 32*8), Dialogue = Dialogue(Texte = DFabien1), Surface = "Labo7", Direction = "Dos0")
#Martin#
DMartin1 = [("Je retrouve pas ma PS4 !...", "Je suis sûr que c'est encore Pr. Richard..."), ("il deteste me voir jouer...", "")]
DMartin2 = [("Bouh", "")]
Martin = PNJ(Nom = "Martin", Pos = (32*8, 32*2), Dialogue = Dialogue(Texte = DMartin1), Surface = "Labo7", Direction = "Dos0")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
Pos_P = 0
Dep_PyH, Dep_PyB, Dep_PxD, Dep_PxG = 0, 0, 0, 0

#Pos_Px = (Largeur_Jeu/2 - Modules.Axe_x ) / Background.TailleGrid
#Pos_Py = (Hauteur_Jeu/2 - Modules.Axe_y +25) / Background.TailleGrid
   
Continuer = True

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

    for Portail in AllPortails.values():
        if LocPerso3 == Portail[2] and Maps.CurrentMapName == Portail[0]:
            Maps.CurrentMapName = str(Portail[1])
            #CurrentMap = Portail[1]
            #print(Portail[1])
            #print(str(Portail[1]))
            #CurrentMap = Portail[1]
            Background.Obstacle = []
            Mapping.ObstacleDecor = []
            Background.ObstaclePNJ = []
            Mapping.DecorListe = []
            Modules.Diff = Portail[3]
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


pygame.quit()
# Sauvegarde
ecrire_fichier(Fichier_sauvegarde, Quest)
ecrire_fichier(Fichier_sauvegarde_module, Modules)
ecrire_fichier(Fichier_sauvegarde_Map, Maps)
sys.exit()
    
