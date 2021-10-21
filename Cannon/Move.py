from functools import total_ordering

numsToRows = {"1": 9, "2": 8, "3": 7, "4": 6, "5": 5,
              "6": 4, "7": 3, "8": 2, "9": 1, "10": 0}
rowsToNums = {v: k for k, v in numsToRows.items()}
alphasToCols = {"J": 9, "I": 8, "H": 7, "G": 6, "F": 5,
                "E": 4, "D": 3, "C": 2, "B": 1, "A": 0}
colsToAlphas = {v: k for k, v in alphasToCols.items()}


@total_ordering
class Move():
    def __init__(self, startSq, endSq, board, moveType=None):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isShoot = True if moveType == 4 else False
        self.moveType = moveType
        if self.isShoot:
            self.pieceMoved = None
        else:
            self.pieceMoved = board[self.startRow][self.startCol]
        self.moveID = self.startRow * 1000 + self.startCol * \
            100 + self.endRow * 10 + self.endCol

    def __str__(self):
        return self.getCannonNotation()

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveType == other.moveType and self.moveID == other.moveID
        else:
            return False

    # movetypes =
    # 0: move
    # 1: retreat
    # 2: cannonmove
    # 3: capture
    # 4: shoot

    # The strongest moves are highest numbers
    # sort to give strongest first
    def __lt__(self, other):
        if isinstance(other, Move):
            return self.moveType > other.moveType
        else:
            return False

    def getCannonNotation(self):
        return self.getNumAlpha(self.startRow, self.startCol) + self.getNumAlpha(self.endRow, self.endCol)

    def getNumAlpha(self, r, c):
        return colsToAlphas[c] + rowsToNums[r]
