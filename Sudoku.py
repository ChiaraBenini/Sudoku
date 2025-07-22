from Field import Field


class Sudoku:

    def __init__(self, filename):
        self.board = self.read_sudoku(filename)

    def __str__(self):
        output = "╔═══════╦═══════╦═══════╗\n"
        # iterate through rows
        for i in range(9):
            if i == 3 or i == 6:
                output += "╠═══════╬═══════╬═══════╣\n"
            output += "║ "
            # iterate through columns
            for j in range(9):
                if j == 3 or j == 6:
                    output += "║ "
                output += str(self.board[i][j]) + " "
            output += "║\n"
        output += "╚═══════╩═══════╩═══════╝\n"
        return output

    @staticmethod
    def read_sudoku(filename):
        """
        Read in a sudoku file
        @param filename: Sudoku filename
        @return: A 9x9 grid of Fields where each field is initialized with all its neighbor fields
        """
        assert filename is not None and filename != "", "Invalid filename"
        # Setup 9x9 grid
        grid = [[Field for _ in range(9)] for _ in range(9)]

        try:
            with open(filename, "r") as file:
                for row, line in enumerate(file):
                    for col_index, char in enumerate(line):
                        if char == '\n':
                            continue
                        if int(char) == 0:
                            grid[row][col_index] = Field()
                        else:
                            grid[row][col_index] = Field(int(char))

        except FileNotFoundError:
            print("Error opening file: " + filename)

        Sudoku.add_neighbours(grid)
        return grid





    @staticmethod
    def add_neighbours(grid):
        """
        Adds a list of neighbors to each field
        @param grid: 9x9 list of Fields
        """
        for i in range(9):
            for j in range(9):
                #Create neighbour list
                neighbours = set()

                #Add row neighbours
                for k in range(9):
                    if k != j:
                        field = grid[i][k]
                        neighbours.add(field)


                #Add column neighbours
                for k in range(9):
                    if k != i:
                        field = grid[k][j]
                        neighbours.add(field)


                #Add 3x3 box neighbours
                box_row_start = (i//3)*3
                box_col_start = (j//3)*3
                for box_row in range(box_row_start, box_row_start + 3):
                    for box_col in range(box_col_start, box_col_start + 3):
                        if (box_row, box_col) != (i, j):  # Exclude the current field itself
                            field = grid[box_row][box_col]
                            neighbours.add(field)

                grid[i][j].set_neighbours(list(neighbours))





    def board_to_string(self):

        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board


