from src.grid import raw_grids_generator
from src.ui import id_generator, grid_generator, grid_printer


def main():

    grid_seize, seed_number = id_generator()
    empty_grid_for_play, grille = raw_grids_generator(grid_seize, seed_number)
    generate_or_solve = input(
        f"Générer une grille ou résoudre une grille en fonction de son ID"
        f"\nGénerer (1)"
        f"\nSolution (2)"
        f"\nRéponse: "
    )

    if generate_or_solve == "1":
        grid_generator(empty_grid_for_play, grille, seed_number)
    else:
        id_number = int(input("ID de la grille: "))
        empty_grid_for_play, grille = raw_grids_generator(grid_seize, id_number)
        grid_printer(grille)


if __name__ == "__main__":
    main()
