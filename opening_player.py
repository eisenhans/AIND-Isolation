
from random import randint
import timeit
import math
import game_agent
import sample_players
import isolation
from copy import copy



class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

class OpeningPlayer(game_agent.IsolationPlayer):
    
    visit_square_lists = [[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)],
                      [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5)],
                      [(3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3)],
                      [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]]
    
    def __init__(self):
        self.alphabeta_player = game_agent.AlphaBetaPlayer()
        self.squares_to_visit = None
        super(OpeningPlayer, self).__init__()
    
    def get_move(self, board, time_left):
#        time_millis = lambda: 1000 * timeit.default_timer()
#        move_start = time_millis()
#        self.time_left = lambda : move_start + 150 - time_millis()
        
        self.time_left = time_left
        
        if self.squares_to_visit == None:
            self.squares_to_visit = self.find_squares_to_visit(board)
            
        if self.squares_to_visit:
            move = self.find_visiting_move(board)
#            print('tried to find a move to one of the squares {}, result: {}'.format(self.squares_to_visit, move))
            if move:
                return move

        return self.alphabeta_player.get_move(board, time_left)
        
    def find_squares_to_visit(self, board):
        current_square_player = board.get_player_location(board.active_player)
        current_square_opponent = board.get_player_location(board.inactive_player)
        same_color = self.is_same_color(current_square_player, current_square_opponent)
        
        if not same_color:
            return []
#        print('current square player/opponent: {}/{}, same color: {}'.format(current_square_player, current_square_opponent, same_color))
        
        squares_to_visit = self.find_square_list_with(current_square_player)
        if squares_to_visit:
            squares_to_visit.remove(current_square_player)
            return squares_to_visit
        
        for move in board.get_legal_moves():
            squares_to_visit = self.find_square_list_with(move)
            if squares_to_visit:
                return squares_to_visit
                
        raise RuntimeError('square ' + str(current_square) + ' not close to any square list')
    
    def is_same_color(self, square_1, square_2):
        return self.is_dark_square(square_1) == self.is_dark_square(square_2)
    
    def is_dark_square(self, square):
        return (square[0] + square[1]) % 2
            
    def find_square_list_with(self, start_square):
        for square_list in OpeningPlayer.visit_square_lists:
            if start_square in square_list:
                return list(square_list)
        return None
    
    def find_visiting_move(self, board):
        opponent_location = board.get_player_location(board.get_opponent(board.active_player))
        if opponent_location in self.squares_to_visit:
            self.squares_to_visit.remove(opponent_location)

        for move in board.get_legal_moves():
            if move in self.squares_to_visit:
                self.squares_to_visit.remove(move)
                return move
            
        return None
        
        
    