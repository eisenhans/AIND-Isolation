"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest
import timeit

import isolation
import game_agent
from competition_agent import MonteCarloPlayer
from competition_agent import MonteCarloPosition

from importlib import reload

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""
    

    def setUp(self):
        reload(game_agent)
        self.player_1 = "Player1"
        self.player_2 = "Player2"
        self.board = isolation.Board(self.player_1, self.player_2)
        self.board.apply_move((4, 4))
        self.board.apply_move((0, 2))
        self.agent = MonteCarloPlayer()
        
        root = MonteCarloPosition(self.board, None)
        root.wins = 11
        root.simulations = 21
        self.agent.update_root(root)
        node_1 = self.add_child_pos(root, (3, 2), 7, 10)
        
        node_2 = self.add_child_pos(root, (6, 3), 3, 8)
        node_3 = self.add_child_pos(root, (6, 5), 0, 3)
        
        node_11 = self.add_child_pos(node_1, (1, 1), 2, 4)
        node_12 = self.add_child_pos(node_1, (1, 3), 1, 6)
        
        node_21 = self.add_child_pos(node_2, (4, 2), 1, 2)
        node_22 = self.add_child_pos(node_2, (5, 1), 2, 3)
        node_23 = self.add_child_pos(node_2, (5, 5), 2, 3)
        
        node_121 = self.add_child_pos(node_12, (0, 5), 2, 3)
        node_122 = self.add_child_pos(node_12, (0, 1), 3, 3)
        
        self.agent.frontier = [node_11, node_121, node_122, node_21, node_22, node_23, node_3]
        
    def add_child_pos(self, parent, move, wins, simulations):
        board = parent.board.forecast_move(move)
        pos = MonteCarloPosition(board, move, parent)
        pos.wins = wins
        pos.simulations = simulations
        parent.add_child(pos)
        return pos
        
    def create_clock(self, time_limit = 150):
        time_millis = lambda: 1000 * timeit.default_timer()
        start = time_millis()
        return lambda : start + time_limit - time_millis()        
        
#    def test_copy_board(self):
#        player_1 = 'p1'
#        player_2 = 'p2'
#        copy_1 = self.agent.copy_board(self.board, player_1, player_2)
#        self.assertEqual(2, copy_1.move_count)
#        self.assertEqual(player_1, copy_1.active_player)
#        self.assertEqual(player_2, copy_1.inactive_player)
#        
#        self.board.apply_move((6, 5))
#        copy_2 = self.agent.copy_board(self.board, player_1, player_2)
#        self.assertEquals(3, copy_2.move_count)
#        self.assertEqual(player_2, copy_2.active_player)
#        self.assertEqual(player_1, copy_2.inactive_player)
#        
#        blank = copy_2.get_blank_spaces()
#        self.assertFalse((0, 2) in blank)
#        self.assertFalse((4, 4) in blank)
#        self.assertFalse((6, 5) in blank)
        
#    def test_monte_carlo_search(self):
#        node = self.agent.select_next_node()
#        print('node: {}'.format(node))
#        self.assertEqual((0, 1), node.move)
#        self.assertEqual(3, node.wins)
#        self.assertEqual(3, node.simulations)
#        
#        new_nodes = self.agent.expand_node(node)
#        new_node = new_nodes[0]
#        print('expanded node: {} -> {}'.format(node, new_node))
#        self.assertEqual(node, new_node.parent)
#        
#        is_win = self.agent.simulate(new_node)
#        print('win: {}'.format(is_win))
#        
#        self.agent.propagate_back(new_node, False)
#        self.assertEquals(1, new_node.simulations)
#        self.assertEquals(0, new_node.wins)
#        
#        self.assertEquals(4, new_node.parent.simulations)
#        self.assertEquals(4, new_node.parent.wins)
#        
#        self.assertEquals(7, new_node.parent.parent.simulations)
#        self.assertEquals(1, new_node.parent.parent.wins)
#        
#        self.assertEquals(11, new_node.parent.parent.parent.simulations)
#        self.assertEquals(8, new_node.parent.parent.parent.wins)         
#        
#        self.assertEquals(22, self.agent.root.simulations)
#        self.assertEquals(11, self.agent.root.wins)
        
    def test_get_move(self):
        move = self.agent.get_move(self.board, self.create_clock())
        self.assertTrue(move in [(2, 5), (2, 3), (3, 2), (3, 6), (5, 2), (6, 39), (6, 5)], 'best move: ' + str(move))

#    def test_monte_carlo(self):
#        player = competition_agent.MonteCarloPlayer()
#        best_move = player.get_move(self.game, self.create_clock())
#        self.assertTrue(best_move in [(2, 3), (3, 6), (6, 3)], 'best move: ' + str(best_move))

if __name__ == '__main__':
    unittest.main()
