import random
import time
from collections import defaultdict

from AIAlgorithms.Evaluation import countBoardValue, tableSize, townCost


class Minimax:
    def __init__(self, maxDepth=2):
        self.nextMove = None
        self.nodeVisitCount = 0
        self.maxDepth = maxDepth

    def findBestMove(self, gs, possibleMoves):
        random.shuffle(possibleMoves)
        possibleMoves.sort()
        startTime = time.time()
        self.findBestMoveHelper(
            gs, possibleMoves, self.maxDepth, gs.redToMove)
        print("visited node number: ", self.nodeVisitCount)
        print("execution time: ", time.time() - startTime)
        return self.nextMove

    def findBestMoveHelper(self, gs, possibleMoves, d, redToMove):
        self.nodeVisitCount += 1
        if d == 0:
            return countBoardValue(gs, redToMove)

        if len(possibleMoves) == 0:
            if redToMove:
                return -townCost*10
            else:
                return townCost*10

        if redToMove:
            maxScore = -townCost
            for move in possibleMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllPossbileMoves()
                nextMoves.sort()
                score = self.findBestMoveHelper(
                    gs, nextMoves, d - 1, False)
                if score > maxScore:
                    maxScore = score
                    if d == self.maxDepth:
                        self.nextMove = move
                gs.undoMove()
            return maxScore
        else:
            minScore = townCost
            for move in possibleMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllPossbileMoves()
                nextMoves.sort()
                score = self.findBestMoveHelper(
                    gs, nextMoves, d - 1, True)
                if score < minScore:
                    minScore = score
                    if d == self.maxDepth:
                        self.nextMove = move
                gs.undoMove()
            return minScore

class MinimaxAB:
    def __init__(self, maxDepth=2):
        self.nextMove = None
        self.nodeVisitCount = 0
        self.maxDepth = maxDepth

    def findBestMove(self, gs, possibleMoves):
        random.shuffle(possibleMoves)
        possibleMoves.sort()
        alpha = -townCost*10
        beta = townCost*10
        startTime = time.time()
        self.findBestMoveHelper(
            gs, possibleMoves, self.maxDepth, gs.redToMove, alpha, beta)
        print("visited node number: ", self.nodeVisitCount)
        print("execution time: ", time.time() - startTime)
        return self.nextMove

    def findBestMoveHelper(self, gs, possibleMoves, d, redToMove, alpha, beta):
        self.nodeVisitCount += 1
        if d == 0:
            return countBoardValue(gs, redToMove)

        if len(possibleMoves) == 0:
            if redToMove:
                return -townCost*10
            else:
                return townCost*10

        if redToMove:
            maxScore = -townCost
            for move in possibleMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllPossbileMoves()
                nextMoves.sort()
                score = self.findBestMoveHelper(
                    gs, nextMoves, d - 1, False, alpha, beta)
                if score > maxScore:
                    maxScore = score
                    if d == self.maxDepth:
                        self.nextMove = move
                gs.undoMove()
                alpha = max(alpha, maxScore)
                if beta <= alpha:
                    break

            return maxScore
        else:
            minScore = townCost
            for move in possibleMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllPossbileMoves()
                nextMoves.sort()
                score = self.findBestMoveHelper(
                    gs, nextMoves, d - 1, True, alpha, beta)
                if score < minScore:
                    minScore = score
                    if d == self.maxDepth:
                        self.nextMove = move
                gs.undoMove()
                beta = min(beta, minScore)
                if beta <= alpha:
                    break
            return minScore


class MinimaxABTT:
    def __init__(self, maxDepth=2):
        self.nextMove = None
        self.nodeVisitCount = 0
        self.maxDepth = maxDepth
        self.transpositionTable = defaultdict(list)

    def findBestMove(self, gs, possibleMoves):
        random.shuffle(possibleMoves)
        possibleMoves.sort()
        alpha = -townCost*10
        beta = townCost*10
        startTime = time.time()
        self.findBestMoveHelper(
            gs, possibleMoves, self.maxDepth, gs.redToMove, alpha, beta)
        print("visited node number: ", self.nodeVisitCount)
        print("execution time: ", time.time() - startTime)
        return self.nextMove

    def findBestMoveHelper(self, gs, possibleMoves, d, redToMove, alpha, beta):
        self.nodeVisitCount += 1
        alphaOrig = alpha

        if self.transpositionTable[gs.zobristKey % tableSize] != []:
            TTResult = self.transpositionTable[gs.zobristKey % tableSize]

            # exact, lowerbound, upperbound
            if TTResult[0] >= d:
                if TTResult[1] == 'E':
                    return TTResult[2]
                elif TTResult[1] == 'L':
                    alpha = max(alpha, TTResult[2])
                elif TTResult[1] == 'U':
                    beta = min(beta, TTResult[2])

                if alpha >= beta:
                    return TTResult[2]

        possibleMovesNum = len(possibleMoves)

        if d == 0:
            return countBoardValue(gs, redToMove)

        if possibleMovesNum == 0:
            # noMoveLeft = True
            gs.noMoveLeft = True
            return countBoardValue(gs, redToMove)

        if redToMove:
            maxScore = -townCost
            for move in possibleMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllPossbileMoves()
                nextMoves.sort()
                score = self.findBestMoveHelper(
                    gs, nextMoves, d - 1, False, alpha, beta)
                if score > maxScore:
                    maxScore = score
                    if d == self.maxDepth:
                        self.nextMove = move
                gs.undoMove()
                alpha = max(alpha, maxScore)
                if beta <= alpha:
                    break

            flag = None
            TTValue = maxScore
            if maxScore <= alphaOrig:
                flag = 'U'
            elif maxScore >= beta:
                flag = 'L'
            else:
                flag = 'E'
            self.transpositionTable[gs.zobristKey % tableSize] = [d, flag, TTValue]

            return maxScore

        else:
            minScore = townCost
            for move in possibleMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllPossbileMoves()
                nextMoves.sort()
                score = self.findBestMoveHelper(
                    gs, nextMoves, d - 1, True, alpha, beta)
                if score < minScore:
                    minScore = score
                    if d == self.maxDepth:
                        self.nextMove = move
                gs.undoMove()
                beta = min(beta, minScore)
                if beta <= alpha:
                    break

            flag = None
            TTValue = minScore
            if minScore <= alphaOrig:
                flag = 'U'
            elif minScore >= beta:
                flag = 'L'
            else:
                flag = 'E'
            self.transpositionTable[gs.zobristKey % tableSize] = [d, flag, TTValue]

            return minScore
