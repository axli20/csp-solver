# author: Angela Li
# date: 10/17/17

from BoardPiece import BoardPiece
from Constraint import Constraint
from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from backtracking_search import backtracking_search

class CircuitBoardCSP:

    # Constructor
    # @self.variables a list of Pieces
    # @self.domains a list of sets of valid bottom-left corner values for each Piece
    # @self.constraints a list of Constraints between each variable
    # @self.connections the hashtable of connections for each Piece
    def __init__(self, board_filename):
        self.board_n = 0
        self.board_m = 0
        self.variables = []
        self.domains = []
        self.constraint_pairs = []
        self.constraints = []
        self.connections = []

        f = open(board_filename)
        line_num = 0

        prev_char = ""
        prev_line = ""
        rows = 0

        for line in f:
            line = line.strip()
            if line_num == 0:
                line = line.split("x")
                self.board_n = int(line[0])
                self.board_m = int(line[1])
            else:
                cur_char = line[0]
                if(prev_char == ""):
                    prev_char = cur_char
                if(cur_char != prev_char):
                    piece = BoardPiece(prev_char, len(prev_line), rows)
                    self.variables.append(piece)
                    rows = 0

                prev_line = line
                prev_char = cur_char
                rows += 1
            line_num += 1

        f.close()

        # Take care of the last piece in the text file
        last_piece = BoardPiece(prev_char, len(prev_line), rows)
        self.variables.append(last_piece)

        self.generate_domains()
        self.generate_connections()
        self.generate_constraint_pairs()
        self.generate_all_constraints()

        self.int_csp = ConstraintSatisfactionProblem(len(self.variables), self.connections, self.domains, self.constraints)

    # Converts coordinates (x, y) into an integer representation of a location on the board
    # e.g. a board *** is represented as 345
    #              ***                   012
    def convert_coordinates(self, x, y):
        return self.board_n * y + x

    def generate_domain(self, piece):
        domain = []

        piece_n = piece.getN()
        piece_m = piece.getM()

        row_limit = self.board_n - piece_n
        col_limit = self.board_m - piece_m

        for x in range(row_limit+1):
            for y in range(col_limit+1):
                domain.append(self.convert_coordinates(x, y))

        return domain

    # Generates the legal domains of each variable
    def generate_domains(self):
        for piece in self.variables:
            self.domains.append(self.generate_domain(piece))

    def generate_connections(self):
        for piece in self.variables:
            list_copy = list(self.variables)
            list_copy.remove(piece)

            index_list = []
            for var in list_copy:
                index_list.append(self.variables.index(var))

            self.connections.append(index_list)

    def generate_constraint_pairs(self):
        variables_copy = list(self.variables)

        while len(variables_copy) > 1:
            var = variables_copy.pop()
            var_index = self.variables.index(var)

            for remaining in variables_copy:
                remaining_index = self.variables.index(remaining)
                self.constraint_pairs.append((var_index, remaining_index))

    # Generates a list of positions (integer representation) that a piece covers on a board
    def piece_coverage(self, piece, pos):
        positions = []

        piece_n = piece.getN()
        piece_m = piece.getM()

        for i in range(piece_m):
            for j in range(piece_n):
                new_pos = pos + (i * self.board_n) + j
                positions.append(new_pos)

        return positions

    def overlap(self, piece1, pos1, piece2, pos2):
        p1 = self.piece_coverage(piece1, pos1)
        p2 = self.piece_coverage(piece2, pos2)

        return bool(set(p1) & set(p2))

    # Generates the Constraint object for the specified constraint pair
    def generate_constraint(self, constraint_pair):
        piece1 = self.variables[constraint_pair[0]]
        piece2 = self.variables[constraint_pair[1]]

        domain1 = self.domains[constraint_pair[0]]
        domain2 = self.domains[constraint_pair[1]]

        legal_values = []

        for pos1 in domain1:
            for pos2 in domain2:
                if pos1 != pos2:
                    if not self.overlap(piece1, pos1, piece2, pos2):
                        legal_values.append((pos1, pos2))

        return Constraint(constraint_pair, legal_values)

    # Generates all the constraints for all constraint pairs
    def generate_all_constraints(self):
        for pair in self.constraint_pairs:
            self.constraints.append(self.generate_constraint(pair))

    # Converts an integer position to coordinates
    def convert_to_coordinates(self, int_rep):
        row = int_rep % self.board_n
        col = (int_rep - row) / self.board_n

        return (col, row)

    def solution(self):
        result = backtracking_search(self.int_csp)

        board = [["."]*self.board_n for _ in range(self.board_m)]

        for piece in self.variables:
            cover = self.piece_coverage(piece, result[self.variables.index(piece)])
            for pos in cover:
                coordinates = self.convert_to_coordinates(pos)
                board[int(coordinates[0])][int(coordinates[1])] = piece.getChar()

        str = "Solution Board: \n"

        for r in range(len(board)-1, -1, -1):
            for c in range(len(board[0])):
                str += board[r][c]

            str += "\n"

        print(str)


if __name__ == "__main__":

    cb = CircuitBoardCSP("board.txt")
    cb.solution()