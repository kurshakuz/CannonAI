from functools import total_ordering
import uuid


class GameState():
    def __init__(self):
        self.board = [
            ['--', '--', '--', '--', '--', '--', '--', '--', 'rT', '--'],
            ['--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
            ['--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
            ['--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
            ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
            ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
            ['--', 'bT', '--', '--', '--', '--', '--', '--', '--', '--'],
        ]

        # testboard1 = [
        #     ['--', '--', '--', '--', '--', '--', '--', '--', 'rT', '--'],
        #     ['--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
        #     ['--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
        #     ['--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
        #     ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
        #     ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
        #     ['--', 'bT', '--', '--', '--', '--', '--', '--', '--', '--'],
        # ]

        # testboard2 = [
        #     ['--', '--', '--', '--', '--', '--', '--', '--', 'rT', '--'],
        #     ['--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
        #     ['--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
        #     ['--', '--', 'rS', 'rS', '--', 'rS', '--', 'rS', '--', 'rS'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
        #     ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
        #     ['bS', '--', 'bS', '--', 'bS', '--', 'bS', '--', 'bS', '--'],
        #     ['--', 'bT', '--', '--', '--', '--', '--', '--', '--', '--'],
        # ]

        # self.board = [
        #     ['--', '--', '--', '--', '--', '--', '--', '--', 'rT', '--'],
        #     ['--', 'rS', '--', '--', '--', 'rS', '--', '--', 'bS', '--'],
        #     ['--', 'rS', '--', 'rS', 'rS', '--', '--', '--', 'bS', '--'],
        #     ['--', '--', '--', '--', '--', 'bS', 'rS', '--', '--', '--'], 
        #     ['--', 'rS', '--', '--', 'rS', '--', '--', 'rS', '--', 'bS'], 
        #     ['rS', '--', '--', '--', '--', '--', '--', '--', '--', '--'], 
        #     ['bS', '--', '--', '--', 'bS', '--', 'bS', 'bS', 'bS', 'bS'], 
        #     ['bS', '--', 'bS', 'bS', '--', 'bS', '--', '--', '--', '--'], 
        #     ['--', '--', 'bS', '--', '--', '--', '--', '--', 'bS', '--'], 
        #     ['--', 'bT', '--', '--', '--', '--', '--', '--', '--', '--']]


        # self.board = [
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', 'bS', 'bS', 'bS', '--', '--', '--', '--'],
        #     ['--', '--', '--', 'bS', 'bS', 'bS', '--', '--', '--', '--'],
        #     ['--', '--', '--', 'bS', 'bS', 'bS', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        # ]

        # self.board = [
        #     ['--', '--', '--', '--', '--', '--', '--', '--', 'bS', '--'],
        #     ['--', 'bS', '--', '--', '--', '--', '--', 'bS', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', 'rS', 'rS', 'rS', '--', '--', '--', '--'],
        #     ['--', '--', '--', 'rS', 'rS', 'rS', '--', '--', '--', '--'],
        #     ['--', '--', '--', 'rS', 'rS', 'rS', '--', '--', '--', '--'],
        #     ['--', '--', 'bS', '--', '--', '--', '--', '--', '--', '--'],
        #     ['--', 'bS', '--', '--', 'bS', '--', '--', 'bS', '--', '--'],
        #     ['bS', '--', '--', '--', 'bS', '--', '--', 'bS', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        # ]

        # self.board = [
        #     ['--', '--', '--', '--', '--', '--', '--', '--', 'bS', '--'],
        #     ['--', 'bS', '--', '--', '--', '--', '--', 'bS', '--', '--'],
        #     ['--', '--', '--', '--', 'rT', '--', '--', '--', '--', '--'],
        #     ['--', '--', '--', 'rS', 'rS', 'rS', '--', '--', '--', '--'],
        #     ['--', '--', '--', 'rS', 'rS', 'rS', '--', '--', 'bS', '--'],
        #     ['--', '--', '--', 'rS', 'rS', 'rS', '--', '--', 'bS', '--'],
        #     ['--', '--', 'bS', '--', '--', '--', '--', '--', 'bS', '--'],
        #     ['--', 'bS', '--', '--', 'bS', '--', '--', '--', '--', '--'],
        #     ['bS', '--', '--', '--', 'bS', '--', '--', 'bS', '--', '--'],
        #     ['--', '--', '--', '--', '--', '--', '--', '--', '--', 'bT'],
        # ]
        self.zobristTable = [[[None] * 4 for _ in range(10)] for _ in range(10)]
        self.fillZobristTable()
        self.generateZobristHash(self.board)
        # print(self.generateZobristHash(self.board))
        # print(self.generateZobristHash(testboard1) ^ self.zobristTable[3][1][0] ^ self.zobristTable[3][2][0])
        # print(self.generateZobristHash(testboard2))
        self.pieceStrIndex = {
            'rS': 0,
            'bS': 1,
            'rT': 2,
            'bT': 3
        }

        self.redToMove = True
        self.redTownDown = False
        self.blackTownDown = False
        self.townCapture = False
        self.noMoveLeft = False
        self.moveLog = []

    def random64(self):
        return uuid.uuid4().int & (1<<64)-1

    def fillZobristTable(self):
        for row in range(10):
            for col in range(10):
                #   0     1      2     3
                # ['rS', 'bS', 'rT', 'bT']
                for sideAndPiece in range(4):
                    self.zobristTable[row][col][sideAndPiece] = self.random64()

    def generateZobristHash(self, board):
        zobristKey = 0
        for row in range(10):
            for col in range(10):
                if board[row][col] == '--':
                    continue
                elif board[row][col] == 'rS':
                    zobristKey ^= self.zobristTable[row][col][0]
                elif board[row][col] == 'bS':
                    zobristKey ^= self.zobristTable[row][col][1]
                elif board[row][col] == 'rT':
                    zobristKey ^= self.zobristTable[row][col][2]
                else:
                    zobristKey ^= self.zobristTable[row][col][3]

        self.zobristKey = zobristKey
        return zobristKey

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != '--':
            if move.isShoot:
                self.zobristKey ^= self.zobristTable[move.endRow][move.endCol][self.pieceStrIndex[self.board[move.endRow][move.endCol]]]
                self.board[move.endRow][move.endCol] = '--'
            else:
                self.zobristKey ^= self.zobristTable[move.startRow][move.startCol][self.pieceStrIndex[self.board[move.startRow][move.startCol]]]
                self.board[move.startRow][move.startCol] = '--'
                self.zobristKey ^= self.zobristTable[move.endRow][move.endCol][self.pieceStrIndex[move.pieceMoved]]
                self.board[move.endRow][move.endCol] = move.pieceMoved
            # self.zobristKey
            self.moveLog.append(move)
            self.redToMove = not self.redToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            if not move.isShoot:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = move.pieceCaptured
            else:
                self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.redToMove = not self.redToMove

            self.townCapture = False
            self.noMoveLeft = False

    def getAllPossbileMoves(self):
        moves = []
        townPresent = False
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'r' and self.redToMove) or (turn == 'b' and not self.redToMove):
                    if self.board[r][c][1] == 'T':
                        townPresent = True

        if not townPresent:
            if self.redToMove:
                self.redTownDown = True
            else:
                self.blackTownDown = True
            self.townCapture = True
            return moves

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                # generate soldier moves
                if (turn == 'r' and self.redToMove) or (turn == 'b' and not self.redToMove):
                    if self.board[r][c][1] == 'S':
                        self.getSoldierMoves(r, c, moves)
        return moves

    def getSoldierMoves(self, r, c, moves):
        if self.redToMove:
            player = 'r'
            opponent = 'b'
        else:
            player = 'b'
            opponent = 'r'

        empty = '--'
        playerSoldier = player + 'S'
        opponentSoldier = opponent + 'S'

        if self.redToMove: 
            if r < 9:
                # move forward
                if self.board[r+1][c] == empty:
                    moves.append(Move((r, c), (r+1, c), self.board, moveType=0))
                # capture forward
                if self.board[r+1][c][0] == opponent:
                    moves.append(Move((r, c), (r+1, c), self.board, moveType=3))

                if c > 0:
                    # move forward left
                    if self.board[r+1][c-1] == empty:
                        moves.append(Move((r, c), (r+1, c-1), self.board, moveType=0))
                    # capture forward left
                    if self.board[r+1][c-1][0] == opponent:
                        moves.append(Move((r, c), (r+1, c-1), self.board, moveType=3))

                if c < 9:
                    # move forward right
                    if self.board[r+1][c+1] == empty:
                        moves.append(Move((r, c), (r+1, c+1), self.board, moveType=0))
                    # capture forward right
                    if self.board[r+1][c+1][0] == opponent:
                        moves.append(Move((r, c), (r+1, c+1), self.board, moveType=3))

            if c > 0:
                # capture left
                if self.board[r][c-1][0] == opponent:
                    moves.append(Move((r, c), (r, c-1), self.board, moveType=3))
            
            if c < 9:
                # capture right
                if self.board[r][c+1][0] == opponent:
                    moves.append(Move((r, c), (r, c+1), self.board, moveType=3))

            canRetreat  = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if r+i >= 0 and c+j >= 0 and r+i <= 9 and c+j <= 9:
                        if self.board[r+i][c+j] == opponentSoldier:
                            canRetreat = True
                            # print(f'can retreat {(r,c)}')

            if canRetreat and r > 1:
                if self.board[r-2][c] == empty and self.board[r-1][c] == empty:
                    # print(f'can retreat to {(r-2, c)}')
                    moves.append(Move((r, c), (r-2, c), self.board, moveType=1))

                if c > 1 and self.board[r-2][c-2] == empty and self.board[r-1][c-1] == empty:
                    # print(f'can retreat to {(r-2, c-2)}')
                    moves.append(Move((r, c), (r-2, c-2), self.board, moveType=1))

                if c < 8 and self.board[r-2][c+2] == empty and self.board[r-1][c+1] == empty:
                    # print(f'can retreat to {(r-2, c+2)}')
                    moves.append(Move((r, c), (r-2, c+2), self.board, moveType=1))

        elif not self.redToMove:
            if  r > 0:
                # move forward
                if self.board[r-1][c] == empty:
                    moves.append(Move((r, c), (r-1, c), self.board, moveType=0))
                # capture forward
                if self.board[r-1][c][0] == opponent:
                    moves.append(Move((r, c), (r-1, c), self.board, moveType=3))

                if c > 0:
                    # move forward left
                    if self.board[r-1][c-1] == empty:
                        moves.append(Move((r, c), (r-1, c-1), self.board, moveType=0))
                    # capture forward left
                    if self.board[r-1][c-1][0] == opponent:
                        moves.append(Move((r, c), (r-1, c-1), self.board, moveType=3))

                if c < 9:
                    # move forward right
                    if self.board[r-1][c+1] == empty:
                        moves.append(Move((r, c), (r-1, c+1), self.board, moveType=0))
                    # capture forward right
                    if self.board[r-1][c+1][0] == opponent:
                        moves.append(Move((r, c), (r-1, c+1), self.board, moveType=3))

            if c > 0:
                # capture left
                if self.board[r][c-1][0] == opponent:
                    moves.append(Move((r, c), (r, c-1), self.board, moveType=3))

            if c < 9:
                # capture right
                if self.board[r][c+1][0] == opponent:
                    moves.append(Move((r, c), (r, c+1), self.board, moveType=3))

            canRetreat  = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if r+i >= 0 and c+j >= 0 and r+i <= 9 and c+j <= 9:
                        if self.board[r+i][c+j] == opponentSoldier:
                            canRetreat = True
                            # print(f'can retreat {(r,c)}')

            if canRetreat and r < 8:
                if self.board[r+2][c] == empty and self.board[r+1][c] == empty:
                    # print(f'can retreat to {(r+2, c)}')
                    moves.append(Move((r, c), (r+2, c), self.board, moveType=1))

                if c > 1 and self.board[r+2][c-2] == empty and self.board[r+1][c-1] == empty:
                    # print(f'can retreat to {(r+2, c-2)}')
                    moves.append(Move((r, c), (r+2, c-2), self.board, moveType=1))

                if c < 8 and self.board[r+2][c+2] == empty and self.board[r+1][c+1] == empty:
                    # print(f'can retreat to {(r+2, c+2)}')
                    moves.append(Move((r, c), (r+2, c+2), self.board, moveType=1))

        # cannon moves and shoots
        # horizontal
        if c > 0 and c < 9:
            if self.board[r][c-1] == playerSoldier and self.board[r][c+1] == playerSoldier:
                if c < 8 and self.board[r][c+2] == empty:
                    moves.append(Move((r, c-1), (r, c+2), self.board, moveType=2))
                    if c < 7 and self.board[r][c+3][0] == opponent:
                        moves.append(Move((r, c), (r, c+3), self.board, moveType=4))
                    elif c < 6 and self.board[r][c+3] == empty and self.board[r][c+4][0] == opponent:
                        moves.append(Move((r, c), (r, c+4), self.board, moveType=4))

                if c > 1 and self.board[r][c-2] == empty:
                    moves.append(Move((r, c+1), (r, c-2), self.board, moveType=2))
                    if c > 2 and self.board[r][c-3][0] == opponent:
                        moves.append(Move((r, c), (r, c-3), self.board, moveType=4))
                    elif c > 3 and self.board[r][c-3] == empty and self.board[r][c-4][0] == opponent:
                        moves.append(Move((r, c), (r, c-4), self.board, moveType=4))

        # vertical
        if r > 0 and r < 9:
            if self.board[r-1][c] == playerSoldier and self.board[r+1][c] == playerSoldier:
                if r < 8 and self.board[r+2][c] == empty:
                    moves.append(Move((r-1, c), (r+2, c), self.board, moveType=2))

                    if r < 7 and self.board[r+3][c][0] == opponent:
                        moves.append(Move((r, c), (r+3, c), self.board, moveType=4))

                    elif r < 6 and self.board[r+3][c] == empty and self.board[r+4][c][0] == opponent:
                        moves.append(Move((r, c), (r+4, c), self.board, moveType=4))

                if r > 1 and self.board[r-2][c] == empty:
                    moves.append(Move((r+1, c), (r-2, c), self.board, moveType=2))

                    if r > 2 and self.board[r-3][c][0] == opponent:
                        moves.append(Move((r, c), (r-3, c), self.board, moveType=4))

                    elif r > 3 and self.board[r-3][c] == empty and self.board[r-4][c][0] == opponent:
                        moves.append(Move((r, c), (r-4, c), self.board, moveType=4))

        if r > 0 and r < 9 and c > 0 and c < 9:
            # diagonal left top to right bottom
            if self.board[r-1][c-1] == playerSoldier and self.board[r+1][c+1] == playerSoldier:
                if r < 8 and c < 8 and self.board[r+2][c+2] == empty:
                    moves.append(Move((r-1, c-1), (r+2, c+2), self.board, moveType=2))

                    if r < 7 and c < 7 and self.board[r+3][c+3][0] == opponent:
                        moves.append(Move((r, c), (r+3, c+3), self.board, moveType=4))

                    elif r < 6 and c < 6 and self.board[r+3][c+3] == empty and self.board[r+4][c+4][0] == opponent:
                        moves.append(Move((r, c), (r+4, c+4), self.board, moveType=4))

                if r > 1 and c > 1 and self.board[r-2][c-2] == empty:
                    moves.append(Move((r+1, c+1), (r-2, c-2), self.board, moveType=2))

                    if r > 2 and c > 2 and self.board[r-3][c-3][0] == opponent:
                        moves.append(Move((r, c), (r-3, c-3), self.board, moveType=4))

                    elif r > 3 and c > 3 and self.board[r-3][c-3] == empty and self.board[r-4][c-4][0] == opponent:
                        moves.append(Move((r, c), (r-4, c-4), self.board, moveType=4))
            
            # diagonal right top to left bottom
            if self.board[r-1][c+1] == playerSoldier and self.board[r+1][c-1] == playerSoldier:
                if r < 8 and c > 1 and self.board[r+2][c-2] == empty:
                    moves.append(Move((r-1, c+1), (r+2, c-2), self.board, moveType=2))

                    if r < 7 and c > 2 and self.board[r+3][c-3][0] == opponent:
                        moves.append(Move((r, c), (r+3, c-3), self.board, moveType=4))

                    elif r < 6 and c > 3 and self.board[r+3][c-3] == empty and self.board[r+4][c-4][0] == opponent:
                        moves.append(Move((r, c), (r+4, c-4), self.board, moveType=4))

                if r > 1 and c < 8 and self.board[r-2][c+2] == empty:
                    moves.append(Move((r+1, c-1), (r-2, c+2), self.board, moveType=2))

                    if r > 2 and c < 7 and self.board[r-3][c+3][0] == opponent:
                        moves.append(Move((r, c), (r-3, c+3), self.board, moveType=4))

                    elif r > 3 and c < 6 and self.board[r-3][c+3] == empty and self.board[r-4][c+4][0] == opponent:
                        moves.append(Move((r, c), (r-4, c+4), self.board, moveType=4))

# movetypes = 
# 0: move
# 1: retreat
# 2: cannonmove
# 3: capture
# 4: shoot

@total_ordering
class Move():
    numsToRows = {"1": 9, "2": 8, "3": 7, "4": 6, "5": 5,
                  "6": 4, "7": 3, "8": 2, "9": 1, "10": 0}
    rowsToNums = {v: k for k,v in numsToRows.items()}
    alphasToCols = {"J": 9, "I": 8, "H": 7, "G": 6, "F": 5,
                  "E": 4, "D": 3, "C": 2, "B": 1, "A": 0}
    colsToAlphas = {v: k for k,v in alphasToCols.items()}

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
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __str__(self):
        return self.getCannonNotation()

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveType == other.moveType
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Move):
            return self.moveType < other.moveType
        else:
            return False

    def getCannonNotation(self):
        return self.getNumAlpha(self.startRow, self.startCol) + self.getNumAlpha(self.endRow, self.endCol)

    def getNumAlpha(self, r, c):
        return self.colsToAlphas[c] + self.rowsToNums[r]