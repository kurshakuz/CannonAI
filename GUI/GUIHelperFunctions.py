import pygame

from GUI.GUIVariables import (col_names, colors, dimension, display_offset, n,
                          row_names, square_size, surface_size)

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
