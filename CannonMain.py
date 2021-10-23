import pygame

from AIEngines.IterativeAI import IterativeAI
from AIEngines.MinimaxAI import (findBestMoveMiniMax, findBestMoveMiniMaxAB,
                                 findBestMoveMiniMaxABTT)
from AIEngines.NegamaxAI import (findBestMoveNegaMax, findBestMoveNegaMaxAB,
                                 findBestMoveNegaMaxABTT)
from AIEngines.RandomAI import findRandomMove
from Engine import CannonEngine
from GUI.GUIHelperFunctions import drawGameState, drawText, loadImages
from GUI.GUIVariables import max_fps, square_size, surface_size


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
    # redIsPerson = True

    # blackIsPerson = False
    blackIsPerson = True
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

        if not personTurn and not gs.noMoveLeft:
            # AIMove = AI.findRandomMove(possibleMoves)
            # AIMove = AI.findBestMoveMiniMax(gs, possibleMoves)
            # AIMove = AI.findBestMoveMiniMaxAB(gs, possibleMoves)
            # AIMove = AI.findBestMoveMiniMaxABTT(gs, possibleMoves)
            # AIMove = AI.findBestMoveMiniMaxABTTID(gs, possibleMoves)
            # AIMove = AI.findBestMoveNegaMax(gs, possibleMoves)
            # AIMove = AI.findBestMoveNegaMaxAB(gs, possibleMoves)
            # AIMove = AI.findBestMoveNegaMaxABTT(gs, possibleMoves)
            AIEngine = IterativeAI()
            AIMove = AIEngine.findBestMove(gs, possibleMoves)

            if AIMove == None:
                # print("AIMove NONE")
                if gs.redToMove:
                    print("red AI moves random")
                else:
                    print("black AI moves random")
                # print(gs.board)
                AIMove = findRandomMove(possibleMoves)
            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
            possibleMoves = gs.getAllPossbileMoves()
            moveMade = False

        drawGameState(surface, gs, font, possibleMoves, sqSelected)

        if gs.townCapture:
            gameOver = True
            if gs.redToMove:
                drawText(surface, font, 'Black captured the town')
            else:
                drawText(surface, font, 'Red captured the town')
        elif gs.noMoveLeft:
            gameOver = True
            if gs.redToMove:
                drawText(surface, font, 'No moves left for red')
            else:
                drawText(surface, font, 'No moves left for black')

        clock.tick(max_fps)
        pygame.display.flip()


if __name__ == '__main__':
    main()
