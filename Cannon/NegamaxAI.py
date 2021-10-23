import random
import time
from collections import defaultdict

from Evaluation import countBoardValue

townCost = 100
maxDepth = 2
tableSize = 400

def findBestMoveNegaMax(gs, possibleMoves):
    nextMove = [None, 0]
    random.shuffle(possibleMoves)
    possibleMoves.sort()
    redToMoveMultiplier = (1 if gs.redToMove else -1)
    findBestMoveHelperNegaMax(
        gs, possibleMoves, maxDepth, redToMoveMultiplier, nextMove)
    print("visited node number: ", nextMove[1])
    return nextMove[0]


# redToMoveMultiplier 1 for red
# -1 for black
def findBestMoveHelperNegaMax(gs, possibleMoves, d, redToMoveMultiplier, nextMove):
    nextMove[1] += 1
    if d == 0:
        return redToMoveMultiplier * countBoardValue(gs)

    if len(possibleMoves) == 0:
        return -1*redToMoveMultiplier*townCost*10

    maxScore = -townCost
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossbileMoves()
        score = - \
            findBestMoveHelperNegaMax(
                gs, nextMoves, d - 1, -redToMoveMultiplier, nextMove)
        if score > maxScore:
            maxScore = score
            if d == maxDepth:
                nextMove[0] = move
        gs.undoMove()
    return maxScore


def findBestMoveNegaMaxAB(gs, possibleMoves):
    nextMove = [None, 0]
    random.shuffle(possibleMoves)
    possibleMoves.sort()
    redToMoveMultiplier = (1 if gs.redToMove else -1)
    findBestMoveHelperNegaMaxAB(
        gs, possibleMoves, maxDepth, -townCost, townCost, redToMoveMultiplier, nextMove)
    print("visited node number: ", nextMove[1])
    return nextMove[0]


def findBestMoveHelperNegaMaxAB(gs, possibleMoves, d, alpha, beta, redToMoveMultiplier, nextMove):
    nextMove[1] += 1
    if d == 0:
        return redToMoveMultiplier * countBoardValue(gs)

    if len(possibleMoves) == 0:
        return -1*redToMoveMultiplier*townCost*10

    maxScore = -townCost
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossbileMoves()
        nextMoves.sort()
        score = -findBestMoveHelperNegaMaxAB(
            gs, nextMoves, d - 1, -beta, -alpha, -redToMoveMultiplier, nextMove)
        if score > maxScore:
            maxScore = score
            if d == maxDepth:
                nextMove[0] = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def findBestMoveNegaMaxABTT(gs, possibleMoves):
    nextMove = [None, 0]
    random.shuffle(possibleMoves)
    possibleMoves.sort()
    transpositionTable = defaultdict(list)
    redToMoveMultiplier = (1 if gs.redToMove else -1)
    findBestMoveHelperNegaMaxABTT(gs, possibleMoves, maxDepth, -townCost,
                                  townCost, redToMoveMultiplier, nextMove, transpositionTable)
    print("visited node number: ", nextMove[1])
    return nextMove[0]


def findBestMoveHelperNegaMaxABTT(gs, possibleMoves, d, alpha, beta, redToMoveMultiplier, nextMove, transpositionTable):
    nextMove[1] += 1
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

    if d == 0:
        return redToMoveMultiplier * countBoardValue(gs)

    if len(possibleMoves) == 0:
        return -1*redToMoveMultiplier*townCost*10

    maxScore = -townCost
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossbileMoves()
        nextMoves.sort()
        score = -findBestMoveHelperNegaMaxABTT(
            gs, nextMoves, d - 1, -beta, -alpha, -redToMoveMultiplier, nextMove, transpositionTable)
        if score > maxScore:
            maxScore = score
            if d == maxDepth:
                nextMove[0] = move
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

    transpositionTable[gs.zobristKey % tableSize] = [d, flag, TTValue]
    return maxScore