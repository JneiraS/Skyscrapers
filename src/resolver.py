import random
from itertools import permutations
from src.grid import transpose, clues, indice_adder, Grid

results_to_insert: list = []
grid_filled: list = []


def permutations_possibles(grid_seize: int):
    """
    Génère toutes les permutations possibles de hauteurs de bâtiments pour un grille de taille 'grid_seize'.
    Cette fonction crée une liste de hauteurs de bâtiments allant de 1 à 'grid_seize', puis génère toutes les
    permutations possibles de ces hauteurs.
    Ces permutations représentent toutes les configurations possibles de hauteurs de bâtiments dans un grille donné.

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
    :return list: Une nouvelle liste où tous les zéros ont été remplacés par remaining_possibilities, tandis que les autres
     valeurs restent inchangées.
    """
    return [remaining_possibilities if e == 0 else e for e in original_list]


def replace_list_of_possibilities_whit_0(original_list):
    """
    Remplace tous les éléments de liste dans original_list par 0.
    Parcourt chaque élément de original_list. Si l'élément est lui-même une liste, il est remplacé par 0. Sinon,
    l'élément reste inchangé.

    :param original_list: La liste originale dont certains éléments (qui sont eux-mêmes des listes) doivent être
     remplacés par 0.
    :return list: Une nouvelle liste où tous les éléments qui étaient des listes ont été remplacés par 0, tandis que les autres valeurs restent inchangées.
    """
    return [0 if isinstance(e, list) else e for e in original_list]


def determine_last_line(list_to_analyse: list):
    perms = permutations_possibles(4)

    for j in range(1, 4):
        for i in range(4):
            perms = [
                line
                for line in perms
                if line[i] != list_to_analyse[j][i + 1]
                   or list_to_analyse[j][i + 1] == 0
            ]

    for i in range(4):
        perms = [
            line
            for line in perms
            if line[i] == list_to_analyse[4][i + 1] or list_to_analyse[4][i + 1] == 0
        ]

    return perms


def generate_game_configurations(game_grid: list):
    grid_dimension = len(game_grid) - 2
    modified_new_grid = []
    modified_new_grid2 = []

    base = {i for i in range(grid_dimension + 1)}

    for i in range(4):

        for row in game_grid:
            if row[0] == 1:
                row.pop(1)
                row.insert(1, grid_dimension)

            elif row[0] == grid_dimension:
                for j in range(1, grid_dimension + 1):
                    row.pop(j)
                    row.insert(j, j)

            elif row[0] == 1 and row[-1] == 2:
                row.pop(-2)
                row.insert(-1, grid_dimension - 1)

        game_grid = transpose(game_grid)

    for row in game_grid:
        remaining_possibilities = list(base - {e for e in row[1:-1]})
        modified_new_grid.append(replace_zeros_with_list_of_possibilities(row, remaining_possibilities))

    for i in range(4):
        for row in modified_new_grid:
            if row[0] == 1 and row[-1] == 3 and row[1] == 4 and row[2] == 3:
                temp_element = row.pop(-2)

                try:
                    num = temp_element[-1]
                    row.insert(-1, num)
                except IndexError:
                    row.insert(-1, temp_element)
        modified_new_grid = transpose(modified_new_grid)

    for row in modified_new_grid:
        modified_new_grid2.append(replace_list_of_possibilities_whit_0(row))
    return modified_new_grid2


def decalage(grid_to_decale: list, origine: int, destination: int):
    temp_line = grid_to_decale.pop(origine)
    grid_to_decale.insert(destination, temp_line)


def adaptive_game_grid_generation(game_grid):
    grid_with_euristics = generate_game_configurations(game_grid)

    empty_grid = []

    for _ in range(4):
        last_line_result = determine_last_line(grid_with_euristics)
        empty_grid.append(last_line_result)
        line_two = grid_with_euristics.pop(1)
        grid_with_euristics.insert(4, line_two)

    possibles_results_by_line = empty_grid.copy()

    line_two = possibles_results_by_line.pop(0)
    possibles_results_by_line.insert(2, line_two)

    line_two = possibles_results_by_line.pop(0)
    possibles_results_by_line.insert(1, line_two)

    buildings = random.choice(possibles_results_by_line[0])
    empty_grid_to_fill = [list(buildings)]

    for i in possibles_results_by_line[1:]:
        k = random.choice(i)
        for j in range(4):
            if empty_grid_to_fill[0][j] == k[j]:
                pass
            else:
                empty_grid_to_fill.append(list(k))
                break

    line_two = empty_grid_to_fill.pop(0)
    empty_grid_to_fill.insert(1, line_two)

    line_two = empty_grid_to_fill.pop(2)
    empty_grid_to_fill.insert(3, line_two)
    return empty_grid_to_fill


def rotate_lists_of_lists(liste):
    """
    Effectue une rotation de toutes les sous-listes dans une liste de listes.

    Args:
    - liste : Liste de listes dont les sous-listes doivent être rotées.

    Returns:
    - Une nouvelle liste de listes avec toutes les sous-listes rotées.
    """
    return [[liste[j][i] for j in range(len(liste))] for i in range(len(liste[0]))]


grid = [
    [-1, 4, 2, 1, 3, -1],
    [3, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 3],
    [-1, 1, 2, 2, 2, -1],
]

while True:

    original = adaptive_game_grid_generation(grid)
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

# grid_printer(gridd)
