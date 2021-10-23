import random
from collections import defaultdict

from AIAlgorithms.Evaluation import countBoardValue, townCost, tableSize


class Negamax:
    def __init__(self, maxDepth=2):
        self.nextMove = None
        self.nodeVisitCount = 0
        self.maxDepth = maxDepth

    def findBestMove(self, gs, possibleMoves):
        random.shuffle(possibleMoves)
        possibleMoves.sort()
        redToMoveMultiplier = (1 if gs.redToMove else -1)
        self.findBestMoveHelper(
            gs, possibleMoves, self.maxDepth, redToMoveMultiplier)
        print("visited node number: ", self.nodeVisitCount)
        return self.nextMove

    # redToMoveMultiplier 1 for red
    # -1 for black
    def findBestMoveHelper(self, gs, possibleMoves, d, redToMoveMultiplier):
        self.nodeVisitCount += 1
        if d == 0:
            return redToMoveMultiplier * countBoardValue(gs, (True if 1 else False))

        if len(possibleMoves) == 0:
            return countBoardValue(gs, (True if 1 else False))

        maxScore = -townCost
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossbileMoves()
            score = -self.findBestMoveHelper(
                gs, nextMoves, d - 1, -redToMoveMultiplier)
            if score > maxScore:
                maxScore = score
                if d == self.maxDepth:
                    self.nextMove = move
            gs.undoMove()
        return maxScore


class NegamaxAB:
    def __init__(self, maxDepth=2):
        self.nextMove = None
        self.nodeVisitCount = 0
        self.maxDepth = maxDepth

    def findBestMove(self, gs, possibleMoves):
        random.shuffle(possibleMoves)
        possibleMoves.sort()
        redToMoveMultiplier = (1 if gs.redToMove else -1)
        self.findBestMoveHelper(
            gs, possibleMoves, self.maxDepth, -townCost, townCost, redToMoveMultiplier)
        print("visited node number: ", self.nodeVisitCount)
        return self.nextMove

    def findBestMoveHelper(self, gs, possibleMoves, d, alpha, beta, redToMoveMultiplier):
        self.nodeVisitCount += 1
        if d == 0:
            return redToMoveMultiplier * countBoardValue(gs, (True if 1 else False))

        if len(possibleMoves) == 0:
            return countBoardValue(gs, (True if 1 else False))

        maxScore = -townCost
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossbileMoves()
            nextMoves.sort()
            score = -self.findBestMoveHelper(
                gs, nextMoves, d - 1, -beta, -alpha, -redToMoveMultiplier)
            if score > maxScore:
                maxScore = score
                if d == self.maxDepth:
                    self.nextMove = move
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
        return maxScore


class NegamaxABTT:
    def __init__(self, maxDepth=2):
        self.nextMove = None
        self.nodeVisitCount = 0
        self.maxDepth = maxDepth
        self.transpositionTable = defaultdict(list)

    def findBestMove(self, gs, possibleMoves):
        random.shuffle(possibleMoves)
        possibleMoves.sort()
        redToMoveMultiplier = (1 if gs.redToMove else -1)
        self.findBestMoveHelper(gs, possibleMoves, self.maxDepth, -townCost,
                                townCost, redToMoveMultiplier)
        print("visited node number: ", self.nodeVisitCount)
        return self.nextMove

    def findBestMoveHelper(self, gs, possibleMoves, d, alpha, beta, redToMoveMultiplier):
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

        if d == 0:
            return redToMoveMultiplier * countBoardValue(gs, (True if 1 else False))

        if len(possibleMoves) == 0:
            return countBoardValue(gs, (True if 1 else False))

        maxScore = -townCost
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossbileMoves()
            nextMoves.sort()
            score = -self.findBestMoveHelper(
                gs, nextMoves, d - 1, -beta, -alpha, -redToMoveMultiplier)
            if score > maxScore:
                maxScore = score
                if d == self.maxDepth:
                    self.nextMove = move
            gs.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
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
