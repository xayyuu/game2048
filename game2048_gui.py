#!/usr/bin/python
# coding:utf-8


import pygame
import sys, random, copy
from pygame.locals import *


# 记录总得分
TOTAL_SCORE = 0

#
BOARDWIDTH = 4
BOARDHEIGHT = 4
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30

#                      R       G    B
BLACK          =       (0,     0,   0)
WHITE          =       (255, 255, 255)
BRIGHTBLUE     =       (0,    50, 255)
DARKTURQUOISE  =       (3,    54,  73)
GREEN          =       (0,    204,  0)

#
BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 15
MESSAGECOLOR = WHITE

#
XMARGIN = int((WINDOWWIDTH - (TILESIZE*BOARDWIDTH +(BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE*BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT, SCORE_SURF, SCORE_RECT, TOTAL_SCORE

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Game 2048')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    NEW_SURF, NEW_RECT = make_text('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 30)

    size = 4
    main_board = generate_new_board(size)
    display(main_board)


    while True:
        next_direction = None
        check_for_quit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                if NEW_RECT.collidepoint(event.pos):
                    TOTAL_SCORE = 0
                    main_board = generate_new_board(size)
                    display(main_board)
            elif event.type == KEYUP:
                # 检查键盘输入
                if event.key in (K_LEFT, K_j):
                    next_direction = "left"
                elif event.key in (K_RIGHT, K_l):
                    next_direction = "right"
                elif event.key in (K_UP, K_i):
                    next_direction = "up"
                elif event.key in (K_DOWN, K_s):
                    next_direction = "down"

        if next_direction:
            tmp_board = copy.deepcopy(main_board)
            process(main_board, next_direction)
            if tmp_board != main_board:
                generate_random_value(main_board)
            draw_board(main_board, '')

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def check_for_quit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def terminate():
    pygame.quit()
    sys.exit()


def display(board, msg='', delay=500):
    draw_board(board, msg)
    pygame.display.update()
    pygame.time.wait(delay)  # 暂停500ms


def get_left_top_of_tile(tilex, tiley):
    left = XMARGIN + (tilex * TILESIZE) + (tilex - 1)
    top = YMARGIN + (tiley * TILESIZE) + (tiley - 1)
    return (left, top)


def draw_tile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = get_left_top_of_tile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 0:
        text_surf = BASICFONT.render('', True, TEXTCOLOR)
    else:
        text_surf = BASICFONT.render(str(number), True, TEXTCOLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(text_surf, text_rect)


def draw_board(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        text_surf, text_rect = make_text(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(text_surf, text_rect)

    size = len(board)
    for tilex in range(size):
        for tiley in range(size):
            draw_tile(tilex, tiley, board[tilex][tiley])

    left, top = get_left_top_of_tile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left-5, top-5, width+11, height+11), 4)

    SCORE_SURF, SCORE_RECT = make_text(get_score_text(), TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 140, WINDOWHEIGHT - 60)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT)


def make_text(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def get_score_text():
    return "SCORE:   " + str(TOTAL_SCORE)


def generate_new_board(size=4):
    board = [[0 for i in range(size)] for j in range(size)]
    assert generate_random_value(board, num=2)  # 确保初始界面有两个随机生成的数字

    assert any(board[i][j] > 0 for i in range(size) for j in range(size))
    return board


def generate_random_value(board, num=1, value_scope=(2, 4)):
    size = len(board)
    assert all(board[i][j]>=0 for i in range(size) for j in range(size))
    assert num > 0
    assert all(i >= 2 for i in value_scope)

    # 查找board矩阵内的空余块，即board[i][j] == 0 的坐标，若不存在，则返回False
    blank_cell = [(i, j)  for i in range(size) for j in range(size) if board[i][j] == 0]
    if not 0 <= num <= len(blank_cell):
        return False

    pos = random.sample(blank_cell, num)
    for i in pos:
        board[i[0]][i[1]] = random.choice(value_scope)

    return True


def can_merge(board):
    size = len(board)
    for row in range(size):
        for col in range(size-1):
            if board[row][col] == board[row][col+1]:
                return True
    for col in range(size):
        for row in range(size-1):
            if board[row][col] == board[row+1][col]:
                return True

    return False


def gameover(board):
    size = len(board)
    blank_cell = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]  #计算matrix中有无空余的点

    if  len(blank_cell) < 1 and not can_merge(board):
        return True
    else:
        return False


def gamewin(board):
    size = len(board)
    return any(board[i][j] == 2048  for i in range(size) for j in range(size))


def merge_row(board, rowspos, direct):
    global  TOTAL_SCORE
    row  = []

    # 将rowspos中的所有点拷贝到新的列表row，对新列表进行合并操作
    for i in range(len(rowspos)):
        posx, posy = rowspos[i]
        row.append(board[posx][posy])

    # 合并一行，遇见相同的数字，则合并
    for i in range(len(row)-1):
        nextpos = i + 1
        while nextpos < len(row):
            if row[nextpos] != 0:
                break
            nextpos += 1
        if nextpos >= len(row):
            break
        if row[i] > 0 and row[i] == row[nextpos]:
            row[i] *= 2
            row[nextpos] = 0
            TOTAL_SCORE += row[i]
    # 省略列表中间的零，比如[2, 0, 4, 0], 处理后应为 [2, 4, 0, 0]
    tmprow = [0] * len(row)
    j = 0
    for i in range(len(row)):
        if row[i] != 0:
            tmprow[j] = row[i]
            j += 1

    # 复制结果到board
    j = 0
    for i in range(len(rowspos)):
        posx, posy = rowspos[i]
        board[posx][posy] = tmprow[j]
        j += 1


def process(board, direction):
    """
    根据键盘输入，对上下左右的输入做处理
     * 合并操作
     * 判断是否赢了（2048数字出现），或者无法再合并并且无法产生新的随机数了
    """
    assert direction in ["left", "right", "up", "down"]
    size = len(board)

    if direction in ["left", "right"]:
        for col in range(size):
            rowspos = [[row, col] for row in range(size)]
            if direction == "right":
                rowspos.reverse()
            merge_row(board, rowspos, direction)
    elif direction in  ["up", "down"]:
        for row in range(size):
            rowspos = [[row, col] for col in range(size)]  # 统计需要合并操作的行的所有点坐标
            if direction == "down":
                rowspos.reverse()
            merge_row(board, rowspos, direction)
    else:
        assert False

    if gameover(board):
        msg = "GAME OVER"
        display(board, msg, 5000)
        terminate()

    if gamewin(board):
        msg = "WIN WIN WIN"
        display(board, msg, 5000)
        terminate()


if __name__ == "__main__":
    main()