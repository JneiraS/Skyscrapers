import copy
import random
from itertools import permutations


class Grid:
    """
    Représente une grille de dimensions spécifiques.

    Cette classe permet de créer une grille vide de dimensions données et de manipuler cette grille.
    """

    def __init__(self, dimension):
        """
        Initialise une nouvelle instance de Grid avec une grille vide de dimensions spécifiées.

        Paramètres :
        - dimension (int) : La dimension de la grille, c'est-à-dire le nombre de lignes et de colonnes.

        Note : La grille est initialisée comme une liste de listes vides, représentant une grille vide.
        """
        self._dimension = dimension
        self.grid = [[] for _ in range(self._dimension)]

    # def empty_grid(self):
    #     """
    #     Génère une grille vide de dimensions spécifiées.
    #
    #     Retourne :
    #     - list : Une liste de listes vides, représentant une grille vide de dimensions spécifiées.
    #
    #     Note : Cette méthode est utilisée pour initialiser la grille lors de l'instanciation de la classe Grid.
    #     """
    #     return

    def generate_valid_configuration(self, seed_number: int):
        """
        Génère une configuration valide de la grille en utilisant des permutations aléatoires de hauteurs de bâtiments.

        Cette méthode procède de la manière suivante :
        1. Génère une liste de hauteurs de bâtiments possibles en fonction de la dimension de la grille.
        2. Calcule toutes les permutations possibles de ces hauteurs de bâtiments.
        3. Pour chaque position dans la grille, sélectionne aléatoirement une permutation unique de hauteurs de
        bâtiments
           qui n'a pas encore été utilisée dans cette position, en s'assurant qu'il n'y a pas de doublons.
        4. Attribue cette configuration unique à la grille.
        5. Ajoute des indices ou des "clues" à la grille pour faciliter le jeu ou la résolution du puzzle.
        6. Retourne `self` pour permettre la chaînage des méthodes.

        Returns:
            self -- La grille mise à jour avec une nouvelle configuration valide et des indices.
        """

        buildings_heights = [i for i in range(1, self._dimension + 1)]
        grid_filled: list = []

        perms: list = list(permutations(buildings_heights))

        for j in range(self._dimension):
            random.seed(seed_number)
            buildings = random.choice(perms)
            grid_filled.append(list(buildings))

            for i in range(self._dimension):
                perms = [tup for tup in perms if not tup[i] == grid_filled[j][i]]

        self.grid = grid_filled
        self.add_clues()
        return self

    def add_clues(self) -> None:
        """
        Ajoute des indices ou des "clues" à la grille pour faciliter le jeu ou la résolution du puzzle.

        Cette méthode procède de la manière suivante :
        1. Initialise une liste de placeholders (-1) pour les indices/clues en haut et en bas de la grille.
        2. Pour chaque ligne de la grille, insère un indice (0) au début et à la fin de la ligne, préparant ainsi
        l'espace pour les indices ou clues.
        3. Ajoute les placeholders (indices/clues) en haut et en bas de la grille principale, représentant les indices
        ou clues en haut et en bas de la grille globale.

        Note : Les placeholders (-1) sont utilisés pour indiquer les positions où les indices ou clues seront placés.

        Returns:
            None
        """
        top_and_bottom_clues = [-1, -1]

        for _ in self.grid:
            top_and_bottom_clues.insert(1, 0)

        for i in self.grid:
            i.insert(0, 0)
            i.append(0)

        self.grid.insert(0, top_and_bottom_clues)
        self.grid.append(top_and_bottom_clues)


class GridFactory:
    """
    Classe Factory pour la création de configurations de grille valides.

    Cette classe fournit une méthode statique pour générer une instance de grille avec une configuration valide,
    basée sur une dimension spécifique et un nombre de graine (seed).
    """

    @staticmethod
    def grid_filler(dimension: int, seed_number: int) -> Grid:
        """
        Génère une configuration de grille valide basée sur la dimension spécifiée et le nombre de graine (seed).

        Paramètres :
        - dimension (int) : La dimension de la grille à générer.
        - seed_number (int) : Le nombre de graine utilisé pour initialiser le générateur de nombres aléatoires.

        Retourne :
        - Grid : Une instance de grille avec une configuration valide pour la dimension spécifiée, initialement générée
        avec le nombre de graine fourni.

        Note : La méthode retourne une nouvelle instance de grille et ne modifie pas les grilles existantes.
        """
        return Grid(dimension).generate_valid_configuration(seed_number)


