import unittest

from othello import *

class valid_tile_func(unittest.TestCase):
    
    def setUp(self):
        self.ot = Othello(6, 6)
        
    def test_corner(self):
        self.assertTrue(self.ot.valid_tile((0, 0)))
        self.assertTrue(self.ot.valid_tile((0, 5)))
        self.assertTrue(self.ot.valid_tile((5, 0)))
        self.assertTrue(self.ot.valid_tile((5, 5)))
    
    def test_edge(self):
        self.assertTrue(self.ot.valid_tile((0, 3)))
        self.assertTrue(self.ot.valid_tile((5, 4)))
        self.assertTrue(self.ot.valid_tile((1, 0)))
        self.assertTrue(self.ot.valid_tile((2, 1)))
        
    def test_center(self):
        self.assertTrue(self.ot.valid_tile((3, 4)))
        self.assertTrue(self.ot.valid_tile((2, 1)))
        self.assertTrue(self.ot.valid_tile((4, 2)))
        self.assertTrue(self.ot.valid_tile((1, 3)))
        
    def test_invalid(self):
        self.assertFalse(self.ot.valid_tile((0, 6)))
        self.assertFalse(self.ot.valid_tile((-1, 4)))
        self.assertFalse(self.ot.valid_tile((6, 3)))
        self.assertFalse(self.ot.valid_tile((2, 7)))
        self.assertFalse(self.ot.valid_tile((5, -1)))
        self.assertFalse(self.ot.valid_tile((6, 3)))


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
        
    def test_edge(self):
        pass
    
    def test_center(self):
        expected = [(2, 1), (2, 2), (2, 3), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3)]
        self.assertCountEqual(self.ot.get_surrounding_tiles((3, 2)), expected)


class landlocked_func(unittest.TestCase):
    
    def setUp(self):
        self.ot = Othello(6, 6)
        
    def test_1(self):
        self.ot.board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        self.ot.board = [[0,0,0,0,0,0],[0,0,1,2,2,0],[0,0,2,1,1,0],[0,0,1,2,1,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        # self.assertTrue(self.ot.landlocked((2, 3)))


class valid_move_func(unittest.TestCase):
    
    def setUp(self):
        self.ot = Othello(6, 6)


class possible_moves_func(unittest.TestCase):

    def setUp(self):
        self.ot = Othello(6, 6)
        
    def test_1(self):
        self.ot.board = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,1,2,0,0],[0,0,2,1,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        expected = [(3, 1), (4, 2), (1, 3), (2, 4)]
        self.assertCountEqual(self.ot.get_possible_moves(), expected)


if __name__ == "__main__":
    unittest.main()
