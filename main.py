#importation des modules
import pygame, random, sys, os
from pygame.locals import QUIT



#initialisation de pygame
pygame.init()


#contrôler le FPS maximum
clock = pygame.time.Clock()

longueur, largeur = 600, 500 #configuration des dimensions de la fenêtre
#création de la fenêtre/écran
ecran = pygame.display.set_mode((longueur,largeur))
pygame.display.set_caption('Snake created by Nam, Christopher, Jules and Nareg')

game_over = pygame.image.load("game_over.png") #importation du game over

#implémentation de l'effet sonore lorsque le serpent mange la pomme
bruit_manger = pygame.mixer.Sound("pomme.wav")

#implémentation du game over à la fin du jeu
bruit_fin = pygame.mixer.Sound("game_over.wav")

compteur_bruit_fin = 0 #variable compteur pour game over


game_over =  pygame.transform.scale(game_over, (450, 450)) #dimension image game over

#couleurs => afin de ne pas confondre avec les coordonnées de la balle et du serpent
noir = (0, 0, 0)
rouge = (255, 0, 0)
vert = (0, 255, 0)
bleu = (0,0, 255)
blanc = (255,255,255)
gris = (28, 28, 28)
jaune = (255, 255, 0)

#état de la partie
partie_en_cours = True


#positions x et y de la pomme aléatoires
x_pomme = random.randint(100, 575)
y_pomme = random.randint(100, 475)

#taille d'une case
case = 20

#position du serpent
corps_serpent = []

#tête du serpent au départ
x_serpent = 50
y_serpent = 100

#taille du serpent initiale 
taille_serpent = 1

#booléen pause
pause = False

#vitesse du serpent
vitesse = 4

#score de base
compteur = 0



#fonction mouvement
def mouvement_corps_serpent():
    global corps_serpent, x_serpent, y_serpent, vert, case, pause

  #mouvement corps serpent
    if (pause == False): # condition pas en pause
        if len(corps_serpent) > taille_serpent:
            del(corps_serpent[0]) #supression première élément liste (derrière serpent)

        tete_serpent = []
        tete_serpent.append(x_serpent)
        tete_serpent.append(y_serpent) #ajout de nouvelles coordonées x et y dans la liste du serpent

        corps_serpent.append(tete_serpent)

        corps_serpent_sans_tete = corps_serpent[:-case] #supression dernier élément de la liste (avant du serpent)

        if tete_serpent in corps_serpent_sans_tete: #si la tête se retrouve dans le corps le jeu s'arrête --> les deux listes se croisent
            fin_du_jeu()

    #affichage des autres parties du serpent (surface, couleur, [position x, position y, longueur, largeur]
    for i in corps_serpent:
        pygame.draw.rect(ecran, vert, (i[0], i[1], case, case))




#fonction de la collision entre la pomme et le serpent
def serpent_mange_pomme():
    global compteur, taille_serpent, x_pomme, y_pomme, bruit_manger, corps_serpent, case
    #augmentation du score à chaque fois que le serpent mange la pomme
    compteur+=1

    #augmentation de la taille du serpent
    taille_serpent += case

    #joue à chaque fois l'effet sonore lorsque le serpent mange la pomme
    bruit_manger.play()

    #nouvelles coordonnées aléatoires de la pomme si le serpent touche la pomme
    x_pomme, y_pomme = random.randint(100, 575), random.randint(100, 475)

  # condition de collision entre la pomme et le serpent --> pomme a de nouvelles coordonnées aléatoires
    if [x_pomme, y_pomme] in corps_serpent:
        x_pomme, y_pomme = random.randint(100, 575), random.randint(100, 475)

