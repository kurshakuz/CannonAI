soldierCost = 5
townCost = 100
tableSize = 400
cannonShootCost = 2


# positive score better for red
def countMaterial(board):
    count = 0
    for r in range(10):
        for c in range(10):
            if board[r][c][0] == 'r':
                count += soldierCost
            elif board[r][c][0] == 'b':
                count -= soldierCost

    return count


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

    count = countMaterial(gs.board)
    return count


def countBoardValueWithMobility(gs, redToMove, moveCount):
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

    count = countMaterial(gs.board)
    count += moveCount[0]
    count -= moveCount[1]
    return count


def countBoardValueWithCannonShootCount(gs, redToMove, cannonShootCount):
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

    count = countMaterial(gs.board)
    count += cannonShootCount[0]*cannonShootCost
    count -= cannonShootCount[1]*cannonShootCost
    return count
