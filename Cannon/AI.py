from multiprocessing.context import DefaultContext
import random
from collections import defaultdict
import time

soldierCost = 1
townCost = 100
noPossibleMove = 0
maxDepth = 2

def findRandomMove(possibleMoves):
    return possibleMoves[random.randint(0, len(possibleMoves)-1)]

def findBestMoveMiniMax(gs, possibleMoves):
    nextMove = [None]
    findBestMoveHelperMiniMax(gs, possibleMoves, maxDepth, gs.redToMove, nextMove)
    # time.sleep(2)
    return nextMove[0]

def findBestMoveHelperMiniMax(gs, possibleMoves, d, redToMove, nextMove):
    if  d == 0:
        return countBoardValue(gs)

    if redToMove:
        maxScore = -townCost
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossbileMoves()
            score = findBestMoveHelperMiniMax(gs, nextMoves, d - 1, False, nextMove)
            if score > maxScore:
                maxScore = score
                if d == maxDepth:
                    nextMove[0] = move
            gs.undoMove()
        return maxScore
    else:
        minScore = townCost
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossbileMoves()
            score = findBestMoveHelperMiniMax(gs, nextMoves, d - 1, True, nextMove)
            if score < minScore:
                minScore = score
                if d == maxDepth:
                    nextMove[0] = move
            gs.undoMove()
        return minScore

# --------------------
def findBestMoveMiniMaxAB(gs, possibleMoves):
    nextMove = [None]
    possibleMoves.sort()
    alpha = -townCost*10
    beta = townCost*10
    findBestMoveHelperMiniMaxAB(gs, possibleMoves, maxDepth, gs.redToMove, nextMove, alpha, beta)
    time.sleep(2)
    return nextMove[0]

def findBestMoveHelperMiniMaxAB(gs, possibleMoves, d, redToMove, nextMove, alpha, beta):
    if  d == 0:
        return countBoardValue(gs)

    if len(possibleMoves) == 0:
        return countBoardValue(gs)

    if redToMove:
        maxScore = -townCost*10
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossbileMoves()
            score = findBestMoveHelperMiniMaxAB(gs, nextMoves, d - 1, False, nextMove, alpha, beta)
            if score > maxScore:
                maxScore = score
                if d == maxDepth:
                    print(move, maxScore)
                    nextMove[0] = move
            gs.undoMove()
            alpha = max(alpha, maxScore)
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = townCost*10
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossbileMoves()
            score = findBestMoveHelperMiniMaxAB(gs, nextMoves, d - 1, True, nextMove, alpha, beta)
            if score < minScore:
                minScore = score
                if d == maxDepth:
                    print(move, minScore)
                    nextMove[0] = move
            gs.undoMove()
            beta = min(beta, minScore)
            if beta <= alpha:
                break

        return minScore

# --------------------

def findBestMoveNegaMax(gs, possibleMoves):
    nextMove = [None]
    # random.shuffle(possibleMoves)
    possibleMoves.sort()
    redToMoveMultiplier = (1 if gs.redToMove else -1)
    findBestMoveHelperNegaMax(gs, possibleMoves, maxDepth, redToMoveMultiplier, nextMove)
    return nextMove[0]

# redToMoveMultiplier 1 for red
# -1 for black
def findBestMoveHelperNegaMax(gs, possibleMoves, d, redToMoveMultiplier, nextMove):
    if  d == 0:
        return redToMoveMultiplier * countBoardValue(gs)

    maxScore = -townCost
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossbileMoves()
        score = -findBestMoveHelperNegaMax(gs, nextMoves, d - 1, -redToMoveMultiplier, nextMove)
        if score > maxScore:
            print(score)
            maxScore = score
            if d == maxDepth:
                nextMove[0] = move
        gs.undoMove()
    return maxScore

# def findBestMoveNegaMaxAB(gs, possibleMoves):
#     nextMove = [None]
#     random.shuffle(possibleMoves)
#     possibleMoves.sort()
#     redToMoveMultiplier = (1 if gs.redToMove else -1)
#     findBestMoveHelperNegaMaxAB(gs, possibleMoves, maxDepth, -townCost, townCost, redToMoveMultiplier, nextMove)
#     return nextMove[0]

# def findBestMoveHelperNegaMaxAB(gs, possibleMoves, d, alpha, beta, redToMoveMultiplier, nextMove):
#     if  d == 0:
#         return redToMoveMultiplier * countBoardValue(gs)

