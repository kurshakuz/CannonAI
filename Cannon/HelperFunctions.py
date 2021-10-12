import uuid

def random64():
    return uuid.uuid4().int & (1<<64)-1

def fillZobristTable():
    zobristTable = [[[None] * 4 for _ in range(10)] for _ in range(10)]
    for row in range(10):
        for col in range(10):
            #   0     1      2     3
            # ['rS', 'bS', 'rT', 'bT']
            for sideAndPiece in range(4):
                zobristTable[row][col][sideAndPiece] = random64()
    return zobristTable

def generateZobristHash(board, zobristTable):
    zobristKey = 0
    for row in range(10):
        for col in range(10):
            if board[row][col] == '--':
                continue
            elif board[row][col] == 'rS':
                zobristKey ^= zobristTable[row][col][0]
            elif board[row][col] == 'bS':
                zobristKey ^= zobristTable[row][col][1]
            elif board[row][col] == 'rT':
                zobristKey ^= zobristTable[row][col][2]
            else:
                zobristKey ^= zobristTable[row][col][3]

    return zobristKey
