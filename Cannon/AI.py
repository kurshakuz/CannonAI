from multiprocessing.context import DefaultContext
import random
from collections import defaultdict

soldierCost = 1
townCost = 100
noPossibleMove = 0
maxDepth = 4

def findRandomMove(possibleMoves):
    return possibleMoves[random.randint(0, len(possibleMoves)-1)]

def findBestMove(gs, possibleMoves):
    nextMove = [None]
    # random.shuffle(possibleMoves)
    possibleMoves.sort()
    findBestMoveHelper(gs, possibleMoves, maxDepth, gs.redToMove, nextMove)
    return nextMove[0]

def findBestMoveHelper(gs, possibleMoves, d, redToMove, nextMove):
    if  d == 0:
        return countBoardValue(gs)

    if redToMove:
        maxScore = -townCost
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossbileMoves()
            score = findBestMoveHelper(gs, nextMoves, d - 1, False, nextMove)
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
            score = findBestMoveHelper(gs, nextMoves, d - 1, True, nextMove)
            if score < minScore:
                minScore = score
                if d == maxDepth:
                    nextMove[0] = move
            gs.undoMove()
        return minScore

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

def findBestMoveNegaMaxAB(gs, possibleMoves):
    nextMove = [None]
    random.shuffle(possibleMoves)
    possibleMoves.sort()
    redToMoveMultiplier = (1 if gs.redToMove else -1)
    findBestMoveHelperNegaMaxAB(gs, possibleMoves, maxDepth, -townCost, townCost, redToMoveMultiplier, nextMove)
    return nextMove[0]

def findBestMoveHelperNegaMaxAB(gs, possibleMoves, d, alpha, beta, redToMoveMultiplier, nextMove):
    if  d == 0:
        return redToMoveMultiplier * countBoardValue(gs)

    maxScore = -townCost
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossbileMoves()
        score = -findBestMoveHelperNegaMaxAB(gs, nextMoves, d - 1, -beta, -alpha, -redToMoveMultiplier, nextMove)
        if score > maxScore:
            maxScore = score
            if d == maxDepth:
                nextMove[0] = move
                print(move, score)
        gs.undoMove()
        # alpha = max(maxScore, alpha)
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
    tableSize = 400
    if transpositionTable[gs.zobristKey % tableSize] != []:
        # print(transpositionTable[gs.zobristKey % tableSize])
        TTResult = transpositionTable[gs.zobristKey % tableSize]
        # lowerbound
        if TTResult[4] is not None and TTResult[4] >= beta:
            return TTResult[4]
        # upperbound
        if TTResult[5] is not None and TTResult[5] >= beta:
            return TTResult[5]

        if TTResult[4] is not None:
            alpha = max(alpha, TTResult[4])
        if TTResult[5] is not None:
            beta = min(beta, TTResult[5])

    if  d == 0:
        return redToMoveMultiplier * countBoardValue(gs)

    maxScore = -townCost
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossbileMoves()
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

    lowerBound = upperBound = None
    if maxScore <= alpha:
        upperbound = maxScore; 
    if maxScore >  alpha and maxScore < beta:
        lowerbound = maxScore
        upperbound = maxScore
    if maxScore >= beta: 
        lowerbound = maxScore
    transpositionTable[gs.zobristKey % tableSize] = [d, maxScore, redToMoveMultiplier, nextMove[0], lowerBound, upperBound]
    return maxScore

# positive score better for red
def countBoardValue(gs):
    if gs.townCapture:
        if not gs.redToMove:
            return -townCost
        else:
            return townCost
    elif gs.noMoveLeft:
        if not gs.redToMove:
            return -townCost
        else:
            return townCost
        # return noPossibleMove

    count = 0
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            if gs.board[r][c][0] == 'r':
                count += soldierCost
            elif gs.board[r][c][0] == 'b':
                count -= soldierCost

    return count

def countMaterial(board):
    count = 0
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c][0] == 'r':
                count += soldierCost
            elif board[r][c][0] == 'b':
                count -= soldierCost

    return count
