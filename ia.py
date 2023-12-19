import random

def ia(plateau, signe):
    # Convertir le plateau en format numérique
    plateau_num = [[0 if case == "" else (1 if case == "X" else 2) for case in row] for row in plateau]

    # Trouver les cases vides
    choix_possibles = [i for i in range(9) if plateau_num[i // 3][i % 3] == 0]

    # Choisir un emplacement aléatoire parmi les cases vides
    if choix_possibles:
        choix = random.choice(choix_possibles)
        return (choix // 3, choix % 3)  # Convertir l'indice en coordonnées (row, col)
    else:
        return False