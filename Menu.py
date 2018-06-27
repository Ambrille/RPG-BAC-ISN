# -*- coding: utf-8 -*-

import sys, os, pygame, math
from pygame.locals import *
import time

Hauteur, Largeur = 600, 800
CoordSouris = 0
Souris_x, Souris_y = 0, 0
fond = pygame.image.load("Textures/Menu/Menu.png")
fond = pygame.transform.scale(fond, (Largeur, Hauteur))
Btn_Continue = pygame.image.load("Textures/Menu/Btn_continue.png")
Btn_Continue2 = pygame.image.load("Textures/Menu/Btn_continue2.png")
Btn_Reset = pygame.image.load("Textures/Menu/Btn_reset.png")
Btn_Reset2 = pygame.image.load("Textures/Menu/Btn_reset2.png")
Btn_Exit = pygame.image.load("Textures/Menu/Btn_exit.png")
Btn_Exit2 = pygame.image.load("Textures/Menu/Btn_exit2.png")
Sound = False

def menu():
    pygame.init()
    Menu = pygame.display.set_mode((Largeur, Hauteur))
    Menu.blit(fond, (0,0))
    Menu.blit(Btn_Continue, (200,200))
    Menu.blit(Btn_Reset, (200,300))
    Menu.blit(Btn_Exit, (200,400))
    volume = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(0.1)
    channel1 = pygame.mixer.Channel(0)
    tic = pygame.mixer.Sound("Musique/Sound/tic.wav")

#400*65
    
    while True:
        for event in pygame.event.get():            
            if event.type==QUIT:
                pygame.quit()
                sys.exit(0)
                return

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                CoordSouris = pygame.mouse.get_pos()
                Souris_x = event.pos[0]
                Souris_y = event.pos[1]

                    
                #if 400<Souris_y<465:
                    #tic.play(0,1000,100)
                    #if 402<Souris_y<465:
                        #pygame.mixer.stop()
                    
                if 200 < Souris_x <600:
                    if 200<Souris_y<265:
                        Menu.blit(Btn_Continue2, (200,200))
                    elif 300<Souris_y<365:
                        Menu.blit(Btn_Reset2, (200,300))
                    elif 400<Souris_y<465:
                        Menu.blit(Btn_Exit2, (200,400))
                    else:
                        Menu.blit(fond, (0,0))
                        Menu.blit(Btn_Continue, (200,200))
                        Menu.blit(Btn_Reset, (200,300))
                        Menu.blit(Btn_Exit, (200,400))
                        
                else:
                    Menu.blit(fond, (0,0))
                    Menu.blit(Btn_Continue, (200,200))
                    Menu.blit(Btn_Reset, (200,300))
                    Menu.blit(Btn_Exit, (200,400))
                    
                    

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                
                if 200<Souris_x <600 and 200<Souris_y<265:
                    #son.play(0,1000,10)
                    tic.play()
                    pygame.mixer.music.stop()
                    return "Continue"
                    
                elif 200<Souris_x <600 and 300<Souris_y<365:
                    #son.play(0,1000,100)
                    tic.play()
                    return "Reset"

                elif 200<Souris_x <600 and 400<Souris_y<465:
                    tic.play()
                    return "Quitter"
