import pygame
import pygame_menu

pygame.init()

# Définition des variables globales
longueur, largeur = 600, 600  # Définit la longueur et la largeur de la fenêtre de jeu
screen = pygame.display.set_mode((longueur, largeur))  # Crée la fenêtre de jeu avec les dimensions définies
pygame.display.set_caption("Tic Tac Toe")  # Définit le titre de la fenêtre de jeu
white = (255, 255, 255)
black = (0, 0, 0)
taille_ligne = 7  # Définit l'épaisseur des lignes de la grille
espacement = 200 # Définit l'espacement entre les lignes de la grille
joueur_actuel = "X"
plateau = [["" for _ in range(3)] for _ in range(3)]  # Crée un plateau de jeu 3x3 vide

# Dessine la grille du jeu
def grille():
    for i in range(1, 3):
        pygame.draw.line(screen, black, (0, i * espacement), (longueur, i * espacement), taille_ligne)  # Dessine 2 lignes horizontales
        pygame.draw.line(screen, black, (i * espacement, 0), (i * espacement, largeur), taille_ligne)   # Dessine 2 lignes verticales

# Place le symbole du joueur ('X' ou 'O') dans la case sélectionnée
def placer_symbole(row, col, joueur): 
    plateau[row][col] = joueur

# Dessine les symboles 'X' et 'O' sur le plateau
def dessiner_symboles():
    for row in range(3):
        for col in range(3):
            if plateau[row][col] == "X":
                pygame.draw.line(screen, black, (col * espacement + 50, row * espacement + 50), (col * espacement + 150, row * espacement + 150), taille_ligne)
                pygame.draw.line(screen, black, (col * espacement + 150, row * espacement + 50), (col * espacement + 50, row * espacement + 150), taille_ligne)
            elif plateau[row][col] == "O":
                pygame.draw.circle(screen, black, (col * espacement + 100, row * espacement + 100), 50, taille_ligne)

# Vérifie si le joueur actuel a gagné
def verifier_victoire(joueur):
    for i in range(3):
        if plateau[i][0] == plateau[i][1] == plateau[i][2] == joueur or plateau[0][i] == plateau[1][i] == plateau[2][i] == joueur: # Vérifie les lignes et colonnes
            return True
    if plateau[0][0] == plateau[1][1] == plateau[2][2] == joueur or plateau[0][2] == plateau[1][1] == plateau[2][0] == joueur: # Vérifie les diagonales
        return True
    return False

# Vérifie si toutes les cases du plateau sont remplies (match nul)
def verifier_match_nul():
    for row in plateau:
        if "" in row:
            return False
    return True

# Vérifie si la case sélectionnée est libre
def verifier_case_libre(row, col):
    return plateau[row][col] == ""

# Change le joueur actuel
def changer_joueur():
    global joueur_actuel
    joueur_actuel = "O" if joueur_actuel == "X" else "X"

# Réinitialiser le jeu
def reinitialiser_jeu():
    global joueur_actuel, plateau
    joueur_actuel = "X"
    plateau = [["" for _ in range(3)] for _ in range(3)]

# Fonction pour démarrer le jeu
def commencer_jeu():
    global jeu_en_cours
    reinitialiser_jeu()
    jeu_en_cours = True
    menu_principal.close()

# Affiche un message sur l'écran
def afficher_message(message, temps_attente=2000):
    font = pygame.font.Font(None, 36)
    texte = font.render(message, True, black)
    texte_rect = texte.get_rect(center=(longueur / 2, largeur / 2))
    screen.fill(white)
    screen.blit(texte, texte_rect)
    pygame.display.update()
    pygame.time.wait(temps_attente)

# Création du menu
menu_principal = pygame_menu.Menu('Tic Tac Toe', longueur, largeur,
                                  theme=pygame_menu.themes.THEME_BLUE)
menu_principal.add.button('Jouer', commencer_jeu)
menu_principal.add.button('Quitter', pygame_menu.events.EXIT)

# Boucle principale du jeu
jeu_en_cours = False

while True:
    if jeu_en_cours:
        screen.fill(white)
        grille()
        dessiner_symboles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // espacement
                row = y // espacement
                if verifier_case_libre(row, col):
                    placer_symbole(row, col, joueur_actuel)
                    grille()
                    dessiner_symboles()
                    pygame.display.update()
                    if verifier_victoire(joueur_actuel):
                        gagnant = "Les ronds ont gagné !" if joueur_actuel == "O" else "Les croix ont gagné !"
                        afficher_message(gagnant)
                        jeu_en_cours = False
                        break
                    elif verifier_match_nul():
                        afficher_message("Match Nul !")
                        jeu_en_cours = False
                        break
                    changer_joueur()

    else:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        menu_principal.update(events)
        menu_principal.draw(screen)

    pygame.display.update()