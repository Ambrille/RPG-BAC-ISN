# -*- coding: utf-8 -*-

import pygame
import random
from pygame.locals import *
from Classes import *
from Textures import *

pygame.init()

global Current, Gesture

class GestuelClass(object):

    global Current, Gesture

    Personnages = ["LeoG", "CharlesA", "Fabien", "Nicolas", "CharlesV", "Marin",
                   "Ambre", "Amelie", "Marie", "Ewan", "Julie", "Alexis", "Adrien",
                   "Arno", "Barthelemy", "Emma", "Ewan", "Hippolyte", "Jean",
                   "Julien", "Martin", "Paul", "Sacha", "Soana", "Tanguy", "Thomas",
                   "Timothée", "VictorD", "Victoria", "Josephine", "LeoF", "VictorA", "Clara"
                  ]
                  
    def ChargerGesture(self, Nom):
        global Current, Gesture
        Taille = [64, 64]
        Largeur = Taille[0]
        Hauteur = Taille[1]
        Perso = pygame.image.load("Textures/Perso/{}/Ov{}.png".format(Nom, Nom))
        Perso = pygame.transform.scale(Perso, (Largeur*3, Hauteur*4))

        #Gesture = self.ChargerGesture(Perso)
        

        Gesture = {}
        Taille = [64, 64]
        TailleX = Taille[0]
        TailleY = Taille[1]

        #FACE#
        Face0 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Face0.blit(Perso, (0,0), (TailleX*2, TailleY, TailleX*3, TailleY*2))
        Gesture["Face0"] = Face0

        Face1 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Face1.blit(Perso, (0,0), (TailleX*2, TailleY*2, TailleX*3, TailleY*3))
        Gesture["Face1"] = Face1

        Face2 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Face2.blit(Perso, (0,0), (TailleX*2, TailleY*3, TailleX*3, TailleY*4))
        Gesture["Face2"] = Face2

        #GAUCHE#
        Gauche0 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Gauche0.blit(Perso, (0,0), (0, TailleY*2, TailleX, TailleY*3))
        Gesture["Gauche0"] = Gauche0

        Gauche1 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Gauche1.blit(Perso, (0,0), (0, TailleY, TailleX, TailleY*2))
        Gesture["Gauche1"] = Gauche1

        Gauche2 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Gauche2.blit(Perso, (0,0), (0, TailleY*3, TailleX, TailleY*4))
        Gesture["Gauche2"] = Gauche2

        #DROITE#
        Droite0 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Droite0.blit(Perso, (0,0), (TailleX, 0, TailleX*2, TailleY))
        Gesture["Droite0"] = Droite0

        Droite1 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Droite1.blit(Perso, (0,0), (TailleX, TailleY, TailleX*2, TailleY*2))
        Gesture["Droite1"] = Droite1

        Droite2 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Droite2.blit(Perso, (0,0), (TailleX, TailleY*2, TailleX*2, TailleY*3))
        Gesture["Droite2"] = Droite2

        #DOS#
        Dos0 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Dos0.blit(Perso, (0,0), (0, 0, TailleX, TailleY))
        Gesture["Dos0"] = Dos0

        Dos1 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Dos1.blit(Perso, (0,0), (TailleX, TailleY*3, TailleX*2, TailleY*4))
        Gesture["Dos1"] = Dos1

        Dos2 = pygame.Surface(Taille, pygame.HWSURFACE|pygame.SRCALPHA)
        Dos2.blit(Perso, (0,0), (TailleX*2, 0, TailleX*3, TailleY))
        Gesture["Dos2"] = Dos2
        
        
        return Gesture
    
    #Gesture = ChargerGesture()
    
    #print(Gesture)

Gestuel = GestuelClass()

def MoveNPC(npc):
    npc.facing = random.choice(("Face0", "Dos0", "Gauche0", "Droite0"))
    npc.walking = random.choice((True, False))


class Dialogue(object):

    def __init__(self, Texte):
        self.Page = 0
        self.Texte = Texte #[('Page 1 Ligne 1', 'Page 1 Ligne 2'), ('Page 2 Ligne 1')]
        
