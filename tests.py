import unittest

from othello import *

class valid_tile_func(unittest.TestCase):
    
    def setUp(self):
        self.ot = Othello(6, 6)
        
    def test_corner(self):
        self.assertTrue(self.ot.valid_tile(0, 0))
        self.assertTrue(self.ot.valid_tile(0, 5))
        self.assertTrue(self.ot.valid_tile(5, 0))
        self.assertTrue(self.ot.valid_tile(5, 5))
    
    def test_edge(self):
        self.assertTrue(self.ot.valid_tile(0, 3))
        self.assertTrue(self.ot.valid_tile(5, 4))
        self.assertTrue(self.ot.valid_tile(1, 0))
        self.assertTrue(self.ot.valid_tile(2, 1))
        
    def test_center(self):
        self.assertTrue(self.ot.valid_tile(3, 4))
        self.assertTrue(self.ot.valid_tile(2, 1))
        self.assertTrue(self.ot.valid_tile(4, 2))
        self.assertTrue(self.ot.valid_tile(1, 3))
        
    def test_invalid(self):
        self.assertFalse(self.ot.valid_tile(0, 6))
        self.assertFalse(self.ot.valid_tile(-1, 4))
        self.assertFalse(self.ot.valid_tile(6, 3))
        self.assertFalse(self.ot.valid_tile(2, 7))
        self.assertFalse(self.ot.valid_tile(5, -1))
        self.assertFalse(self.ot.valid_tile(6, 3))


class valid_move_func(unittest.TestCase):
    
    def setUp(self):
        self.ot = Othello(6, 6)


if __name__ == "__main__":
    unittest.main()
