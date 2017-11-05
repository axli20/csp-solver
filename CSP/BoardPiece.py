# author: Angela Li
# date: 10/17/17

class BoardPiece:

    # Constructor
    # @char the character of the piece
    # @dimensions the dimensions in tuple form (n, m), where n is rows and m is columns
    def __init__(self, char, n, m):
        self.char = char
        self.piece_n = n
        self.piece_m = m

    def getChar(self):
        return self.char

    def getN(self):
        return self.piece_n

    def getM(self):
        return self.piece_m

    def __str__(self):
        return str(self.char) + " " + str(self.piece_n) + "x" + str(self.piece_m)