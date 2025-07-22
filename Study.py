import time
import matplotlib.pyplot as plt
from Game import Game
from Sudoku import Sudoku  # Assuming Sudoku and Game classes are defined


class ComplexityStudy:
    def __init__(self, sudoku_files):
        self.sudoku_files = sudoku_files  # List of Sudoku file paths
        self.heuristics = ["default", "MRV", "Degree", "ConstraintPropagation"]
        self.results = []

    def run_study(self):
        """Runs the complexity study on different Sudoku puzzles with different heuristics."""
        for sudoku_file in self.sudoku_files:
            for heuristic in self.heuristics:
                for backtracking in [False, True]:

                    print(f"Testing {sudoku_file} with {heuristic} heuristic...")
                    solved, time_taken, iterations = self.run_solver(sudoku_file, heuristic)

                    self.results.append({
                        "puzzle": sudoku_file,
                        "heuristic": heuristic,
                        "solved": solved,
                        "time": time_taken,
                        "iterations": iterations
                    })

            self.print_summary()
            self.plot_results()

    def run_solver(self, sudoku_file, heuristic):
        """Runs the Sudoku solver and records performance metrics."""
        sudoku = Sudoku(sudoku_file)
        game = Game(sudoku)

        start_time = time.time()
        iterations = 0  # Track number of iterations

        # Modify solve function to count iterations
        def track_iterations():
            nonlocal iterations
            iterations += 1

        # Attach tracking to backtracking function
        original_backtrack = game.backtrack
        def modified_backtrack(assignment):
            track_iterations()
            return original_backtrack(assignment)

        game.backtrack = modified_backtrack

        # Solve the Sudoku
        solved = game.solve(heuristic, use_backtracking=True)
        time_taken = time.time() - start_time

        return solved, time_taken, iterations

    def print_summary(self):
        """Prints a summary of the results."""
        print("\n=== Complexity Study Summary ===")
        for result in self.results:
            print(f"Puzzle: {result['puzzle']} | Heuristic: {result['heuristic']} | "
                  f"Solved: {result['solved']} | Time: {result['time']:.4f}s | Iterations: {result['iterations']}")

    def plot_results(self):
        """Plots a graph comparing heuristic performance."""
        difficulties = list(set(result["puzzle"] for result in self.results))
        heuristics = self.heuristics

        plt.figure(figsize=(10, 5))

        for heuristic in heuristics:
            times = [result["time"] for result in self.results if result["heuristic"] == heuristic]
            plt.plot(difficulties, times, label=heuristic, marker='o')

        plt.xlabel("Sudoku Puzzle")
        plt.ylabel("Time (seconds)")
        plt.title("Sudoku Solving Time Comparison")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid()
        plt.show()
