import pygame

import AI
import CannonEngine

n = 11
dimension = n - 1
surface_size = 800
square_size = surface_size // n
surface_size = n * square_size
display_offset = 50
max_fps = 15
colors = [(244, 164, 96), (139, 69, 19), (255, 255, 255), (0, 0, 0)]
row_names = ['', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
col_names = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
images = {}


def loadImages():
    images['rS'] = pygame.transform.scale(
        pygame.image.load('./images/rS.png'), (40, 40))
    images['bS'] = pygame.transform.scale(
        pygame.image.load('./images/bS.png'), (40, 40))
    images['rT'] = pygame.transform.scale(
        pygame.image.load('./images/rT.png'), (40, 40))
    images['bT'] = pygame.transform.scale(
        pygame.image.load('./images/bT.png'), (40, 40))


def main():
    pygame.init()
    font = pygame.font.SysFont('Courier', 20)
    surface = pygame.display.set_mode((surface_size, surface_size))
    clock = pygame.time.Clock()

    gs = CannonEngine.GameState()
    possibleMoves = gs.getAllPossbileMoves()
    moveMade = False

    loadImages()
    running = True
    gameOver = False

    sqSelected = ()
    playerClicks = []

    redIsPerson = False
    blackIsPerson = False
    redIsPerson = True
    # blackIsPerson = True
    while running:
        if len(possibleMoves) == 0:
            gs.noMoveLeft = True
        personTurn = (gs.redToMove and redIsPerson) or (
            not gs.redToMove and blackIsPerson)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                break

            elif ev.type == pygame.KEYDOWN:
                key = ev.dict['key']
                if key == ord('z'):
                    if redIsPerson == True and blackIsPerson == True:
                        gs.undoMove()

                    if redIsPerson == False or blackIsPerson == False:
                        gs.undoMove()
                        gs.undoMove()

                    moveMade = True
                    gameOver = False

                if key == ord('r'):
                    gs = CannonEngine.GameState()
                    possibleMoves = gs.getAllPossbileMoves()
                    moveMade = False
                    sqSelected = ()
                    playerClicks = []
                    gameOver = False

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver and personTurn:
                    # print(gs.zobristKey)
                    if ev.button == 3:
                        sqSelected = ()
                        playerClicks = []
                        continue

                    location = pygame.mouse.get_pos()
                    col = (location[0] + 30) // square_size - 1
                    row = (location[1] + 30) // square_size - 1
                    if row == -1 or col == -1 or row == 10 or col == 10:
                        sqSelected = ()
                        playerClicks = []
                        continue

                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2:
                        move = CannonEngine.Move(
                            playerClicks[0], playerClicks[1], gs.board)
                        print(move.getCannonNotation())
                        moveFound = False
                        for possibleMove in possibleMoves:
                            if move.moveID == possibleMove.moveID:
                                gs.makeMove(possibleMove)
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                                moveFound = True
                        if not moveFound:
                            playerClicks = [sqSelected]

                # print(gs.generateZobristHash(gs.board))
                print(gs.zobristKey)

        if not personTurn and not gs.noMoveLeft:
            # AIMove = AI.findRandomMove(possibleMoves)
            # AIMove = AI.findBestMoveMiniMax(gs, possibleMoves)
            # AIMove = AI.findBestMoveMiniMaxAB(gs, possibleMoves)
            # AIMove = AI.findBestMoveMiniMaxABTT(gs, possibleMoves)
            AIMove = AI.findBestMoveMiniMaxABTTID(gs, possibleMoves)
            # AIMove = AI.findBestMoveNegaMax(gs, possibleMoves)
            # AIMove = AI.findBestMoveNegaMaxAB(gs, possibleMoves)
            # AIMove = AI.findBestMoveNegaMaxABTT(gs, possibleMoves)
            if AIMove == None:
                # print("AIMove NONE")
                if gs.redToMove:
                    print("red AI moves random")
                else:
                    print("black AI moves random")
                # print(gs.board)
                AIMove = AI.findRandomMove(possibleMoves)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            possibleMoves = gs.getAllPossbileMoves()
            moveMade = False
            # gs.zobristLog.append(gs.zobristKey)

        drawGameState(surface, gs, font, possibleMoves, sqSelected)

        if gs.townCapture:
            gameOver = True
            if gs.redToMove:
                drawText(surface, font, 'Black captured the town')
            else:
                drawText(surface, font, 'Red captured the town')
        elif gs.noMoveLeft:
            gameOver = True
            # drawText(surface, font, 'No valid moves left')
            if gs.redToMove:
                drawText(surface, font, 'No moves left for red')
            else:
                drawText(surface, font, 'No moves left for black')

        clock.tick(max_fps)
        pygame.display.flip()


def highlightMoves(surface, gs, possibleMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        square_offset = square_size//2
        if gs.board[r][c][0] == ('r' if gs.redToMove else 'b'):
            s = pygame.Surface((square_size, square_size))
            s.set_alpha(50)
            s.fill(pygame.Color('blue'))
            surface.blit(s, (c*square_size + square_offset,
                         r*square_size + square_offset))
            s.fill(pygame.Color('yellow'))

            for move in possibleMoves:
                if move.startRow == r and move.startCol == c:
                    surface.blit(s, (move.endCol*square_size + square_offset,
                                 move.endRow*square_size + square_offset))


def drawGameState(surface, gs, font, possibleMoves, sqSelected):
    drawBoard(surface, font)
    highlightMoves(surface, gs, possibleMoves, sqSelected)
    drawPieces(surface, gs.board)


def drawBoard(surface, font):
    nums_counter = 0
    alpha_counter = 0
    for row in range(n):
        c_indx = row % 2
        for col in range(n):
            if row != 0 and col != 0 and row != 10 and col != 10:
                the_square = (col*square_size, row*square_size,
                              square_size, square_size)
                surface.fill(colors[c_indx], the_square)
                c_indx = (c_indx + 1) % 2

            if col == 0 or col == 10:
                the_text_square = ((display_offset//2) + col*square_size, row *
                                   square_size - (display_offset//5), square_size, square_size)
                the_square = (col*square_size, row*square_size,
                              square_size, square_size)
                the_text = font.render(
                    row_names[nums_counter], True, colors[2])
                surface.fill(colors[3], the_square)
                surface.blit(the_text, the_text_square)
                if col == 10:
                    nums_counter += 1

            if row == 0 or row == 10:
                the_text_square = (
                    col*square_size, (display_offset//2) + row*square_size, square_size, square_size)
                the_square = (col*square_size, row*square_size,
                              square_size, square_size)
                the_text = font.render(
                    col_names[alpha_counter % 11], True, colors[2])
                surface.fill(colors[3], the_square)
                surface.blit(the_text, the_text_square)
                alpha_counter += 1


def drawPieces(surface, board):
    for row in range(dimension):
        for col in range(dimension):
            piece = board[row][col]
            if piece != '--':
                sprite_offset = -images[piece[:2]
                                        ].get_width() // 2 + square_size
                surface.blit(images[piece[:2]], (col*square_size +
                             sprite_offset, row*square_size + sprite_offset))


def drawText(surface, font, text):
    textObject = font.render(text, 0, pygame.Color('Gray'))
    textLoc = pygame.Rect(0, 0, surface_size, surface_size).move(
        surface_size/2 - textObject.get_width()/2, surface_size/2 - textObject.get_height()/2)
    surface.blit(textObject, textLoc)
    textObject = font.render(text, 0, pygame.Color('Black'))
    surface.blit(textObject, textLoc.move(2, 2))


if __name__ == '__main__':
    main()
