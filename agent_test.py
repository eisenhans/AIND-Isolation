"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import timeit

import isolation
import game_agent

from importlib import reload

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""
    

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.board = isolation.Board(self.player1, self.player2)
        self.board.apply_move((4, 4))
        self.board.apply_move((0, 2))
        
    def create_clock(self, time_limit = 150):
        time_millis = lambda: 1000 * timeit.default_timer()
        start = time_millis()
        return lambda : start + time_limit - time_millis()
    
    def test_is_distance_1(self):
        self.assertTrue(game_agent.is_distance_1((3, 3), (4, 5)))
        self.assertTrue(game_agent.is_distance_1((0, 0), (1, 2)))
        
        self.assertFalse(game_agent.is_distance_1((3, 3), (5, 5)))
        self.assertFalse(game_agent.is_distance_1((0, 0), (1, 1)))
        
    def test_distance(self):
        self.assertEqual(1, game_agent.distance(self.board, (0, 2), (2, 3)))
        self.assertEqual(2, game_agent.distance(self.board, (4, 4), (0, 2)))
        self.assertEqual(4, game_agent.distance(self.board, (2, 3), (0, 5)))
        
        self.board.apply_move((2, 1))
        self.board.apply_move((3, 1))
        self.board.apply_move((2, 2))
        self.board.apply_move((2, 3))
        self.board.apply_move((1, 4))
        
        self.assertEqual(-1, game_agent.distance(self.board, (4, 4), (0, 2)))
        
    def test_path_count(self):
        self.assertEqual(16, game_agent.path_count(self.board, (4, 4), (0, 2)))
        
#    def test_minimax_depth_1(self):
#        player = game_agent.MinimaxPlayer()
#        player.time_left = self.create_clock()
#        best_move = player.minimax(self.game, 1)
#        self.assertTrue((2, 3) == best_move or (3, 2) == best_move)
#        
#    def test_alphabeta_depth_1(self):
#        player = game_agent.AlphaBetaPlayer()
#        player.time_left = self.create_clock()
#        path = player.alphabeta(self.game, 1)
#        self.assertEquals([(3, 2)], path)
#       
#    def test_minimax_depth_2(self):
#        player = game_agent.MinimaxPlayer()
#        player.time_left = self.create_clock()
#        best_move = player.minimax(self.game, 2)
#        self.assertTrue((2, 3) == best_move or (3, 2) == best_move)
#        
#    def test_minimax_depth_3(self):
#        player = game_agent.MinimaxPlayer()
#        player.time_left = self.create_clock()
#        best_move = player.minimax(self.game, 3)
#        self.assertEqual((2, 3), best_move)
#        
#    def test_minimax_depth_4(self):
#        player = game_agent.MinimaxPlayer()
#        player.time_left = self.create_clock()
#        best_move = player.minimax(self.game, 4)
#        self.assertTrue(best_move in [(3, 2), (3, 6)], 'best move: ' + str(best_move))
#        
#    def test_minimax_depth_5(self):
#        player = game_agent.MinimaxPlayer()
#        player.time_left = self.create_clock(1000)
#        best_move = player.minimax(self.game, 5)
#        self.assertTrue(best_move in [(2, 3), (3, 2), (2, 5), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)], 'best move: ' + str(best_move))
#
#    def test_alphabeta_depth_5(self):
#        player = game_agent.AlphaBetaPlayer()
#        player.time_left = self.create_clock()
#        best_move = player.alphabeta(self.game, 5)
#        self.assertTrue(best_move in [(2, 3), (3, 2), (2, 5), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)], 'best move: ' + str(best_move))
#
#
#    def test_minimax_depth_6(self):
#        player = game_agent.MinimaxPlayer()
#        player.time_left = self.create_clock(1000)
#        best_move = player.minimax(self.game, 6)
#        self.assertTrue(best_move in [(2, 3), (3, 2), (2, 5), (3, 6), (5, 2), (5, 6), (6, 3), (6, 5)], 'best move: ' + str(best_move))

#    def test_minimax_depth_7(self):
#        player = game_agent.MinimaxPlayer()
#        player.time_left = self.create_clock(5000)
#        best_move = player.minimax(self.game, 7)
#        self.assertTrue(best_move in [(3, 6), (6, 3)], 'best move: ' + str(best_move))
#        
#    def test_alphabeta_depth_7(self):
#        player = game_agent.AlphaBetaPlayer(score_fn=game_agent.custom_score_2)
#        player.time_left = self.create_clock(1000)
#        best_move = player.alphabeta(self.game, 7)
#        self.assertTrue(best_move in [(3, 6), (6, 3)], 'best move: ' + str(best_move))        

#    def test_alphabeta_iterative_deepening(self):
#        player = game_agent.AlphaBetaPlayer()
#        best_move = player.get_move(self.game, self.create_clock())
#        self.assertTrue(best_move in [(2, 3), (3, 6), (6, 3)], 'best move: ' + str(best_move))
        
#    def test_alphabeta_iterative_deepening_2(self):
#        player = game_agent.AlphaBetaPlayer(score_fn=game_agent.custom_score_2)
#        best_move = player.get_move(self.game, self.create_clock())
#        self.assertTrue(best_move in [(2, 3), (2, 5), (3, 6), (5, 2), (5, 6), (6, 3)], 'best move: ' + str(best_move))          

if __name__ == '__main__':
    unittest.main()
