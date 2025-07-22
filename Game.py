from collections import deque
from Sudoku import Sudoku
import time
import matplotlib.pyplot as plt
import pandas as pd
import os
sudoku_folder = os.path.join(os.path.dirname(__file__), "Sudokus")




class Game:

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.ac3_iterations = 0
        self.backtrack_iterations = 0
        self.start_time = 0

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self, heuristic="default", use_backtracking=False) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        grid = self.sudoku.get_board()
        queue = self.initialize_queue(grid, heuristic)
        self.ac3_iterations = 0
        self.backtrack_iterations = 0
        self.start_time = time.time()


        while queue: #while loop, stops when queue empties
            self.ac3_iterations += 1  # Track AC-3 iterations
            (x,y) = queue.popleft() #Eliminate current arc (already used) on the queue
            if self.revise(x,y):  #Reduce domain of X
                if len(x.get_domain()) == 0: #If there are no possible values left in the domain, the sudoku is not solvable
                    return False
                for z in x.get_neighbours():
                    if z != y and (z,x) not in queue:
                        queue.append((z,x))

        is_complete = self.is_complete(self.get_assignment())
        if is_complete:
            return True

        # If not fully solved, use backtracking
        if use_backtracking:
            return self.backtracking_search()
        else:
            return False





    def revise(self, x, y) -> bool:
        """
        Checks ach value in X's domain to see if there's a compatible value in Y's domain. For Sudoku, compatibility is x != y
        @return: true if the sudoku solution is correct
        """
        # TODO: implement valid_solution function
        revised = False
        domain_x = x.get_domain()
        value_y = y.get_value()

        if value_y != '.' and value_y in domain_x:
            x.remove_from_domain(value_y)
            revised = True

        return revised


    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        # TODO: implement valid_solution function

        grid = self.sudoku.get_board()

        #Check rows, columns, and 3x3 boxes
        for i in range(9):
            row_values = set()
            col_values = set()


            for j in range(9):
                row_value = grid[i][j].get_value()
                col_value = grid[j][i].get_value()

                if row_value in row_values or col_value in col_values:
                    return False  # Duplicate found, invalid solution

                row_values.add(row_value)
                col_values.add(col_value)


        # Check 3x3 subgrids
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box_values = set()
                for i in range(3):
                    for j in range(3):
                        val = grid[box_row + i][box_col + j].get_value()
                        if val in box_values:
                            return False
                        box_values.add(val)

        print("Sudoku solution is valid!")
        return True




    def initialize_queue(self, grid, heuristic="default"):
        """
        Initializes the queue with different heuristics.
        :param grid: The Sudoku board.
        :param heuristic: The heuristic to use ("MRV", "Degree", "ConstraintPropagation", etc.).
        :return: The initialized queue.
        """
        queue = deque()

        if heuristic == "MRV":
        # Sort all arcs based on the domain size of X
            arcs = []
            for i in range(9):
                for j in range(9):
                    field = grid[i][j]
                    for neighbor in field.get_neighbours():
                        arcs.append((len(field.get_domain()), id(field), field, neighbor))

            arcs.sort(key=lambda arc: (arc[0], arc[1]))  # Sort by domain size first, then tie-break with id
            queue.extend([(x, y) for _, _, x, y in arcs])


        elif heuristic == "Degree":
            # Sort based on the number of constraints (neighbors)
            arcs = []
            for i in range(9):
                for j in range(9):
                    field = grid[i][j]
                    for neighbor in field.get_neighbours():
                        arcs.append((-len(field.get_neighbours()), id(field), field, neighbor))

            arcs.sort(key=lambda arc: (arc[0], arc[1]))  # Most constrained variable first
            queue.extend([(x, y) for _, _, x, y in arcs])


        elif heuristic == "ConstraintPropagation":
            priority_arcs = []
            normal_arcs = []
            for i in range(9):
                for j in range(9):
                    field = grid[i][j]
                    for neighbour in field.get_neighbours():
                        if neighbour.get_value() != 0:
                            priority_arcs.append((field, neighbour))  # Prioritize arcs where Y is assigned
                        else:
                            normal_arcs.append((field, neighbour))
            queue = deque(priority_arcs + normal_arcs) #makes a complete queue with the priority arcs first and the other at the end


        else:  # Default, does normal order going left to right for each row top down
            queue = deque()
            for i in range(9):
                for j in range(9):
                    field = grid[i][j]
                    for neighbour in field.get_neighbours():
                        queue.append((field, neighbour))

        return queue

    def backtracking_search(self):
        """
        Solves the Sudoku using backtracking search.
        :return: True if solved, False otherwise.
        """
        print("Starting Backtracking Search...")
        assignment = self.get_assignment()
        result = self.backtrack(assignment)
        if result is not None:
            print("Sudoku solved with backtracking!")
            return True
        print("Backtracking failed to find a solution.")
        return False

    def backtrack(self, assignment):
        self.backtrack_iterations += 1

        if self.is_complete(assignment):
            print("Solution found!")
            return assignment

        var = self.select_unassigned_variable(assignment)
        if var is None:
            return None  # Prevents infinite recursion

        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                var.set_value(value)
                assignment[var] = value


                result = self.backtrack(assignment)
                if result is not None:
                    return result  # Solution found
                # Backtrack: reset the Field's value and remove from assignment
                var.set_value(0)
                del assignment[var]

        return None  # Failure, triggers backtracking


    def get_assignment(self):
        """Returns the current assignment (filled and unfilled cells)."""
        assignment = {cell: cell.get_value() for row in self.sudoku.get_board() for cell in row if cell.get_value() != 0}
        return assignment



    def is_complete(self, assignment) -> bool:
        """Checks if all cells are assigned."""
        return all(cell.get_value() != 0 for row in self.sudoku.get_board() for cell in row)

    def select_unassigned_variable(self, assignment):
        """Selects the next empty cell using MRV heuristic."""
        unassigned = [cell for row in self.sudoku.get_board() for cell in row if cell.get_value() == 0]  # Only select cells that are truly empty
        if not unassigned:
            return None  # No unassigned variables left
        return min(unassigned, key=lambda cell: len(cell.get_domain()))  # MRV heuristic

    def order_domain_values(self, var, assignment):
        """Orders domain values using LCV heuristic."""
        return sorted(var.get_domain(), key=lambda val: self.count_conflicts(var, val, assignment))

    def is_consistent(self, var, value, assignment) -> bool:
        """Checks if a value can be assigned to a cell without conflicts."""
        conflicts = [neighbor for neighbor in var.get_neighbours() if neighbor.get_value() == value]
        return not conflicts  # Ensures no neighbors have the same value

    def count_conflicts(self, var, value, assignment):
        """Counts how many conflicts a value causes (for LCV heuristic)."""
        return sum(1 for neighbor in var.get_neighbours() if neighbor.get_value() == value)



    @staticmethod
    def complexity_study():
        heuristics = ["default", "MRV", "Degree", "ConstraintPropagation"]
        puzzles = ["sudoku1.txt", "sudoku2.txt", "sudoku3.txt"]
        results = []

        for puzzle in puzzles:
            puzzle_path = os.path.join(sudoku_folder, puzzle)

            for heuristic in heuristics:
                for backtracking in [False, True]:
                    # Test without backtracking
                    game = Game(Sudoku(puzzle_path))
                    success, time_taken, iterations = Game.run_solver(game, heuristic, False)
                    results.append({
                        "Puzzle": puzzle,
                        "Heuristic": heuristic,
                        "Backtracking": False,
                        "Time": time_taken,
                        "Iterations": iterations,
                        "Solved": success
                    })

                    # Test with backtracking
                    game = Game(Sudoku(puzzle_path))
                    success, time_taken, iterations = Game.run_solver(game, heuristic, True)
                    results.append({
                        "Puzzle": puzzle,
                        "Heuristic": heuristic,
                        "Backtracking": True,
                        "Time": time_taken,
                        "Iterations": iterations,
                        "Solved": success
                    })

        # Generate report and plots
        Game.generate_report(results)

    @staticmethod
    def run_solver(game, heuristic, use_backtracking):
        game.ac3_iterations = 0  # Reset AC-3 iteration counter
        game.backtrack_iterations = 0  # Reset backtracking iteration counter
        start_time = time.time()

        try:
            solved = game.solve(heuristic, use_backtracking)
            valid = game.valid_solution() if solved else False
        except:
            solved = False
            valid = False

        return (
            valid,
            time.time() - start_time,
            game.ac3_iterations + game.backtrack_iterations  # Total iterations
        )

    @staticmethod
    def generate_report(results):
        df = pd.DataFrame(results)

        # Print summary table
        print("\n=== Summary Table ===")
        print(df.groupby(['Heuristic', 'Backtracking']).agg({
            'Solved': 'mean',
            'Time': 'mean',
            'Iterations': 'mean'
        }))

        # Plotting
        fig, ax = plt.subplots(2, 1, figsize=(12, 10))

        # Time plot
        df.groupby(['Heuristic', 'Backtracking'])['Time'].mean().unstack().plot(
            kind='bar',
            ax=ax[0],
            title='Average Solving Time by Heuristic'
        )
        ax[0].tick_params(axis='x', rotation=0)  # <-- Rotate labels horizontally


        # Iterations plot
        df.groupby(['Heuristic', 'Backtracking'])['Iterations'].mean().unstack().plot(
            kind='bar',
            ax=ax[1],
            title='Average Iterations by Heuristic'
        )
        ax[1].tick_params(axis='x', rotation=0)  # <-- Rotate labels horizontally


        plt.tight_layout()
        save_path = os.path.join(os.getcwd(), 'complexity_report.png')
        plt.savefig('complexity_report.png')
        print(f"Graph saved successfully at: {save_path}")  # Confirm save location
        plt.show()
        plt.close()