class NPC(object):

    AllNPCs = []
    Decor = []
    LastLocation = 0
    Done = False
    
    def __init__(self, Nom, Pos, Dialogue, Surface, Direction):
        self.Name = Nom
        self.X = Pos[0]
        self.Y = Pos[1]
        self.Dialogue = Dialogue
        self.Surface = Surface
        self.Largeur = 64
        self.Hauteur = 64
        self.walking = False
        self.Timer = Timer(1)
        self.Timer.OnNext = lambda: MoveNPC(self)
        self.Current = Direction
        self.CurrentInit = Direction
        self.Gesture = Gestuel.ChargerGesture(Nom)

        NPC.AllNPCs.append(self)
        print(NPC.AllNPCs)
        
    def Render(self, surface):
        if not self.walking:
            #Mouv = 100 * Modules.deltatime
            #Location = [(self.X / Background.TailleGrid), ((self.Y+64) / Background.TailleGrid)]
            #Location1 = [((self.X+32) / Background.TailleGrid), ((self.Y+64) / Background.TailleGrid)]
            Location2 = [(self.X / Background.TailleGrid), ((self.Y+32) / Background.TailleGrid)]
            Location3 = [((self.X+32) / Background.TailleGrid), ((self.Y+32) / Background.TailleGrid)]
            
            #if self.LastLocation in Background.Obstacle and self.walking == True:
                #Background.Obstacle.remove(self.LastLocation)
                #Background.Obstacle.remove(self.LastLocation1)
                #Background.Obstacle.remove(self.LastLocation2)
                #Background.Obstacle.remove(self.LastLocation3)
            #if not Location in Background.Obstacle:
            #    Background.Obstacle.append(Location)
            #    self.LastLocation = Location
            #if not Location1 in Background.Obstacle:
            #    Background.Obstacle.append(Location1)
            #    self.LastLocation1 = Location1
            if not Location2 in Background.ObstaclePNJ:
               Background.ObstaclePNJ.append(Location2)
               self.LastLocation2 = Location2
            if not Location3 in Background.ObstaclePNJ:
               Background.ObstaclePNJ.append(Location3)
               self.LastLocation3 = Location3
        
                
        surface.blit(self.Gesture[self.Current], (self.X + Modules.Axe_x, self.Y + Modules.Axe_y))

class PNJ(NPC):

    def __init__(self, Nom, Pos, Dialogue = None, Surface = None, Direction = None):
        super(PNJ, self).__init__(Nom, Pos, Dialogue, Surface, Direction)
        
class Timer:
    
    def __init__(self, interval = 1):
        self.Interval = interval
        self.Value = 0
        self.LastInt = 0
        self.Active = False
        self.OnNext = None

## DONNES DES PNJs

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
DCharlesV2 = [("Non  pitiez!", "Arêtez de me taper"), ("Je vous promet de plus etre une grosse guez", "")]
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
DHippolyte3 = [("Bartouille était un grand homme!", "")]

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
DArno9 = [("Nous regrettons tous pour Bartouille!","Mais nous devons continuer sa quête!")]

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
DSacha2 = [("Pourquoi il me fixe comme ca?", "")]

Emma = PNJ(Nom = "Sacha", Pos = (32*32+20, 32*17+16), Dialogue = Dialogue(Texte = DSacha1), Surface = "Hotel4", Direction = "Gauche0")
#Emma#
DEmma1 = [("MMMmmmmh…Cette salade", "Un vraie délice")]

Emma = PNJ(Nom = "Emma", Pos = (32*29+20, 32*17+16), Dialogue = Dialogue(Texte = DEmma1), Surface = "Hotel4", Direction = "Droite0")
#Thomas#
DThomas1 = [("Allez les  filles !", "C’est ma tournée !")]
DThomas2 = [("Oups!", "j'ai plus d'argent !")]

Thomas = PNJ(Nom = "Thomas", Pos = (32*35+20, 32*13-16), Dialogue = Dialogue(Texte = DThomas1), Surface = "Hotel4", Direction = "Droite0")
#Marie#
DMarie1 = [("Je me  demande...", "Tu fais attention à la couleur de tes chaussettes ?")]
DMarie2  = [("Tiens !", "Autobus !")]
DMarie3  = [("j’ai reçu un porte banane pour mon anniv", "C’est génial !")]
DMarie4  = [("Le patron ?", "Il est très occupé…"),("Bon je vais voir ce que  je peux  faire", "…Le voilà qui arrive !")]
DMarie5  = [("tout s'est bien  passé avec  le patron?","Tu veux un bisous  magique?"), ("eh ben non","mais si tu veux je t'offres des chaussettes")]

Marie = PNJ(Nom = "Marie", Pos = (32*3, 32*12), Dialogue = Dialogue(Texte = DMarie1), Surface = "Hotel4", Direction = "Face0")
#Joséphine#
DJosephine = [("Si vous saviez comment Marie danse bien...", "C'est elle qui m'a tout appris !"), ("Et regardez comment je danse bien aujourd'hui ~", "*Se concentre sur sa chorégraphie*")]
DJosephine2 = [("Ah mince ! j'ai encore oublié de donner", "mon cadeau pour Marie !...")]

Josephine = PNJ(Nom = "Joséphine", Pos = (32*21, 32*12), Dialogue = Dialogue(Texte = DJosephine), Surface = "Hotel4", Direction = "Face0")
#Julie#
DJulie1 = [("Notre maire est un homme splendide", "tu ne trouves pas?")]
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
DVictoria1 = [("Non Charles!","Pourquoi  tant de   haine?")]

