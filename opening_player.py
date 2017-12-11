
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
    
#    visit_square_lists_same_color = [[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)],
#                      [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5)],
#                      [(3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3)],
#                      [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]]
    
    visit_square_lists_same_color = [[(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (3, 1)],
                  [(1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (3, 5)],
                  [(3, 1), (4, 1), (4, 2), (5, 1), (5, 2), (5, 3)],
                  [(3, 5), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]]
    
#    visit_square_lists_same_color = [[(1, 1), (1, 2), (2, 1), (2, 2)],
#                  [(1, 4), (1, 5), (2, 4), (2, 5)],
#                  [(4, 1), (4, 2), (5, 1), (5, 2)],
#                  [(4, 4), (4, 5), (5, 4), (5, 5)]]
#    
#    visit_square_lists_same_color = [[(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)],
#                  [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5)],
#                  [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1)],
#                  [(1, 5), (2, 5), (3, 5), (4, 5), (5, 5)]]
    
#    visit_square_lists_same_color = [[(1, 2), (1, 3), (1, 4)],
#                  [(5, 2), (5, 3), (5, 4)],
#                  [(2, 1), (3, 1), (4, 1)],
#                  [(2, 5), (3, 5), (4, 5)]]
    
#    visit_square_lists_same_color = [[(0, 2), (0, 3), (0, 4)],
#                  [(6, 2), (6, 3), (6, 4)],
#                  [(2, 0), (3, 0), (4, 0)],
#                  [(2, 6), (3, 6), (4, 6)]]        
    
#    visit_square_lists_same_color = [[(1, 1), (1, 2), (2, 1), (4, 5), (5, 4), (5, 5)],
#                  [(1, 4), (1, 5), (2, 5), (4, 1), (5, 1), (5, 2)]]
    
#    visit_square_lists = [[(1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (2, 4)],
#                  [(4, 2), (4, 3), (4, 4), (5, 2), (5, 3), (5, 4), (5, 5)],
#                  [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (4, 1), (4, 2)],
#                  [(2, 4), (2, 5), (3, 4), (3, 5), (4, 4), (4, 5), (5, 5)]]  
    
    # if different colors
    visit_square_lists_different_color = [[(2, 3), (4, 3), (3, 2), (3, 4), (3, 3)]] 
    
#    visit_square_lists = [[(1, 1), (2, 3), (1, 5), (3, 4), (5, 5), (4, 3), (5, 1), (3, 2)]]   
    
#    visit_square_lists = [[(3, 3), (4, 4), (2, 2), (2, 4), (4, 2)]]
    
#    visit_square_lists = [[(2, 3), (3, 2), (3, 4), (4, 3)]]
    
    def __init__(self):
        self.alphabeta_player = game_agent.AlphaBetaPlayer()
        self.squares_to_visit = None
        super(OpeningPlayer, self).__init__()
    
    def get_move(self, board, time_left):
#        time_millis = lambda: 1000 * timeit.default_timer()
#        move_start = time_millis()
#        self.time_left = lambda : move_start + 150 - time_millis()
        
        self.time_left = time_left
        
        if board.move_count <= 3:
            self.squares_to_visit = self.find_squares_to_visit(board)
#            print('will try to visit these squares: {}'.format(self.squares_to_visit))
            
        if self.squares_to_visit:
            visit = self.squares_to_visit.copy()
            move = self.find_visiting_move(board)
            current_square_player = board.get_player_location(board.active_player)
#            print('tried to find a move from {} to one of the squares {}, result: {}'.format(current_square_player, visit, move))
            if move:
                return move
            
#        print('opening finished - AlphabetaPlayer is playing')
        return self.alphabeta_player.get_move(board, time_left)
        
    def find_squares_to_visit(self, board):
        current_square_player = board.get_player_location(board.active_player)
        current_square_opponent = board.get_player_location(board.inactive_player)
        same_color = self.is_same_color(current_square_player, current_square_opponent)
        
        if not same_color:
            squares = list(set(OpeningPlayer.visit_square_lists_different_color[0]) & set(board.get_blank_spaces()))
            print('bad situation - trying to visit these squares: {}'.format(squares))
            return squares
#        print('current square player/opponent: {}/{}, same color: {}'.format(current_square_player, current_square_opponent, same_color))
        
        squares = self.find_square_list_same_color_with(current_square_player)
        if not squares:
            for move in board.get_legal_moves():
                squares = self.find_square_list_same_color_with(move)
                if squares:
                    break
        
        squares = list(set(squares) & set(board.get_blank_spaces()))
        print('good situation - trying to visit these squares: {}'.format(squares))
        
        return squares
    
    def is_same_color(self, square_1, square_2):
        return self.is_dark_square(square_1) == self.is_dark_square(square_2)
    
    def is_dark_square(self, square):
        return (square[0] + square[1]) % 2
            
    def find_square_list_same_color_with(self, start_square):
        for square_list in OpeningPlayer.visit_square_lists_same_color:
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
                if not self.is_blunder(board, move):
                    return move
            
        if not self.squares_to_visit:
            return None
        
        from_square = board.get_player_location(board.active_player)
        goal_square = self.squares_to_visit[0]
#        print('none of the squares from {} are directly accessible from {} - trying to access {} indirectly (opp. loc: {})'.format(
#           self.squares_to_visit, from_square, self.squares_to_visit[0], opponent_location))
        to_square = self.find_path(board, from_square, goal_square)
#        print('moving towards square {} with move {} -> {}'.format(goal_square, from_square, to_square))
        
        return to_square
    
    def is_blunder(self, board, move):
        board_after_move = board.forecast_move(move)
        for opp_move in board_after_move.get_legal_moves():
            if board_after_move.forecast_move(opp_move).is_loser(board.active_player):
                print('move {} -> {} would be a blunder - will not be played!\n{}\n'.format(
                        board.get_player_location(board.active_player), move, board.to_string()))
                return True
        
        return False
    
    def find_path(self, board, from_square, to_square):
        near_to_square = set(self.get_moves(board, to_square))
        frontier = list(near_to_square)
        legal_moves = board.get_legal_moves()
        
        for _ in range(1, 6):
            new_frontier = []
            for square in frontier:
                if square in legal_moves:
                    return square
                new_frontier.extend(self.get_moves(board, square))
            
    #        print('count: {}, frontier: {}'.format(count, frontier))
            frontier = [x for x in new_frontier if x not in near_to_square]
            near_to_square |= set(frontier)
            
        raise RuntimeError('no path from {} to {} found:\n{}'.format(from_square, to_square, board.to_string()))    
 
    def get_moves(self, board, square):
        """Generate the list of possible moves for an L-shaped motion (like a
        knight in chess).
        """
        if square == isolation.Board.NOT_MOVED:
            return board.get_blank_spaces()
    
        r, c = square
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        valid_moves = [(r + dr, c + dc) for dr, dc in directions
                       if board.move_is_legal((r + dr, c + dc))]
        
    #    print('valid moves from ' + str(loc) + ': ' + str(valid_moves))
        return valid_moves           
        
    def __str__(self):
        return type(self).__name__