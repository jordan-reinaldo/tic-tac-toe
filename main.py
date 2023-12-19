import pygame  
import pygame_menu  
from ia import ia  # importe la fonction ia depuis le fichier ia.py

# Initialisation de Pygame
pygame.init() 

# Définition des variables globales
longueur, largeur = 600, 600 
screen = pygame.display.set_mode((longueur, largeur))  # crée la fenêtre du jeu
pygame.display.set_caption("Tic Tac Toe")  # titre de la fenêtre
white = (255, 255, 255)  
black = (0, 0, 0)  
taille_ligne = 7  
espacement = 200  # définit l'espacement entre les lignes de la grille
joueur_actuel = "X"  # définit le joueur actuel (commence par 'X')
plateau = [["" for _ in range(3)] for _ in range(3)]  # crée un plateau de jeu 3x3 vide
mode_contre_ia = False  # indique si le jeu est en mode joueur contre IA

# dessine la grille du jeu
def grille():
    # dessine les lignes verticales et horizontales de la grille
    for i in range(1, 3):
        pygame.draw.line(screen, black, (0, i * espacement), (longueur, i * espacement), taille_ligne)
        pygame.draw.line(screen, black, (i * espacement, 0), (i * espacement, largeur), taille_ligne)

def placer_symbole(row, col, joueur):
    plateau[row][col] = joueur  # place le symbole du joueur sur le plateau

# dessine les symboles 'X' et 'O' sur le plateau
def dessiner_symboles():
    # parcourt chaque case du plateau pour dessiner les symboles
    for row in range(3):
        for col in range(3):
            if plateau[row][col] == "X":
                pygame.draw.line(screen, black, (col * espacement + 50, row * espacement + 50), (col * espacement + 150, row * espacement + 150), taille_ligne)
                pygame.draw.line(screen, black, (col * espacement + 150, row * espacement + 50), (col * espacement + 50, row * espacement + 150), taille_ligne)
            elif plateau[row][col] == "O":
                pygame.draw.circle(screen, black, (col * espacement + 100, row * espacement + 100), 50, taille_ligne)

# vérifie si le joueur actuel a gagné
def verifier_victoire(joueur):
    # vérifie chaque ligne, colonne et diagonale pour un gagnant
    for i in range(3):
        if plateau[i][0] == plateau[i][1] == plateau[i][2] == joueur or plateau[0][i] == plateau[1][i] == plateau[2][i] == joueur:
            return True
    if plateau[0][0] == plateau[1][1] == plateau[2][2] == joueur or plateau[0][2] == plateau[1][1] == plateau[2][0] == joueur:
        return True
    return False


def verifier_match_nul():
    for row in plateau: # vérifie si toutes les cases du plateau sont remplies (match nul)
        if "" in row:
            return False
    return True

def verifier_case_libre(row, col):
    return plateau[row][col] == "" 

def changer_joueur():
    global joueur_actuel 
    joueur_actuel = "O" if joueur_actuel == "X" else "X"  # change le joueur actuel de 'X' à 'O' ou inversement

def reinitialiser_jeu():
    global joueur_actuel, plateau  
    joueur_actuel = "X"  # réinitialise le joueur actuel à 'X'
    plateau = [["" for _ in range(3)] for _ in range(3)]  # réinitialise le plateau

def afficher_message(message, temps_attente=2000):
    font = pygame.font.Font(None, 36)  # définit la police et la taille du texte
    texte = font.render(message, True, black)  # crée le texte à afficher
    texte_rect = texte.get_rect(center=(longueur / 2, largeur / 2))  
    screen.fill(white)  
    screen.blit(texte, texte_rect)  
    pygame.display.update()  # met à jour l'affichage
    pygame.time.wait(temps_attente)  

# fonction pour démarrer le jeu contre un autre joueur
def commencer_jeu():
    global jeu_en_cours, mode_contre_ia  
    reinitialiser_jeu()  
    jeu_en_cours = True  # démarre le jeu
    mode_contre_ia = False  # désactive le mode contre l'IA
    menu_principal.close()  # ferme le menu principal

# fonction pour démarrer le jeu contre l'IA
def commencer_jeu_vs_ia():
    global jeu_en_cours, mode_contre_ia  
    reinitialiser_jeu()  
    jeu_en_cours = True  
    mode_contre_ia = True  # active le mode contre l'IA
    menu_principal.close() 

# création du menu
menu_principal = pygame_menu.Menu('Tic Tac Toe', longueur, largeur, theme=pygame_menu.themes.THEME_BLUE)
menu_principal.add.button('Jouer contre un ami', commencer_jeu)
menu_principal.add.button('Jouer contre l\'ordinateur', commencer_jeu_vs_ia)
menu_principal.add.button('Quitter', pygame_menu.events.EXIT)

jeu_en_cours = False 

while True:
    events = pygame.event.get()  
    for event in events:
        if event.type == pygame.QUIT:  
            pygame.quit()  #
            exit()  

    if jeu_en_cours:
        screen.fill(white)  # remplit l'écran de blanc
        grille()  # dessine la grille du jeu
        dessiner_symboles()  # dessine les symboles 'X' et 'O'
        pygame.display.update()  # met à jour l'affichage

        # Tour du joueur
        if not mode_contre_ia or (mode_contre_ia and joueur_actuel == "X"):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:  # si le joueur clique sur la souris
                    x, y = event.pos  # récupère la position du clic
                    col = x // espacement  # calcule la colonne cliquée
                    row = y // espacement  # calcule la ligne cliquée
                    if verifier_case_libre(row, col):  
                        placer_symbole(row, col, joueur_actuel)  
                        if verifier_victoire(joueur_actuel):  
                            gagnant = "Les croix ont gagné !" if joueur_actuel == "X" else "Les ronds ont gagné !"
                            afficher_message(gagnant)  
                            jeu_en_cours = False  # termine le jeu
                        elif verifier_match_nul():  
                            afficher_message("Match Nul !")  
                            jeu_en_cours = False
                        changer_joueur()
                        break  # important pour sortir de la boucle après un coup

        # tour de l'IA
        if mode_contre_ia and joueur_actuel == "O" and jeu_en_cours:
            pygame.time.delay(2000)  # délai pour simuler la réflexion de l'IA
            row, col = ia(plateau, joueur_actuel)
            if row is not None and col is not None:
                placer_symbole(row, col, joueur_actuel)
                if verifier_victoire(joueur_actuel):
                    afficher_message("L'ordinateur a gagné !")
                    jeu_en_cours = False
                elif verifier_match_nul():
                    afficher_message("Match Nul !")
                    jeu_en_cours = False
                changer_joueur()

    else:
        menu_principal.update(events)
        menu_principal.draw(screen)
        pygame.display.update()