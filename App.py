import os
from Game import Game
from Sudoku import Sudoku

sudoku_folder = os.path.join(os.path.dirname(__file__), "Sudokus")

class App:


    @staticmethod
    def solve_sudoku(sudoku_file, heuristic="default", use_backtracking=False):
        game = Game(Sudoku(sudoku_file))
        game.show_sudoku()
        if game.solve(heuristic, use_backtracking) and game.valid_solution():
            print("Solved!")
        else:
            print("Could not solve this sudoku :(")

    @staticmethod
    def start():
        while True:
            file_num = input("Enter Sudoku file (1-5): ")
            heuristic_choice = input("Choose heuristic (default/MRV/Degree/ConstraintPropagation): ").strip().lower()
            use_backtracking = input("Use backtracking? (yes/no): ").strip().lower() == "yes"
            choice = input("Do you want to do a complexity study? (yes/no): ").strip().lower()
            print(f"Final use_backtracking value: {use_backtracking}")  # Debug print
            print("\n")

            file = None
            for filename in os.listdir(sudoku_folder):
                if file_num in filename:
                    file = filename
            if file is not None:
                print(f"Using backtracking: {use_backtracking}")
                App.solve_sudoku(os.path.join(sudoku_folder, file), heuristic_choice, use_backtracking)
            else:
                print("Invalid choice")

            if choice == "yes":
                Game.complexity_study()
            else:
                continue

            continue_input = input("Continue? (yes/no): ")
            if continue_input.lower() != 'yes':
                break


if __name__ == "__main__":
    App.start()

