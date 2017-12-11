"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import timeit

import isolation
import game_agent
from opening_player import OpeningPlayer, get_distance, is_border, no_border_filter

from importlib import reload

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""
    
    start_position_player_1 = (4, 4)
    start_position_player_2 = (0, 2)

    def setUp(self):
        reload(game_agent)
        self.player_1 = OpeningPlayer()
        self.player_2 = 'player_2'
        self.board = Board(player_1, player_2)

        
    def create_clock(self, time_limit = 150):
        time_millis = lambda: 1000 * timeit.default_timer()
        start = time_millis()
        return lambda : start + time_limit - time_millis()        
    
    def test_is_border(self):
        self.assertTrue(is_border(self.board, (0, 0)))
        self.assertTrue(is_border(self.board, (0, 1)))
        self.assertTrue(is_border(self.board, (3, 6)))
        
        self.assertFalse(is_border(self.board, (1, 1)))
        self.assertFalse(is_border(self.board, (5, 5)))
        
    def test_no_border_filter(self):
        self.assertEqual([(1, 1), (5, 5)], no_border_filter(self.board, [(0, 0), (0, 3), (1, 1), (5, 5), (5, 6)]))
  
if __name__ == '__main__':
    unittest.main()
