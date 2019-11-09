#!/usr/bin/env python
# coding=utf-8

"""
 2048 游戏.
 1. 当棋盘中出现2048数字,则游戏胜利.
 2. 当无法合并,且没有空余方格时,则游戏失败.

显示：
  n×n 方格,默认是4*4方格.

"""

import os
import random
import copy

# 记录总得分
TOTAL_SCORE = 0
# 方向控制，输入键盘中的字母来控制相应的方向
DIRECT_DICT = {'j': 'left', 'l': 'right', 'i': 'up', 'k': 'down'}


def generate_new_matrix(size=4):
    """
    创建矩阵块，并随机产生两个数字，返回矩阵块
    """
    matrix = [[0 for i in range(size)] for j in range(size)]
    assert generate_cellvalue_in_block(matrix, size, 2)  # 确保初始界面有两个随机生成的数字

    assert any(matrix[i][j] > 0 for i in range(size) for j in range(size))
    return matrix


def display(matrix, size=4, conceal=0, info=""):
    """
    显示矩阵块(棋盘)
    """
    print "\nINPUT: { j-->LEFT, k-->DOWN ,l-->RIGHT, i-->UP },  ctrl+d: QUIT.\n"
    print "TOTAL SCORE:  %d" % TOTAL_SCORE

    linenum = size*9 + 1 # '-'符号的个数，根据matrix的大小来定
    print '-' * linenum
    for i in range(size):
        for j in range(size):
            if conceal or matrix[i][j]:
                output = '{:^6}'.format(matrix[i][j])
            else:
                output = '{:^6}'.format(' ')
            print '| ' + output,
        print '|'
        print '-' * linenum

    print info


def generate_cellvalue_in_block(matrix, size, num=1, value_scope=(2, 4)):
    """
    在matrix矩阵块的空白格中随机产生两个数.
    """
    assert all(matrix[i][j]>=0 for i in range(size) for j in range(size))
    assert num > 0
    assert all(i >= 2 for i in value_scope)

    # 查找matrix矩阵内的空余块，即matrix[i][j] == 0 的坐标，若不存在，则返回False
    blank_cell = [(i, j)  for i in range(size) for j in range(size) if matrix[i][j] == 0]
    if not 0 <= num <= len(blank_cell):
        return False

    pos = random.sample(blank_cell, num)
    for i in pos:
        matrix[i[0]][i[1]] = random.choice(value_scope)

    return True


def can_merge(matrix, size=4):
    """
    判断matrix是否还可以合并.
    """
    for row in range(size):
        for col in range(size-1):
            if matrix[row][col] == matrix[row][col+1]:
                return True
    for col in range(size):
        for row in range(size-1):
            if matrix[row][col] == matrix[row+1][col]:
                return True

    return False


def gameover(matrix, size=4):
    """
    判断是否游戏结束
    """
    blank_cell = [(i, j) for i in range(size) for j in range(size) if matrix[i][j] == 0]  #计算mtatrix中有无空余的点

    if  len(blank_cell) < 1 and not can_merge(matrix, size):
        return True
    else:
        return False


def gamewin(matrix, size=4):
    return any(matrix[i][j] == 2048  for i in range(size) for j in range(size))


def merge_row(matrix, rowspos, direct):
    """
    根据方向对matrix中的某一行或某一列进行合并,合并结果直接复制到matrix上.
    """
    global  TOTAL_SCORE
    row  = []

    # 将mrowspos中的所有点拷贝到新的列表row，对新列表进行合并操作
    for i in range(len(rowspos)):
        posx, posy = rowspos[i]
        row.append(matrix[posx][posy])

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

    # 复制结果到matrix
    j = 0
    for i in range(len(rowspos)):
        posx, posy = rowspos[i]
        matrix[posx][posy] = tmprow[j]
        j += 1


def process(matrix, direction, size=4):
    """
    根据键盘输入，对上下左右的输入做处理，退出按 Ctrl-C, Ctrl-D
     * 合并操作
     * 判断是否赢了（2048数字出现），或者无法再合并并且无法产生新的随机数了
    """
    assert direction in DIRECT_DICT.values()

    if direction in ["left", "right"]:
        for row in range(size):
            rowspos = [[row, col] for col in range(size)]  # 统计需要合并操作的行的所有点坐标
            if direction == "right":
                rowspos.reverse()
            merge_row(matrix, rowspos, direction)
    elif direction in  ["up", "down"]:
        for col in range(size):
            rowspos = [[row, col] for row in range(size)]
            if direction == "down":
                rowspos.reverse()
            merge_row(matrix, rowspos, direction)
    else:
        assert False

    if gameover(matrix, size):
        display(matrix, size=size, info="GAME OVER")
        exit()

    if gamewin(matrix, size):
        display(matrix, size=size, info="WIN WIN WIN")
        exit()


def get_input():
    while True:
        try:
            direct = raw_input()
            if direct not in DIRECT_DICT.keys():
                continue
            return direct
        except (KeyboardInterrupt, EOFError):
            print "BYE BYE!"
            exit()


def start():
    """
    start the 2048 game.
    """
    size = 4
    # assert size >= 4 and  size % 2 == 0
    matrix = generate_new_matrix(size)
    display(matrix, size=size)

    while True:
        next_direction = get_input()
        os.system('/usr/bin/clear')   # 清屏
        tmpmtrx = copy.deepcopy(matrix)   # 此处若用 tmpmtrx = matrix[:]会产生bug，因为这是浅拷贝
        process(matrix, DIRECT_DICT[next_direction], size)  # 处理键盘输入
        if tmpmtrx != matrix:
            generate_cellvalue_in_block(matrix, size)
        display(matrix, size=size)


if __name__ == "__main__":
    start()