Victoria = PNJ(Nom = "Victoria", Pos = (3222.5, 327), Dialogue = Dialogue(Texte = DVictoria1), Surface = "QG", Direction = "Gauche0")
#Clara#
DClara1 = [("Vous commencez a troublé nos activités…", "Si j’ai un conseil pour toi, c’est de te calmer !")]
DClara2 = [("Peut etre que  je  pourrai remplacer le boss", "oups qu'est ce que tu as à m'écouter")]

Clara = PNJ(Nom = "Clara", Pos = (32*24, 32*7), Dialogue = Dialogue(Texte = DClara1), Surface = "Mine", Direction = "Droite0")
#Alexis#
DAlexis1 = [("Semper Parati, ludus sauvegardus est.", "Vade retro satanas... Ameeeen!")]

Alexis = PNJ(Nom = "Alexis", Pos = (32*15, 32*7), Dialogue = Dialogue(Texte = DAlexis1), Surface = "Eglise1", Direction = "Face0")
Alexis2 = PNJ(Nom = "Alexis", Pos = (32*15, 32*7), Dialogue = Dialogue(Texte = DAlexis1), Surface = "Eglise2", Direction = "Face0")
#Adrien#
DAdrien1 = [("Je suis perdu...", "Vous pourriez pas m'aider par hasard ?"), ("Je cherche le chemin de la maison de Charles A.", "On est censé se faire un raclette aujourd'hui, je vais être en retard...")]
DAdrien2 = [("Dites, vous auriez pas l'heure par hasard ?...", "Et le jour en passant, ça m'aiderait bien..."), ("Bon, et puis l'année aussi, c'est que j'ai","pas trop la notion du temps moi...", "")]
DAdrien3 = [("Vous ne savez pas où  est passé Victor D. par hasard ?","Je suis sûr qu’il m’a encore donné la mauvaise direction...")]

Adrien1 = PNJ(Nom = "Adrien", Pos = (32*27, 32*29), Dialogue = Dialogue(Texte = DAdrien2), Surface = "Foret", Direction = "Face0")
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
DEwan1 = [("Il est écrit..", "Karmaboy...Légende passée")]
DEwan2 = [("Mais c'est quoi cette histoire?", "Allez je retoourne dans ma  cité!"), ("Got them", "Po-Po stressing!")]

#LeoG#
DLeoG1 = [("Empêchez les de passer !", "L’artefact passe avant tout !")]
DLeoG2 = [("Halte la !","Rendez-vous ou mourrez !")]
DLeoG3 = [("Hum...","")]


#CharlesA#
DCharlesA1 = [("l'Aube et le crépuscule...","n'oublie pas..."), ("la vie est tel un kinder...","pleine de surprise")]


#Ines#
DInes1 = [("Bonjour Mon Chaton, bien dormi ?", "Le professeur Richard voulait te voir !"), ("Pourrais-tu le rejoindre dans son Labo ?", "C'est juste à côté, et je crois qu'il voulait te montrer des choses ~")]
DInes2 = [("Salut Mon Amour ~", "As-tu  vu le professeur ?"),  ("*Votre mère retourne dans ses pensées*", "")]
DInes3 = [("Salut Mon Amour ~", "il y a des cookies dans le four si tu veux"),  ("*Votre mère retourne dans ses pensées*", "")]

Ines = PNJ(Nom = "Ines", Pos = (32*7, 32*9), Dialogue = Dialogue(Texte = DInes1), Surface = "Salon", Direction = "Face0")
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
DFabien3 = [("Alors Jacques… Cette Grotte ?", ""),("Incroyable!", "Mais qu'est il passé par la tete de ron frère?")]

Fabien = PNJ(Nom = "Fabien", Pos = (32*5, 32*8), Dialogue = Dialogue(Texte = DFabien1), Surface = "Labo", Direction = "Dos0")
#Martin#
DMartin1 = [("Je retrouve pas ma PS4 !...", "Je suis sûr que c'est encore Pr. Richard..."), ("il deteste me voir jouer...", "")]
DMartin2 = [("Bouh", "")]
Martin = PNJ(Nom = "Martin", Pos = (32*8, 32*2), Dialogue = Dialogue(Texte = DMartin1), Surface = "Labo", Direction = "Dos0")
#LeoF#
DLeoF1 = [("Ah dur vie  d'etre soldat", "haha!")]
DLeoF2 = [("Mouhahahaha", "J'étais le chef depuis le   début!"), ("Tu pensais nous avoir vaicu  n'est ce pas!", "Jamais tu ne t'en sortiras!"), ("J'en fait appel  au héros de l'ancien temps!", "Soie le bras armée de ma  colère"),
         ("Karmaboyyyy", "EN SCENE!!")]
DLeoF3 = [("Mais non c'est un terrible malentendue", "Charles était le vraie chef"), ("Ne me faite pas  de mal", "J'ai de   l'argent vous  savez!!!")]