#     maxScore = -townCost
#     for move in possibleMoves:
#         gs.makeMove(move)
#         nextMoves = gs.getAllPossbileMoves()
#         score = -findBestMoveHelperNegaMaxAB(gs, nextMoves, d - 1, -beta, -alpha, -redToMoveMultiplier, nextMove)
#         if score > maxScore:
#             maxScore = score
#             if d == maxDepth:
#                 nextMove[0] = move
#                 print(move, score)
#         gs.undoMove()
#         # alpha = max(maxScore, alpha)
#         if maxScore > alpha:
#             alpha = maxScore
#         if alpha >= beta:
#             break
#     return maxScore

def findBestMoveNegaMaxAB(gs):
    nextMove = [None]
    redToMoveMultiplier = (1 if gs.redToMove else -1)
    findBestMoveHelperNegaMaxAB(gs, maxDepth, -townCost, townCost, redToMoveMultiplier, nextMove)
    time.sleep(2)
    return nextMove[0]

def findBestMoveHelperNegaMaxAB(gs, d, alpha, beta, redToMoveMultiplier, nextMove):
    if  d == 0:
        return redToMoveMultiplier * countBoardValue(gs)

    possibleMoves = gs.getAllPossbileMoves()
    possibleMoves.sort()
    if len(possibleMoves) == 0:
        return redToMoveMultiplier * (countBoardValue(gs) + maxDepth - d)
    maxScore = -townCost
    for move in possibleMoves:
        gs.makeMove(move)
        score = -findBestMoveHelperNegaMaxAB(gs, d - 1, -beta, -alpha, -redToMoveMultiplier, nextMove)
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
    nextMove = [None]
    random.shuffle(possibleMoves)
    possibleMoves.sort()
    transpositionTable = defaultdict(list)
    redToMoveMultiplier = (1 if gs.redToMove else -1)
    findBestMoveHelperNegaMaxABTT(gs, possibleMoves, maxDepth, -townCost, townCost, redToMoveMultiplier, nextMove, transpositionTable)
    return nextMove[0]

def findBestMoveHelperNegaMaxABTT(gs, possibleMoves, d, alpha, beta, redToMoveMultiplier, nextMove, transpositionTable):
    alphaOrig = alpha

    tableSize = 400
    if transpositionTable[gs.zobristKey % tableSize] != []:
        # print(transpositionTable[gs.zobristKey % tableSize])
        TTResult = transpositionTable[gs.zobristKey % tableSize]
        if TTResult is not None and TTResult[0] >= d and TTResult[4] != None:
            if TTResult[4] == 'EXACT':
                return TTResult[1]
            elif TTResult[4] == 'LB':
                alpha = max(alpha, TTResult[1])
            elif TTResult[4] == 'UB':
                beta = min(beta, TTResult[1])

        if alpha >= beta:
            return TTResult[1]

    if  d == 0:
        return redToMoveMultiplier * countBoardValue(gs)

    maxScore = -townCost
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossbileMoves()
        # nextMoves.sort()
        score = -findBestMoveHelperNegaMaxABTT(gs, nextMoves, d - 1, -beta, -alpha, -redToMoveMultiplier, nextMove, transpositionTable)
        if score > maxScore:
            maxScore = score
            if d == maxDepth:
                nextMove[0] = move
                # print(move, score)
        gs.undoMove()
        # alpha = max(maxScore, alpha)
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    
    flag = None
    if maxScore <= alphaOrig:
        flag = 'UB'
    elif maxScore >= beta:
        flag = 'LB'
    if maxScore >= beta: 
        flag = 'EXACT'
    transpositionTable[gs.zobristKey % tableSize] = [d, maxScore, redToMoveMultiplier, nextMove[0], flag]
    return maxScore

# positive score better for red
def countBoardValue(gs):
    # if gs.townCapture:
    #     if not gs.redToMove:
    #         return -townCost
    #     else:
    #         return townCost
    # elif gs.noMoveLeft:
    #     if not gs.redToMove:
    #         return -townCost
    #     else:
    #         return townCost
        # return noPossibleMove

    count = 0
    for r in range(10):
        for c in range(10):
            if gs.board[r][c] == 'rS':
                count += soldierCost
            if gs.board[r][c] == 'rT':
                count += townCost
            if gs.board[r][c] == 'bS':
                count -= soldierCost
            if gs.board[r][c] == 'bT':
                count -= townCost

    return count

def countMaterial(board):
    count = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 'rS':
                count += soldierCost
            elif board[r][c] == 'bS':
                count -= soldierCost

    return count
