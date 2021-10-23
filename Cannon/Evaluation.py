soldierCost = 5
townCost = 100

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
    # count += moveCount[0]
    # count -= moveCount[1]
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
