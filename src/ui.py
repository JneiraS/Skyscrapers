import random


def bars(cell):
    horrizontal_bar = "---"
    intersections = "+"
    return ((intersections + horrizontal_bar) * cell) + intersections


def line_printer(line: list):
    print(
        f"| {' | '.join([str(i).replace('-1', ' ') for i in line])} |\n{bars(len(line))}"
    )


def grid_printer(grid):
    print(bars(len(grid)))
    for i in grid:
        line_printer(i)


def id_generator():
    """
    Génère un identifiant unique (ID) basé sur la taille de la grille saisie par l'utilisateur.

    Cette fonction calcule le certains nombre résultats possibles en fonction de la taille de la grille et
    sélectionne un nombre aléatoire parmi ceux-ci pour servir d'ID unique.

    Retourne :
    - tuple : Un tuple contenant deux éléments.
      - Le premier élément est la taille de la grille saisie par l'utilisateur.
      - Le deuxième élément est un nombre aléatoire sélectionné parmi les résultats possibles, servant d'ID unique.

    Note : La fonction utilise la bibliothèque standard Python `random` pour générer le nombre aléatoire.
    """
    responses = int(input("Taille de la Grille (idéalement de 4 à 8): "))
    # number_of_results = int(responses**responses * responses / 2)
    number_of_results = 10**5

    return responses, random.choice([i for i in range(1, number_of_results)])


def grid_generator(empty_grid_for_play, grille, seed_number):
    """
    Affiche une grille de jeu et une grille de solution, permettant à l'utilisateur de choisir s'il souhaite  regarder
     la solution ou non.

    Cette fonction est principalement interactive et ne retourne pas de valeur explicite.

    Paramètres :
    - empty_grid_for_play (list) : La grille de jeu prête à être jouée.
    - grille (list) : La grille de solution, montrant la disposition finale souhaitée.
    - seed_number (int) : Le numéro de graine utilisé pour générer les grilles, affiché à titre d'ID.

    Interaction :
    - L'utilisateur est invité à appuyer sur Entrée pour voir la solution.
    - Pendant que l'option 'quitter' est 'n', la fonction continue à afficher la grille de solution et demande à
    l'utilisateur s'il souhaite quitter ou non.

    Note : Cette fonction est destinée à être utilisée dans un environnement interactif tel qu'un terminal ou une
    interface graphique, où l'utilisateur peut entrer des commandes textuelles.
    """
    quitter = "n"
    print(f" ID:{seed_number}")
    grid_printer(empty_grid_for_play)
    input(" Appuyez sur entrée pour voir la solution:")
    while quitter == "n":
        grid_printer(grille)
        quitter = input("Quitter ? (o/n)")
