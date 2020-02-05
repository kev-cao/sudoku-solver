import csv
import itertools
import cProfile


class Board:
    def __init__(self, filename):
        self.n = 0
        self.n2 = 0

        # A mapping from a cell to the number in that cell.
        self.board = None

        # A mapping from a row/col/box # to a set of values contained in that box.
        self.vals_in_rows = None
        self.vals_in_cols = None
        self.vals_in_boxes = None

        # A set of unsolved board spaces.
        self.unsolved_cells = None

        # The set of static cells (cells that were filled at the beginning of the game).
        self.static_cells = None

        # A mapping from a cell to the valid options for that cell. Those valid options are stored in a list of size n2.
        self.legal_options = None
        self.load_sudoku(filename)

    # Loads the sudoku board from the given file.
    def load_sudoku(self, filename):
        with open(filename) as csv_file:
            self.n = - 1
            reader = csv.reader(csv_file)

            for row in reader:
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    self.n2 = int(len(row))
                    self.board = {}

                    self.vals_in_rows = [set() for i in range(self.n2)]
                    self.vals_in_cols = [set() for i in range(self.n2)]
                    self.vals_in_boxes = [set() for i in range(self.n2)]
                    self.unsolved_cells = set(itertools.product(range(self.n2), range(self.n2)))
                    self.legal_options = {}
                    self.static_cells = set()

                for col_num, item in enumerate(row):
                    val = 0 if item == '' else int(item)
                    row_num = reader.line_num - 1

                    self.board[(row_num, col_num)] = val
                    self.legal_options[(row_num, col_num)] = [False for i in range(self.n2)]

                    # If there is a value, mark it in its respective row/col/box
                    if val != 0:
                        self.vals_in_rows[row_num].add(val)
                        self.vals_in_cols[col_num].add(val)
                        self.vals_in_boxes[self.get_box_num((row_num, col_num))].add(val)
                        self.unsolved_cells.remove((row_num, col_num))
                        self.static_cells.add((row_num, col_num))

            # Fill in legal_options for every unsolved cell.
            for cell in self.unsolved_cells:
                for index in range(self.n2):
                    if self.is_legal_move(cell, index + 1):
                        self.legal_options[cell][index] = True

    # prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            # add row divider
            if r % self.n == 0 and not r == 0:
                if self.n2 > 9:
                    print("  " + "----" * self.n2)
                else:
                    print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                val = self.board[(r,c)]

                # add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                # add value placeholder
                if self.n2 > 9:
                    if val ==  0: row += "__"
                    else: row += "%2i" % val
                else:
                    if val == 0: row += "_"
                    else: row += str(val)
            print(row)

    # Returns the box number containing a given cell.
    def get_box_num(self, cell):
        return self.n * (cell[0] // self.n) + cell[1] // self.n


    # Checks if a given value can legally be put in a given cell.
    def is_legal_move(self, cell, value):
        in_bounds = cell[0] >= 0 and cell[0] < self.n2 and cell[1] >= 0 and cell[1] < self.n2
        not_in_row = value not in self.vals_in_rows[cell[0]]
        not_in_col = value not in self.vals_in_cols[cell[1]]
        not_in_box = value not in self.vals_in_boxes[self.get_box_num(cell)]

        return in_bounds and not_in_row and not_in_col and not_in_box


    # Places a given value in a given cell.
    def make_move(self, cell, value):
        self.board[cell] = value
        self.vals_in_rows[cell[0]].add(value)
        self.vals_in_cols[cell[1]].add(value)
        self.vals_in_boxes[self.get_box_num(cell)].add(value)
        self.unsolved_cells.remove(cell)
        self.update_options_fill(cell, value)


    # Cleans out a given cell and makes it empty.
    def undo_move(self, cell):
        prev_val = self.board[cell]
        self.board[cell] = 0
        self.vals_in_rows[cell[0]].remove(prev_val)
        self.vals_in_cols[cell[1]].remove(prev_val)
        self.vals_in_boxes[self.get_box_num(cell)].remove(prev_val)
        self.unsolved_cells.add(cell)
        self.update_options_clear(cell, prev_val)

    # Cleans out every cell in a list of cells.
    def undo_all_moves(self, cells):
        for cell in cells:
            self.undo_move(cell)

    # Gets all the cells in a given box number.
    def get_box(self, box_num):
        first_row = (box_num // self.n) * self.n
        first_col = (box_num % self.n) * self.n

        cells = set()
        for i in range(self.n2):
            cell = (first_row + i // self.n, first_col + i % self.n)
            cells.add(cell)

        return cells

    # Gets all the cells in a given row.
    def get_row(self, row_num):
        cells = set()

        for col_num in range(self.n2):
            cell = (row_num, col_num)
            cells.add((row_num, col_num))

        return cells

    # Gets all the cells in a given column.
    def get_col(self, col_num):
        cells = set()

        for row_num in range(self.n2):
            cell = (row_num, col_num)
            cells.add((row_num, col_num))

        return cells

    # Get the cell with the most constraints (conversely, least legal options).
    def get_most_constrained_cell(self):
        min_options = self.n2 + 1
        min_cell = None

        for cell in self.unsolved_cells:
            num_options = self.get_num_options(cell)

            if num_options < min_options:
                min_options = num_options
                min_cell = cell

        return min_cell

    # Updates the legal options for a cell after another cell was filled.
    def update_options_fill(self, cell, value):
        for r_cell in self.get_row(cell[0]):
            if r_cell in self.unsolved_cells and r_cell not in self.static_cells:
                self.legal_options[r_cell][value - 1] = False

        for c_cell in self.get_col(cell[1]):
            if c_cell in self.unsolved_cells and c_cell not in self.static_cells:
                self.legal_options[c_cell][value - 1] = False

        for b_cell in self.get_box(self.get_box_num(cell)):
            if b_cell in self.unsolved_cells and b_cell not in self.static_cells:
                self.legal_options[b_cell][value - 1] = False

    # Updates the legal options for a cell after another cell was cleared.
    def update_options_clear(self, cell, value):
        for r_cell in self.get_row(cell[0]):
            if r_cell in self.unsolved_cells and r_cell not in self.static_cells and self.is_legal_move(r_cell, value):
                self.legal_options[r_cell][value - 1] = True

        for c_cell in self.get_col(cell[1]):
            if c_cell in self.unsolved_cells and c_cell not in self.static_cells and self.is_legal_move(c_cell, value):
                self.legal_options[c_cell][value - 1] = True

        for b_cell in self.get_box(self.get_box_num(cell)):
            if b_cell in self.unsolved_cells and b_cell not in self.static_cells and self.is_legal_move(b_cell, value):
                self.legal_options[b_cell][value - 1] = True

    # Gets the count of legal options for a given cell.
    def get_num_options(self, cell):
        count = 0

        for opt in self.legal_options[cell]:
            if opt:
                count += 1

        return count

    # Gets the list of options for a given cell.
    def get_options(self, cell):
        return self.legal_options[cell]

class Solver:
    def __init__(self):
        pass

    def solveBoard(self, board):
        curr_cell = board.get_most_constrained_cell()

        if curr_cell is not None:
            options = board.get_options(curr_cell)

            for index, is_legal in enumerate(options):
                if is_legal:
                    board.make_move(curr_cell, index + 1)

                    if self.solveBoard(board):
                        return True
                    else:
                        board.undo_move(curr_cell)

            return False
        else:
            return len(board.unsolved_cells) == 0


    def deduce_rows(self, board, valid_options):
        for row in range(board.n2):
            options_count = [0 for i in range(board.n2 + 1)]
            last_cell_for_option = {}

            for col in range(board.n2):
                cell = (row, col)

                for opt in valid_options[cell]:
                    options_count[opt] += 1
                    last_cell_for_option[opt] = cell

                for option, count in enumerate(options_count):
                    if count == 1:
                        board.makeMove(last_cell_for_option[option], option)

    def deduce_columns(self, board, valid_options):
        for col in range(board.n2):
            options_count = [0 for i in range(board.n2 + 1)]
            last_cell_for_option = {}

            for row in range(board.n2):
                cell = (row, col)

                for opt in valid_options[cell]:
                    options_count[opt] += 1
                    last_cell_for_option[opt] = cell

                for option, count in enumerate(options_count):
                    if count == 1:
                        board.makeMove(last_cell_for_option[option], option)


    def deduce_box(self, board, valid_options):
        for box_num in range(board.n2):
            options_count = [0 for i in range(board.n2 + 1)]
            last_cell_for_option = {}

            for cell in board.get_box(box_num):
                for opt in valid_options[cell]:
                    options_count[opt] += 1
                    last_cell_for_option[opt] = cell

            for option, count in enumerate(options_count):
                if count == 1:
                    board.makeMove(last_cell_for_option[option], option)

    def fill_valid_options(self, board, valid_options):
        for cell in board.unsolved_cells:
            for i in range(1, board.n2 + 1):
                if board.is_legal_move(cell, i):
                   valid_options[cell].add(i)

    def update_options_on_fill(self, board, valid_options, cell, value):
        for r_cell in board.get_row(cell[0]):
            if r_cell in board.unsolved_cells:
                valid_options[r_cell].discard(value)

        for c_cell in board.get_col(cell[1]):
            if c_cell in board.unsolved_cells:
                valid_options[c_cell].discard(value)

        for b_cell in board.get_box(board.get_box_num(cell)):
            if b_cell in board.unsolved_cells:
                valid_options[b_cell].discard(value)

    def update_options_on_clear(self, board, valid_options, cell, value):
        for r_cell in board.get_row(cell[0]):
            if r_cell in board.unsolved_cells and board.is_legal_move(r_cell, value):
                valid_options[r_cell].add(value)

        for c_cell in board.get_col(cell[1]):
            if c_cell in board.unsolved_cells and board.is_legal_move(c_cell, value):
                valid_options[c_cell].add(value)

        for b_cell in board.get_box(board.get_box_num(cell)):
            if b_cell in board.unsolved_cells and board.is_legal_move(b_cell, value):
                valid_options[b_cell].add(value)

    def get_most_constrained_cell(self, board, valid_options):
        min_options = board.n2 + 1
        min_cell = None

        for cell in board.unsolved_cells:
            num_options = len(valid_options[cell])

            if num_options < min_options:
                min_options = num_options
                min_cell = cell

        return cell

def test_board(board):
    for row in range(board.n2):
        vals = [0 for i in range(board.n2)]
        for col in range(board.n2):
            cell = (row, col)
            vals[board.board[cell] - 1] += 1
            if vals[board.board[cell] - 1] > 1:
                print("Error in row")
                return cell

    for col in range(board.n2):
        vals = [0 for i in range(board.n2)]
        for row in range(board.n2):
            cell = (row, col)
            vals[board.board[cell] - 1] += 1
            if vals[board.board[cell] - 1] > 1:
                plint("Error in col")
                return cell

    for box_num in range(board.n2):
        vals = [0 for i in range(board.n2)]
        first_row = (box_num // board.n) * board.n
        first_col = (box_num % board.n) * board.n

        for i in range(board.n2):
            cell = (first_row + i // board.n, first_col + i % board.n)
            vals[board.board[cell] - 1] += 1
            if vals[board.board[cell] - 1] > 1:
                print("Error in box")
                return cell

    return None

if __name__ == "__main__":
    # change this to the input file that you'd like to test
    board = Board('tests/test-3-hard/12.csv')
    board.print()
    print("=================")
    s = Solver()
    #s.solveBoard(board)
   cProfile.run("s.solveBoard(board)", sort="tottime")
    board.print()

    cell = test_board(board)
    if cell is None:
        print("Proper board.")
    else:
        print("BAD BOARD AT %s" % str(cell))