def transpose(grille: list) -> list:
    """
    Transpose un tableau.

    Paramètres :
    - grille (list) : Un tableau représenté comme une liste de listes, où chaque sous-liste représente une ligne du
    tableau.

    Retourne :
    - list : Le tableau transposé.

    Note : Cette fonction retourne un nouveau tableau et ne modifie pas le tableau original.
    """
    new_grid = []

    for line in range(len(grille)):
        new_line = [i[line] for i in reversed(grille)]
        new_grid.append(new_line)

    return new_grid


def indice_adder(indices: list, grid: list):
    """
    Ajoute les indices fournis au début de chaque ligne interne d'un tableau, en commençant par la deuxième ligne et
    en excluant la dernière ligne.

    Paramètres :
    - indices (list) : Une liste contenant les indices à ajouter au tableau.
    - grid (list) : Un tableau représenté comme une liste de listes, où chaque sous-liste
    représente une ligne du tableau.

    Retourne :
    - list : Le tableau original avec les indices ajoutés au début de chaque ligne interne.

    Note : Cette fonction modifie le tableau original. Si vous souhaitez conserver le tableau original intact,
    procédez à une copie avant d'appeler cette fonction.
    """
    for i in range(1, len(grid) - 1):
        grid[i].pop(0)
        grid[i].insert(0, indices[i - 1])
    return grid


def clues(grille: list) -> list:
    """
    Calcule les indices d'une grille en comptant le nombre de fois où une valeur augmente par rapport à la précédente
    dans chaque ligne,excluant les bordures extérieures.

    Paramètres :
    - grille (list) : Le tableau d'entrée dont les indices doivent être calculés.

    Retourne :
    - list : Une liste contenant les indices calculés pour chaque ligne de la grille.
    """
    row_increase_counts = []
    inner_dimension = (
        len(grille[0]) - 2
    )  # Dimension intérieure pour exclure les bordures

    for rowIndex in range(1, inner_dimension + 1):
        current_value = 0
        increase_count = 0

        for columnValue in grille[rowIndex]:
            if columnValue > current_value:
                increase_count += 1
                current_value = columnValue

        row_increase_counts.append(increase_count)

    return row_increase_counts


def raw_grids_generator(grid_seize: int, seed_number: int) -> tuple:
    """
    Génère deux versions d'un tableau basé sur la taille et le numéro de 'seed'.

    Paramètres :
    - grid_seize (int) : La taille du tableau à générer.
    - seed_number (int) : Une valeur de graine utilisée pour initialiser le processus de remplissage du tableau.

    Retourne :
    - tuple : Un tuple contenant deux tableaux.
      - Le premier élément est l'`empty_grid_for_play`, qui est une copie profonde du tableau original mais avec '-1'
       insérés autour du périmètre pour indiquer les zones non jouables.
      - Le second élément est le `grille`, qui est le tableau transformé final après avoir appliqué des indices et des
       transpositions quatre fois.

    Processus :
    1. Initialise le tableau en utilisant une méthode de remplissage de tableau à partir d'une instance de GridFactory,
    en utilisant la taille de tableau et le numéro de seed fournis.
    2. Applique une série de transformations au tableau, y compris l'ajout d'indices et la transposition du tableau,
    répétées quatre fois.
    3. Crée une copie profonde du tableau final pour le préparer au jeu, en insérant '-1' autour du périmètre pour
    marquer les zones non jouables.
    4. Retourne à la fois le tableau préparé pour le jeu et le tableau transformé final.
    """
    board = GridFactory().grid_filler(grid_seize, seed_number)
    grille = board.grid
    for _ in range(4):
        indices = clues(grille)
        grille = transpose(indice_adder(indices, grille))
    empty_grid_for_play = copy.deepcopy(grille)
    for i in range(1, len(empty_grid_for_play) - 1):
        for j in range(1, len(empty_grid_for_play[i]) - 1):
            empty_grid_for_play[i].pop(j)
            empty_grid_for_play[i].insert(j, -1)
    return empty_grid_for_play, grille
