import random
from itertools import permutations
from src.grid import transpose, clues, indice_adder, Grid
from src.ui import grid_printer

results_to_insert: list = []
grid_filled: list = []


def permutations_possibles(grid_seize: int):
    """
    Génère toutes les permutations possibles de hauteurs de bâtiments pour une grille de taille 'grid_seize'.
    Cette fonction crée une liste de hauteurs de bâtiments allant de 1 à 'grid_seize', puis génère toutes les
    permutations possibles de ces hauteurs.
    Ces permutations représentent toutes les configurations possibles de hauteurs de bâtiments dans une grille donnée.

    :param grid_seize:
    :return list: Une liste de tuples, où chaque tuple représente une permutation possible des hauteurs de
    bâtiments. Chaque tuple contient 'grid_seize' éléments, chacun étant une hauteur de bâtiment valide dans la grille.
    """
    buildings_heights = [height for height in range(1, grid_seize + 1)]
    return list(permutations(buildings_heights))


def replace_zeros_with_list_of_possibilities(original_list: list, remaining_possibilities: list):
    """
    Remplace tous les zéros dans original-list par remaining_possibilities.
    Parcourt chaque élément de original_list et le remplace par rest si l'élément est égal à 0. Autrement dit,
    transforme les zéros en remaining_possibilities, tout en conservant les autres valeurs inchangées.
    :param original_list: La liste originale dont certains éléments doivent être remplacés par remaining_possibilities.
    remaining_possibilities (any): L'élément avec lequel remplacer les zéros dans original_list.
    :param remaining_possibilities:  L'élément avec lequel remplacer les zéros dans original_list.
    :return list: Une nouvelle liste où tous les zéros ont été remplacés par remaining_possibilities, tandis que les
    autres valeurs restent inchangées.
    """
    return [remaining_possibilities if e == 0 else e for e in original_list]


def replace_list_of_possibilities_whit_0(original_list):
    """
    Remplace tous les éléments de liste dans original_list par 0.
    Parcourt chaque élément de original_list. Si l'élément est lui-même une liste, il est remplacé par 0. Sinon,
    l'élément reste inchangé.

    :param original_list: La liste originale dont certains éléments (qui sont eux-mêmes des listes) doivent être
     remplacés par 0.
    :return list: Une nouvelle liste où tous les éléments qui étaient des listes ont été remplacés par 0, tandis que
    les autres valeurs restent inchangées.
    """
    return [0 if isinstance(e, list) else e for e in original_list]


def determine_last_line(list_to_analyse: list):
    """
    Filtre les permutations possibles pour trouver celles qui correspondent à une configuration spécifique de la
    dernière ligne d’une grille.
    Cette fonction prend en entrée une liste représentant la configuration de la dernière ligne d’une grille et filtre
    les permutations possibles de hauteurs de bâtiments pour une grille de taille 4x4, afin de ne garder que celles
    qui correspondent à la configuration spécifiée pour la dernière ligne, en tenant compte des conditions spécifiées
    pour chaque côté de la ligne.

    :param list_to_analyse: Liste représentant la configuration de la dernière ligne de la grille, où chaque
    élément de la liste est une hauteur de bâtiment et 'zéro' indique l'absence de bâtiment.
    :return list: Une liste filtrée de permutations possibles qui correspondent à la configuration spécifiée pour la
    dernière ligne de la grille.
    """
    perms: list = permutations_possibles(4)
    for j in range(1, 4):
        for side in range(4):
            perms = [
                line for line in perms if
                line[side] != list_to_analyse[j][side + 1] or list_to_analyse[j][side + 1] == 0
            ]
    for side in range(4):
        perms = [
            line
            for line in perms
            if line[side] == list_to_analyse[4][side + 1] or list_to_analyse[4][side + 1] == 0
        ]
    return perms


def heuristics_determination(game_grid: list, grid_dimension: int):
    """
    Applique une heuristique de détermination des hauteurs de bâtiments pour une grille de jeu, en ajustant les
    hauteurs des bâtiments selon certaines règles et en transposant la grille.
    Cette fonction modifie la grille de jeu en fonction de ses dimensions actuelles, en ajustant les hauteurs des
    bâtiments pour optimiser une certaine condition (par exemple, maximiser la différence entre les hauteurs des
    bâtiments adjacents). Elle applique ensuite une transformation de la grille (transpose) pour préparer la grille à
    une nouvelle analyse.
    :param game_grid: (list) La grille de jeu sous forme de liste de listes, où chaque sous-liste représente une
    ligne de la grille.
    :param grid_dimension: (int): La dimension de la grille, c'est-à-dire le nombre maximum de niveaux de hauteur
    possible pour les bâtiments.
    :return: (tuple): Un tuple contenant deux éléments:
        - Une collection (set) des hauteurs de bâtiments possibles après l'application de l'heuristique.
    - La grille de jeu transposée, prête à une nouvelle analyse ou simulation.

    Notes: Cette fonction suppose que la fonction `transpose` est déjà définie et capable de transposer
    la grille de jeu.

    """
    base = {possible_building_heights for possible_building_heights in range(grid_dimension + 1)}
    for side_of_grid in range(4):

        for row in game_grid:
            if row[0] == 1 and row[-1] == 2:
                row.pop(-2)
                row.insert(-1, grid_dimension - 1)

            elif row[0] == 1:
                row.pop(1)
                row.insert(1, grid_dimension)

            elif row[0] == grid_dimension:
                for j in range(1, grid_dimension + 1):
                    row.pop(j)
                    row.insert(j, j)

        game_grid = transpose(game_grid)
    return base, game_grid


