import unittest

from othello import *

class is_valid_tile_func(unittest.TestCase):
    
    def setUp(self):
        self.ot = Othello(6, 6)
        
    def test_corner(self):
        self.assertTrue(self.ot.is_valid_tile((0, 0)))
        self.assertTrue(self.ot.is_valid_tile((0, 5)))
        self.assertTrue(self.ot.is_valid_tile((5, 0)))
        self.assertTrue(self.ot.is_valid_tile((5, 5)))
    
    def test_edge(self):
        self.assertTrue(self.ot.is_valid_tile((0, 3)))
        self.assertTrue(self.ot.is_valid_tile((5, 4)))
        self.assertTrue(self.ot.is_valid_tile((1, 0)))
        self.assertTrue(self.ot.is_valid_tile((2, 1)))
        
    def test_center(self):
        self.assertTrue(self.ot.is_valid_tile((3, 4)))
        self.assertTrue(self.ot.is_valid_tile((2, 1)))
        self.assertTrue(self.ot.is_valid_tile((4, 2)))
        self.assertTrue(self.ot.is_valid_tile((1, 3)))
        
    def test_invalid(self):
        self.assertFalse(self.ot.is_valid_tile((0, 6)))
        self.assertFalse(self.ot.is_valid_tile((-1, 4)))
        self.assertFalse(self.ot.is_valid_tile((6, 3)))
        self.assertFalse(self.ot.is_valid_tile((5, -1)))


class get_surrounding_tiles_func(unittest.TestCase):
    
    def setUp(self):
        self.ot = Othello(6, 6)
        
    def test_corner(self):
        expected = [(0, 1), (1, 0), (1, 1)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((0, 0)), expected)
        expected = [(0, 4), (1, 4), (1, 5)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((0, 5)), expected)
        expected = [(4, 0), (4, 1), (5, 1)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((5, 0)), expected)
        expected = [(4, 4), (4, 5), (5, 4)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((5, 5)), expected)
        
    def test_edge(self):
        expected = [(3, 0), (3, 1), (4, 1), (5, 0), (5, 1)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((4, 0)), expected)
        expected = [(0, 2), (1, 2), (1, 3), (1, 4), (0, 4)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((0, 3)), expected)
        expected = [(2, 4), (2, 5), (3, 4), (4, 4), (4, 5)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((3, 5)), expected)
        expected = [(4, 1), (4, 2), (4, 3), (5, 1), (5, 3)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((5, 2)), expected)
    
    def test_center(self):
        expected = [(2, 1), (2, 2), (2, 3), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((3, 2)), expected)
        expected = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((4, 4)), expected)


class get_possible_moves_func(unittest.TestCase):

    def setUp(self):
        self.ot = Othello(6, 6)
        
    def test_1(self):
        self.ot.board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,2,0,0],[0,0,2,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.ot.turn = 2
        expected = [(2, 1), (1, 2), (3, 4), (4, 3)]
        self.assertCountEqual(self.ot.get_possible_moves(), expected)
        
    def test_2(self):
        self.ot.board = [[0,0,0,0,0,0],[0,1,2,0,0,0],[0,1,2,2,0,0],[0,1,2,1,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0]]
        self.ot.turn = 2
        expected = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (3, 4), (4, 4), (4, 3), (5, 2)]
        self.assertCountEqual(self.ot.get_possible_moves(), expected)
    
    def test_3(self):
        self.ot.board = [[0,0,0,0,0,0],[0,1,1,1,0,0],[0,1,1,1,0,0],[0,1,2,2,2,0],[0,0,1,1,0,0],[0,0,0,1,0,0]]
        self.ot.turn = 1
        expected = [(3, 5), (2, 5), (4, 5), (4, 4), (2, 4), (4, 1)]
        self.assertCountEqual(self.ot.get_possible_moves(), expected)
        
    def test_4(self):
        self.ot.board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,2,2,2,0,0],[0,2,2,1,0,0],[0,2,0,0,0,0],[0,0,0,0,0,0]]
        self.ot.turn = 1
        expected = [(1, 1), (1, 3), (3, 0)]
        self.assertCountEqual(self.ot.get_possible_moves(), expected)


class make_move_func(unittest.TestCase):

    def setUp(self):
        self.ot = Othello(6, 6)
        
    def test_simulate_game_1(self):
        self.ot.board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,2,0,0],[0,0,2,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.ot.turn = 2
        
        self.ot.make_move((1, 2))
        expected = [[0,0,0,0,0,0],[0,0,2,0,0,0],[0,0,2,2,0,0],[0,0,2,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.assertCountEqual(self.ot.board, expected)
        self.assertEqual(self.ot.turn, 1)
        self.assertEqual(self.ot.white_tiles, 1)
        self.assertEqual(self.ot.black_tiles, 4)
        
        self.ot.make_move((1, 3))
        expected = [[0,0,0,0,0,0],[0,0,2,1,0,0],[0,0,2,1,0,0],[0,0,2,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.assertCountEqual(self.ot.board, expected)
        self.assertEqual(self.ot.turn, 2)
        self.assertEqual(self.ot.white_tiles, 3)
        self.assertEqual(self.ot.black_tiles, 3)
        
        self.ot.make_move((2, 4))
        expected = [[0,0,0,0,0,0],[0,0,2,1,0,0],[0,0,2,2,2,0],[0,0,2,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.assertCountEqual(self.ot.board, expected)
        self.assertEqual(self.ot.turn, 1)
        self.assertEqual(self.ot.white_tiles, 2)
        self.assertEqual(self.ot.black_tiles, 5)
        
        self.ot.make_move((3, 1))
        expected = [[0,0,0,0,0,0],[0,0,2,1,0,0],[0,0,1,2,2,0],[0,1,1,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.assertCountEqual(self.ot.board, expected)
        self.assertEqual(self.ot.turn, 2)
        self.assertEqual(self.ot.white_tiles, 5)
        self.assertEqual(self.ot.black_tiles, 3)


class check_victory_func(unittest.TestCase):

    def setUp(self):
        self.ot = Othello(6, 6)


if __name__ == "__main__":
    unittest.main()