#fonction fin du jeu
def fin_du_jeu():
    global compteur_bruit_fin, bruit_fin, x_serpent, y_serpent, pause, game_over, etiquette_score
    ecran.fill(gris)
    #bruit qui se déclenche à la fin de la partie
    if compteur_bruit_fin == 0:    
        bruit_fin.play()

    compteur_bruit_fin += 1
    ecran.blit(game_over, [60, 20])
    ecran.blit(etiquette_score, [10, 10]) #déclenchement du game over et l'apparition de l'étiquette
    x_serpent =0
    y_serpent =0 #serpent s'arrête
    message_fin_font = pygame.font.SysFont("Minecraft", 25)
    message_fin = message_fin_font.render("Pressez << 1 >> pour recommencer et << 2 >> pour quitter le jeu", True, jaune)
    ecran.blit(message_fin, [35, 450])
    pause = True #le jeu s'arrête121


#fonction pour relancer le jeu
def relancer():
    python=sys.executable
    os.execl(python, python, * sys.argv)  


#le jeu est en cours
while partie_en_cours:
    #remplit l'écran d'une couleur
    ecran.fill(gris)
    for event in pygame.event.get():
        if event.type == QUIT:
            partie_en_cours = False
     #déplacement du serpent avec KEYUP => (détecte à chaque fois qu'une touche est relâchée)
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP: #mouvement en haut
            y_serpent -= vitesse
            pause = False     
        if event.key == pygame.K_DOWN: #mouvement en bas
            y_serpent += vitesse
            pause = False
        if event.key == pygame.K_RIGHT: #mouvement à droite
            x_serpent += vitesse
            pause = False
        if event.key == pygame.K_LEFT: #mouvement à gauche 
            x_serpent -= vitesse
            pause = False
        if event.key == pygame.K_1:
            relancer() #appel la fonction relancer
        if event.key == pygame.K_2:
            break #arrête le programme


        #pause à chaque fois que la touche SPACE est relachée
        if event.key == pygame.K_SPACE:
            x_serpent +=0
            y_serpent +=0 #serpent s'arrête en position (0;0)
            pause = False
            pause_font = pygame.font.SysFont("Minecraft", 25)
            etiquette_pause = pause_font.render("Pressez une des 4 touches directionnelles pour reprendre", True, jaune)
            ecran.blit(etiquette_pause, [60, 450]) #étiquette activé quand mis en pause
            pause = True

    #police du score 
    score_font = pygame.font.SysFont("Minecraft", 35)
    #crée une nouvelle surface d'une taille appropriée à notre texte
    etiquette_score = score_font.render("Score: " + str(compteur), True, jaune)
    #affichage du score sur l'écran selon les coordonnées x et y
    ecran.blit(etiquette_score, [10, 10])



    #affichage des murs (surface, couleur, position de départ, position finale)
    ligne_gauche = pygame.draw.line(ecran, jaune, (5,80), (5,495),3)
    ligne_haut = pygame.draw.line(ecran, jaune, (5,80), (595,80),3)
    ligne_bas = pygame.draw.line(ecran, jaune, (5,495), (595,495),3)
    ligne_droite = pygame.draw.line(ecran, jaune, (595,80),(595,495),3)


    #affichage de la pomme (surface, couleur, centre du cercle (position x, position y), rayon du cercle)
    pomme = pygame.draw.circle(ecran, rouge, (x_pomme,y_pomme), 12)

    #affichage du serpent(surface, couleur, [position x, position y, longueur, largeur]
    serpent = pygame.draw.rect(ecran, vert, (x_serpent, y_serpent, case, case))

    mouvement_corps_serpent() #appel à la fonction mouvement


    #condition pour vérifier s'il y a une collision entre le serpent et la pomme
    if serpent.colliderect(pomme):
        serpent_mange_pomme() #appel à la fonction de la collision entre la pomme et le serpent

    if x_serpent <= 5 or x_serpent >= 595 or y_serpent <= 80 or y_serpent >= 495: #serpent dépasse les limites du terrains
        fin_du_jeu() #appel fonction fin de partie


    #met à jour les événements
    pygame.display.update()
    #pygame.display.flip()

    #garantie que le jeu s’exécute à la même vitesse sur tous les ordinateurs
    clock.tick(60)





pygame.quit() #fin de pygame
sys.exit()