def generate_game_configurations(game_grid: list):
    grid_dimension = len(game_grid) - 2
    modified_grid = []
    modified_grid_2 = []

    base, game_grid = heuristics_determination(game_grid, grid_dimension)

    for row in game_grid:
        remaining_possibilities = list(base - {e for e in row[1:-1]})
        modified_grid.append(replace_zeros_with_list_of_possibilities(row, remaining_possibilities))

    for side_of_grid in range(4):
        for row in modified_grid:
            if row[0] == 1 and row[-1] == 3 and row[1] == 4 and row[2] == 3:
                temp_element = row.pop(-2)

                try:
                    num = temp_element[-1]
                    row.insert(-1, num)
                except IndexError:
                    row.insert(-1, temp_element)
        modified_grid = transpose(modified_grid)

    for row in modified_grid:
        modified_grid_2.append(replace_list_of_possibilities_whit_0(row))
    return modified_grid_2


def position_change(grid_to_change: list, origine: int, destination: int):
    temp_line = grid_to_change.pop(origine)
    grid_to_change.insert(destination, temp_line)


def fill_grid_with_choices(empty_grid_to_fill, possibles_results_by_line):
    """
    Remplit une grille vide avec des choix provenant d'une liste de résultats possibles.

    Cette fonction itère sur une liste de résultats possibles, sélectionnant un choix aléatoire de chacun. Elle vérifie
    ensuite
    si l'élément sélectionné répond à une condition spécifique dans la grille vide à remplir. Si la condition est
    remplie, l'élément
    sélectionné est ajouté à la nouvelle grille.

    Args:
        empty_grid_to_fill (list): Une grille vide représentée comme une liste de listes, prête à être remplie avec des
        choix.
        possibles_results_by_line (list): Une liste de résultats possibles, où chaque élément représente un choix
        potentiel pour remplir la grille.

    Returns:
        None: Modifie le paramètre empty_grid_to_fill en place.
    """
    for possible_result in possibles_results_by_line[1:]:
        k = random.choice(possible_result)
        for j in range(4):
            if empty_grid_to_fill[0][j] == k[j]:
                pass
            else:
                empty_grid_to_fill.append(list(k))
                break


def adjust_game_board(game_grid):
    """
    Génère une grille de jeu adaptative en appliquant des heuristiques et en ajustant les configurations de jeu.

    Cette fonction commence par générer des configurations de jeu à partir de la grille de jeu initiale en utilisant une
    fonction d'heuristique. Ensuite, elle adapte la grille générée en ajoutant et en supprimant des lignes spécifiques
    pour optimiser certaines conditions de jeu. Des changements de position sont appliqués pour diversifier les
    résultats possibles par ligne.
    Enfin, une grille vide est remplie avec des choix aléatoires basés sur les résultats possibles, avec des ajustements
    supplémentaires pour optimiser davantage la configuration finale.

    Args:
        game_grid (list): La grille de jeu initiale sous forme de liste de listes, où chaque sous-liste représente une
        ligne de la grille.

    Returns:
        list: Une grille de jeu adaptative et optimisée, prête à être utilisée pour le jeu.

    Notes:
        Cette fonction suppose que plusieurs fonctions auxiliaires sont déjà définies et capables de réaliser les tâches
        suivantes :
        - generate_game_configurations: Génère des configurations de jeu à partir de la grille de jeu initiale.
        - determine_last_line: Détermine la dernière ligne de la grille générée selon certaines heuristiques.
        - position_change: Change la position d'un élément dans une liste pour diversifier les résultats possibles.
        - fill_grid_with_choices: Remplit une grille vide avec des choix aléatoires basés sur les résultats possibles.

    :param game_grid:
    :return:
    """
    grid_with_heuristics = generate_game_configurations(game_grid)

    empty_grid = []

    for _ in range(4):
        last_line_result = determine_last_line(grid_with_heuristics)
        empty_grid.append(last_line_result)
        line_two = grid_with_heuristics.pop(1)
        grid_with_heuristics.insert(4, line_two)

    possibles_results_by_line = empty_grid.copy()
    position_change(possibles_results_by_line, 0, 2)
    position_change(possibles_results_by_line, 0, 1)
    buildings = random.choice(possibles_results_by_line[0])
    empty_grid_to_fill = [list(buildings)]
    fill_grid_with_choices(empty_grid_to_fill, possibles_results_by_line)
    position_change(empty_grid_to_fill, 0, 1)
    position_change(empty_grid_to_fill, 2, 3)

    return empty_grid_to_fill


def rotate_lists_of_lists(liste):
    """
    Effectue une rotation de toutes les sous-listes dans une liste de listes dans le sens anti-horaire.

    Args:
    - liste: Liste de listes dont les sous-listes doivent être pivotées.
    Returns:
    - Une nouvelle liste de listes avec toutes les sous-listes pivotées.
    """
    return [[liste[j][k] for j in range(len(liste))] for k in range(len(liste[0]))]


grid = [
    [-1, 4, 2, 1, 3, -1],
    [3, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 3],
    [-1, 1, 2, 2, 2, -1],
]

while True:

    original = adjust_game_board(grid)
    tocheckt = rotate_lists_of_lists(original)
    container = []

    for i in tocheckt:
        container.append(len(list(set(i))))

    if container == [4, 4, 4, 4]:
        break

grid_to_find_solution = Grid(4)
grid_to_find_solution.grid = original
grid_to_find_solution.add_clues()

gridd = grid_to_find_solution.grid

for _ in range(4):
    indices = clues(gridd)
    gridd = transpose(indice_adder(indices, gridd))

grid_printer(gridd)

