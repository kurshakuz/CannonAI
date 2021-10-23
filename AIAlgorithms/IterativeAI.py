import random
import time
from collections import defaultdict

from AIAlgorithms.Evaluation import (countBoardValue,
                                     countBoardValueWithCannonShootCount,
                                     countBoardValueWithMobility, tableSize,
                                     townCost)


class IterativeAI:
    def __init__(self, maxTime):
        self.nextMove = None
        self.currentMaxDepth = 1
        self.maxDepth = 10
        self.timePerMove = maxTime
        self.moveCount = [42, 42]
        self.cannonShootCount = [0, 0]

    def findBestMove(self, gs, possibleMoves):
        alpha = -townCost*1.1
        beta = townCost*1.1
        transpositionTable = defaultdict(list)
        startTime = time.time()
        while self.currentMaxDepth < self.maxDepth+1:
            if time.time() - startTime > self.timePerMove:
                break

            random.shuffle(possibleMoves)
            possibleMoves.sort()

            if self.nextMove != None:
                print("inserted")
                previousDepthSearchResult = self.nextMove
                possibleMovesUpdated = [previousDepthSearchResult]
                print("previousDepthSearchResult", previousDepthSearchResult)
                for move in possibleMoves:
                    if str(move) == str(previousDepthSearchResult):
                        print("found copy")
                        continue
                    possibleMovesUpdated.append(move)
                possibleMoves = possibleMovesUpdated.copy()

            print("currentMaxDepth ", self.currentMaxDepth)
            self.findBestMoveHelper(
                gs, possibleMoves, self.currentMaxDepth, gs.redToMove, alpha, beta, transpositionTable)

            print("NEXT MOVE ", self.nextMove)
            self.currentMaxDepth += 1

        print("execution time: ", time.time() - startTime)
        return self.nextMove

    def findBestMoveHelper(self, gs, possibleMoves, d, redToMove, alpha, beta, transpositionTable):
        alphaOrig = alpha

        if transpositionTable[gs.zobristKey % tableSize] != []:
            TTResult = transpositionTable[gs.zobristKey % tableSize]

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

        # cannon move number list to use for evaluation function
        cannonMoves = 0
        for move in possibleMoves:
            if move.moveType == 4:
                cannonMoves += 1

        if redToMove:
            self.cannonShootCount[0] = cannonMoves
        else:
            self.cannonShootCount[1] = cannonMoves

        # total possible number of move possible for each side
        # mobility heuristics
        if redToMove:
            self.moveCount[0] = possibleMovesNum
        else:
            self.moveCount[1] = possibleMovesNum

        if d == 0:
            value = countBoardValue(gs, redToMove)
            # value = countBoardValueWithMobility(gs, redToMove, self.moveCount)
            # value = countBoardValueWithCannonShootCount(gs, redToMove, self.cannonShootCount)
            return value

        if possibleMovesNum == 0:
            gs.noMoveLeft = True
            value = countBoardValue(gs, redToMove)
            # value = countBoardValueWithMobility(gs, redToMove, self.moveCount)
            # value = countBoardValueWithCannonShootCount(gs, redToMove, self.cannonShootCount)
            return value

        if redToMove:
            maxScore = -townCost
            for move in possibleMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllPossbileMoves()
                nextMoves.sort()
                score = self.findBestMoveHelper(
                    gs, nextMoves, d - 1, False, alpha, beta, transpositionTable)
                if score > maxScore:
                    maxScore = score
                    if d == self.currentMaxDepth:
                        self.nextMove = move
                        print(move, score)
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
            transpositionTable[gs.zobristKey % tableSize] = [d, flag, TTValue]

            return maxScore

        else:
            minScore = townCost
            for move in possibleMoves:
                gs.makeMove(move)
                nextMoves = gs.getAllPossbileMoves()
                nextMoves.sort()
                score = self.findBestMoveHelper(
                    gs, nextMoves, d - 1, True, alpha, beta, transpositionTable)
                if score < minScore:
                    minScore = score
                    if d == self.currentMaxDepth:
                        self.nextMove = move
                        print(move, score)
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
            transpositionTable[gs.zobristKey % tableSize] = [d, flag, TTValue]

            return minScore
