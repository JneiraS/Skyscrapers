import random, timeit


class Grid:

    def __init__(self, dimension):
        self._dimension = dimension

    def empty_grid(self):
        return [[] for i in range(self._dimension)]


def transpose(grid: list) -> list:
    """
    Effectue une rotation de 90 degrés de la grille.
    """
    new_grid = []
    for line in range(len(grid)):
        new_line = [i[line] for i in reversed(grid)]
        new_grid.append(new_line)

    return new_grid


def duplicate_checker(grid: list) -> bool:
    """
    Vérifie si toutes les lignes d'une grille sont uniques.
    Retourne True si toutes les lignes sont uniques, False sinon.
    """
    return all(len(row) == len(set(row)) for row in grid)


def step_one(grid):
    for i in range(len(grid)):
        buildings_heights = [i for i in range(1, len(grid) + 1)]
        for _ in range(len(buildings_heights)):
            building = random.choice(buildings_heights)
            buildings_heights.remove(building)
            grid[i].append(building)
    return grid


def step_tow(dimension: int):
    while True:

        grille = Grid(dimension).empty_grid()

        grille = step_one(grille)
        r = transpose(grille)
        if duplicate_checker(r):
            break
    return grille


if __name__ == "__main__":

    print(step_tow(5))

    # loop_time = timeit.timeit("step_tow(4)", globals=globals(), number=1)
    # print(f"Temps d'exécution: {loop_time/10:.3f} secondes")

# Temps d'exécution:  0.005 secondes pout 4x4
# Temps d'exécution: 0.889 secondes pout 5x5
