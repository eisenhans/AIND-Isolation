from random import randint
import timeit
import math
import sys
import game_agent
import sample_players
import isolation
from copy import copy



class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def no_border_filter(board, squares):
    return [square for square in squares if not is_border(board, square)]

def is_border(board, square):
    row, col = square
    return row in [0, board.height - 1] or col in [0, board.width - 1]

def get_distance(square_1, square_2):
    row_1, col_1 = square_1
    row_2, col_2 = square_2
    return math.sqrt(float((row_2 - row_1)**2 + (col_2 - col_1)**2))

def get_moves(board, square):
    """Generate the list of possible moves for an L-shaped motion (like a
    knight in chess).
    """
    r, c = square
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    valid_moves = [(r + dr, c + dc) for dr, dc in directions
                   if board.move_is_legal((r + dr, c + dc))]
    
#    print('valid moves from ' + str(loc) + ': ' + str(valid_moves))
    return valid_moves

class OpeningPlayer(game_agent.IsolationPlayer):
    
    # 51.2%, 63.8%, 48.8%  
    visit_square_sets_offensive_strategy = [{(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)},
                  {(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5)},
                  {(3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1), (5, 2), (5, 3)},
                  {(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)}]
    
    def __init__(self, use_offensive_strategy = True, use_defensive_strategy = True):
        self.alphabeta_player = game_agent.AlphaBetaPlayer(score_fn = game_agent.improved_score)
        self.squares_to_visit = None
        self.use_offensive_strategy = use_offensive_strategy
        self.use_defensive_strategy = use_defensive_strategy
        super(OpeningPlayer, self).__init__()
    
    def get_move(self, board, time_left):
        self.time_left = time_left
        
        current_square_player = board.get_player_location(board.active_player)
        current_square_opponent = board.get_player_location(board.inactive_player)
        advantage = game_agent.is_same_color(current_square_player, current_square_opponent)
        
        if advantage and self.use_offensive_strategy:
            return self.get_move_offensive_strategy(board, time_left)
        
        if not advantage and self.use_defensive_strategy:
            return self.get_move_defensive_strategy(board, time_left)
        
        return self.alphabeta_player.get_move(board, time_left)

    def get_move_offensive_strategy(self, board, time_left):
        if board.move_count <= 7:
            move = self.move_towards_opponent(board)
            if move:
                return move
            else:
                return self.alphabeta_player.get_move(board, time_left)
        
        if self.squares_to_visit == None:
            self.squares_to_visit = self.find_squares_to_visit_offensive_strategy(board)
        
        if board.move_count <= 11:
            self.squares_to_visit = self.squares_to_visit & set(board.get_blank_spaces())
            
            moves = no_border_filter(board, board.get_legal_moves())
            if moves:
                visiting_moves = list(set(moves) & self.squares_to_visit)
                if visiting_moves:
                    # choose a move from where you can visit another square from the target set in the next move
                    return self.find_square_close_to(board, self.squares_to_visit, visiting_moves)
                
                # choose a move from where you can visit a square from the target set in the next move
                return self.find_square_close_to(board, self.squares_to_visit, moves)
                    
        return self.alphabeta_player.get_move(board, time_left)
     
    def get_move_defensive_strategy(self, board, time_left):
        if board.move_count <= 15:
            move = self.move_towards_center(board)
            if move:
                return move
        
        return self.alphabeta_player.get_move(board, time_left)
        
    def find_square_close_to(self, board, square_set, possible_squares):
        closest_square = None
        max_squares = -1
        for square in possible_squares:
            reachable = len(set(get_moves(board, square)) & square_set)
            if reachable > max_squares:
                max_squares = reachable
                closest_square = square
                
        return closest_square
    
    def move_towards_center(self, board):
        chosen_move = None
        smallest_distance = float('inf')
        for move in board.get_legal_moves():
            distance = get_distance(move, (3, 3))
            if distance < smallest_distance and not self.is_blunder(board, move):
                smallest_distance = distance
                chosen_move = move
                
        return chosen_move
    
    def move_towards_opponent(self, board, avoid_squares = []):
        opponent_square = board.get_player_location(board.inactive_player)
        
        chosen_move = None
        smallest_distance = float('inf')
        for move in board.get_legal_moves():
            if is_border(board, move) or move in avoid_squares:
                continue
            distance = get_distance(move, opponent_square)
            if distance < smallest_distance:
                smallest_distance = distance
                chosen_move = move
                
        return chosen_move
    
    def find_squares_to_visit_offensive_strategy(self, board):
        empty_squares = set(board.get_blank_spaces())
        
        min_square_set = None
        min_count = sys.maxsize
        for square_set in self.visit_square_sets_offensive_strategy:
            unvisited = square_set & empty_squares
            if len(unvisited) < min_count:
                min_count = len(unvisited)
                min_square_set = unvisited
        
        return min_square_set
 
    def is_same_color(self, square_1, square_2):
        return self.is_dark_square(square_1) == self.is_dark_square(square_2)
    
    def is_dark_square(self, square):
        return (square[0] + square[1]) % 2
            
    def is_blunder(self, board, move):
        board_after_move = board.forecast_move(move)
        for opp_move in board_after_move.get_legal_moves():
            if board_after_move.forecast_move(opp_move).is_loser(board.active_player):
#                print('move {} -> {} would be a blunder - will not be played!\n{}\n'.format(
#                        board.get_player_location(board.active_player), move, board.to_string()))
                return True
        
        return False
    
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
        
        return valid_moves           
        
    def __str__(self):
        return type(self).__name__ + '|offensive:' + str(self.use_offensive_strategy) + '|defensive:' + str(self.use_defensive_strategy)