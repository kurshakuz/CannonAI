from multiprocessing.context import DefaultContext
import random
from collections import defaultdict
import time

soldierCost = 5
townCost = 100
noPossibleMove = 0
maxDepth = 4
tableSize = 400
moveCount = [42, 42]

def findRandomMove(possibleMoves):
    return possibleMoves[random.randint(0, len(possibleMoves)-1)]


def findBestMoveMiniMax(gs, possibleMoves):
    nextMove = [None, 0]
    random.shuffle(possibleMoves)
    possibleMoves.sort()
    findBestMoveMiniMaxHelper(
        gs, possibleMoves, maxDepth, gs.redToMove, nextMove)
    print("visited node number: ", nextMove[1])
    return nextMove[0]


def findBestMoveMiniMaxHelper(gs, possibleMoves, d, redToMove, nextMove):
    nextMove[1] += 1
    if d == 0:
        return countBoardValue(gs)

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
            score = findBestMoveMiniMaxHelper(
                gs, nextMoves, d - 1, False, nextMove)
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
            nextMoves.sort()
            score = findBestMoveMiniMaxHelper(
                gs, nextMoves, d - 1, True, nextMove)
            if score < minScore:
                minScore = score
                if d == maxDepth:
                    nextMove[0] = move
            gs.undoMove()
        return minScore


def findBestMoveMiniMaxAB(gs, possibleMoves):
    nextMove = [None, 0]
    random.shuffle(possibleMoves)
    possibleMoves.sort()
    alpha = -townCost*10
    beta = townCost*10
    findBestMoveMiniMaxABHelper(
        gs, possibleMoves, maxDepth, gs.redToMove, nextMove, alpha, beta)
    print("visited node number: ", nextMove[1])
    return nextMove[0]


def findBestMoveMiniMaxABHelper(gs, possibleMoves, d, redToMove, nextMove, alpha, beta):
    nextMove[1] += 1
    if d == 0:
        return countBoardValue(gs)

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
            score = findBestMoveMiniMaxABHelper(
                gs, nextMoves, d - 1, False, nextMove, alpha, beta)
            if score > maxScore:
                maxScore = score
                if d == maxDepth:
                    nextMove[0] = move
                    print(move, score)
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
            score = findBestMoveMiniMaxABHelper(
                gs, nextMoves, d - 1, True, nextMove, alpha, beta)
            if score < minScore:
                minScore = score
                if d == maxDepth:
                    nextMove[0] = move
                    print(move, score)
            gs.undoMove()
            beta = min(beta, minScore)
            if beta <= alpha:
                break
        return minScore


def findBestMoveMiniMaxABTT(gs, possibleMoves):
    nextMove = [None, 0]
    random.shuffle(possibleMoves)
    possibleMoves.sort()
    alpha = -townCost*10
    beta = townCost*10
    transpositionTable = defaultdict(list)
    findBestMoveMiniMaxABTTHelper(
        gs, possibleMoves, maxDepth, gs.redToMove, nextMove, alpha, beta, transpositionTable)
    print("visited node number: ", nextMove[1])
    return nextMove[0]


def findBestMoveMiniMaxABTTHelper(gs, possibleMoves, d, redToMove, nextMove, alpha, beta, transpositionTable):
    nextMove[1] += 1
    alphaOrig = alpha

    if transpositionTable[gs.zobristKey % tableSize] != []:
        # print(transpositionTable[gs.zobristKey % tableSize])
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
    if redToMove:
        moveCount[0] = possibleMovesNum
    else:
        moveCount[1] = possibleMovesNum

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
            score = findBestMoveMiniMaxABTTHelper(
                gs, nextMoves, d - 1, False, nextMove, alpha, beta, transpositionTable)
            if score > maxScore:
                maxScore = score
                if d == maxDepth:
                    nextMove[0] = move
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
            score = findBestMoveMiniMaxABTTHelper(
                gs, nextMoves, d - 1, True, nextMove, alpha, beta, transpositionTable)
            if score < minScore:
                minScore = score
                if d == maxDepth:
                    nextMove[0] = move
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

# positive score better for red
def countBoardValue(gs, redToMove):
    if gs.townCapture:
        if redToMove:
            return -(townCost+1)
        else:
            return townCost+1
    if gs.noMoveLeft:
        if redToMove:
            return -townCost
        else:
            return townCost

    count = 0
    for r in range(len(gs.board)):
        for c in range(len(gs.board[r])):
            if gs.board[r][c][0] == 'r':
                count += soldierCost
            elif gs.board[r][c][0] == 'b':
                count -= soldierCost
    count += moveCount[0]
    count -= moveCount[1]
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
