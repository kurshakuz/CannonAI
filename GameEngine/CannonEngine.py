from GameEngine.Move import Move
from GameEngine.ZobristHelperFunctions import fillZobristTable, generateZobristHash


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

        self.zobristTable = fillZobristTable()
        self.zobristKey = generateZobristHash(self.board, self.zobristTable)
        self.pieceStrIndex = {
            'rS': 0,
            'bS': 1,
            'rT': 2,
            'bT': 3
        }
        self.zobristLog = []

        self.redToMove = False
        self.redTownDown = False
        self.blackTownDown = False
        self.townCapture = False
        self.noMoveLeft = False
        self.moveLog = []

    def makeMove(self, move):
        if self.board[move.startRow][move.startCol] != '--':
            if not move.isShoot:
                if self.board[move.endRow][move.endCol] != '--':
                    self.zobristKey ^= self.zobristTable[move.endRow][move.endCol][self.pieceStrIndex[move.pieceCaptured]]
                self.zobristKey ^= self.zobristTable[move.startRow][move.startCol][self.pieceStrIndex[move.pieceMoved]]
                self.board[move.startRow][move.startCol] = '--'
                self.zobristKey ^= self.zobristTable[move.endRow][move.endCol][self.pieceStrIndex[move.pieceMoved]]
                self.board[move.endRow][move.endCol] = move.pieceMoved
            else:
                self.zobristKey ^= self.zobristTable[move.endRow][move.endCol][self.pieceStrIndex[move.pieceCaptured]]
                self.board[move.endRow][move.endCol] = '--'
            self.moveLog.append(move)
            self.redToMove = not self.redToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            if not move.isShoot:
                if move.pieceCaptured != '--':
                    self.zobristKey ^= self.zobristTable[move.endRow][move.endCol][self.pieceStrIndex[move.pieceCaptured]]
                self.zobristKey ^= self.zobristTable[move.startRow][move.startCol][self.pieceStrIndex[move.pieceMoved]]
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.zobristKey ^= self.zobristTable[move.endRow][move.endCol][self.pieceStrIndex[move.pieceMoved]]
                self.board[move.endRow][move.endCol] = move.pieceCaptured
            else:
                self.zobristKey ^= self.zobristTable[move.endRow][move.endCol][self.pieceStrIndex[move.pieceCaptured]]
                self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.redToMove = not self.redToMove

            if self.townCapture and self.checkIfTownPresent():
                self.townCapture = False
            self.noMoveLeft = False

    def checkIfTownPresent(self):
        townPresent = False
        for r in range(10):
            for c in range(10):
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

        return townPresent

    def getAllPossbileMoves(self):
        moves = []
        
        if self.checkIfTownPresent() == False:
            return moves

        for r in range(10):
            for c in range(10):
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

        if self.redToMove:
            # check retreat moves
            canRetreat  = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if r+i >= 0 and c+j >= 0 and r+i <= 9 and c+j <= 9:
                        if self.board[r+i][c+j] == opponentSoldier:
                            canRetreat = True

            if canRetreat and r > 1:
                if self.board[r-2][c] == empty and self.board[r-1][c] == empty:
                    moves.append(Move((r, c), (r-2, c), self.board, moveType=1))

                if c > 1 and self.board[r-2][c-2] == empty and self.board[r-1][c-1] == empty:
                    moves.append(Move((r, c), (r-2, c-2), self.board, moveType=1))

                if c < 8 and self.board[r-2][c+2] == empty and self.board[r-1][c+1] == empty:
                    moves.append(Move((r, c), (r-2, c+2), self.board, moveType=1))

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

        elif not self.redToMove:
            # check retreat moves
            canRetreat  = False
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if r+i >= 0 and c+j >= 0 and r+i <= 9 and c+j <= 9:
                        if self.board[r+i][c+j] == opponentSoldier:
                            canRetreat = True

            if canRetreat and r < 8:
                if self.board[r+2][c] == empty and self.board[r+1][c] == empty:
                    moves.append(Move((r, c), (r+2, c), self.board, moveType=1))

                if c > 1 and self.board[r+2][c-2] == empty and self.board[r+1][c-1] == empty:
                    moves.append(Move((r, c), (r+2, c-2), self.board, moveType=1))

                if c < 8 and self.board[r+2][c+2] == empty and self.board[r+1][c+1] == empty:
                    moves.append(Move((r, c), (r+2, c+2), self.board, moveType=1))

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
