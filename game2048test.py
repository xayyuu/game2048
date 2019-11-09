#!/usr/bin/env python
#coding=utf-8


import game2048
import unittest


class test_game_win(unittest.TestCase):
    def setUp(self):
        self.matrix = game2048.generate_new_matrix()
        self.size = 4


    def test_game_win_true(self):
        self.matrix[0][0] = 2048
        self.assertTrue(game2048.gamewin(self.matrix))

    def test_game_win_false(self):
        self.matrix[0][0] = 0
        self.assertFalse(game2048.gamewin(self.matrix))


class test_game_over(unittest.TestCase):
    def setUp(self):
        self.matrix = game2048.generate_new_matrix()
        self.size=4

    def test_game_over_true(self):
        initval = 2
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j] = initval
                initval *= 2
        self.assertTrue(game2048.gameover(self.matrix))

    def test_game_over_false(self):
        self.matrix[0][0] = 0
        self.assertFalse(game2048.gameover(self.matrix))

class test_merge_row(unittest.TestCase):
    def setUp(self):
        pass

    def test_merge_by_left(self):
        testrows = [
            [0, 0, 0, 2],
            [8, 8, 4, 4],
            [0, 2, 2, 0],
            [0, 4, 2, 2],
            [2, 2, 4, 8],
            [16, 4, 4, 2],
            [16, 4, 2, 8]
        ]
        testrows_left = [
            [2, 0, 0, 0],
            [16, 8, 0, 0],
            [4, 0, 0, 0],
            [4, 4, 0, 0],
            [4, 4, 8, 0],
            [16, 8, 2, 0],
            [16, 4, 2, 8]
        ]

        for i in range(len(testrows)):
            positions = [[i, j] for j in range(len(testrows[0]))]
            game2048.merge_row(testrows, positions, "left")
            self.assertEqual(testrows[i], testrows_left[i])

    def test_merge_by_right(self):
        testrows = [
            [2, 2, 2, 0],
            [16, 8, 0, 0],
            [4, 0, 0, 0],
            [4, 4, 0, 0],
            [4, 4, 8, 0],
            [16, 8, 2, 0],
            [16, 2, 2, 8]
            ]
        testrows_right = [
            [0, 0, 2, 4],
            [0, 0, 16, 8],
            [0, 0, 0, 4],
            [0, 0, 0, 8],
            [0, 0, 8, 8],
            [0, 16, 8, 2],
            [0, 16, 4, 8]
        ]

        for i in range(len(testrows)):
            positions = [[i, j] for j in range(len(testrows[0]))]
            positions.reverse()
            game2048.merge_row(testrows, positions, "right")
            self.assertEqual(testrows[i], testrows_right[i])

    def test_merge_by_up(self):
        testrows = [
            [2, 2, 2, 4],
            [16, 8, 0, 4],
            [4, 0, 2, 4],
            [4, 4, 0, 0],
        ]
        testrows_up = [
            [2, 2, 4, 8],
            [16, 8, 0, 4],
            [8, 4, 0, 0],
            [0, 0, 0, 0],
        ]

        for j in range(len(testrows[0])):
            positions = [[i, j] for i in range(len(testrows))]
            game2048.merge_row(testrows, positions, "up")
            for i in range(len(testrows)):
                self.assertEqual(testrows[i][j], testrows_up[i][j])


    def test_merge_by_down(self):
        testrows = [
            [2, 2, 2, 4],
            [16, 8, 0, 4],
            [4, 0, 2, 4],
            [4, 4, 0, 0],
        ]
        testrows_down = [
            [0, 0, 0, 0],
            [2, 2, 0, 0],
            [16, 8, 0, 4],
            [8, 4, 4, 8],
        ]

        for j in range(len(testrows[0])):
            positions = [[i, j] for i in range(len(testrows))]
            positions.reverse()
            game2048.merge_row(testrows, positions, "down")
            for i in range(len(testrows)):
                self.assertEqual(testrows[i][j], testrows_down[i][j])

class test_generate_cell_value(unittest.TestCase):
    def setUp(self):
        self.matrix = game2048.generate_new_matrix()
        self.size = 4
        self.leftnum = self.size ** 2 - 2

    def test_generate_cellvalue_true(self):
        i = 0
        while i < self.leftnum:
            self.assertTrue(game2048.generate_cellvalue_in_block(self.matrix, self.size, 1))
            i += 1

    def test_generate_cellvalue_false(self):
        i = 15
        while i > 1:
            i -= 1
            self.assertFalse(game2048.generate_cellvalue_in_block(self.matrix, self.size, self.leftnum+i))


if __name__ == "__main__":
    unittest.main()