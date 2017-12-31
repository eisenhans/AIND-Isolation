class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Copied from game_agent.py."""
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')
    
    player_square = game.get_player_location(player)
    player_squares = squares_2_moves(game, player_square)
    
    opp_square = game.get_player_location(game.get_opponent(player))
    opp_squares = squares_2_moves(game, opp_square)
    
    common_square_factor = 0.5 if is_same_color(player_square, opp_square) else -0.5
    
    return len(player_squares) - len(opp_squares) + common_square_factor * len(player_squares & opp_squares)

def is_same_color(square_1, square_2):
    return square_1[0] + square_1[1] % 2 == square_2[0] + square_2[1] % 2

MOVE_DIRECTIONS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

def squares_2_moves(board, square):
    r, c = square
    
    moves1 = set((r + dr, c + dc) for dr, dc in MOVE_DIRECTIONS if board.move_is_legal((r + dr, c + dc)))
    
    moves2 = set((r1 + dr, c1 + dc) for dr, dc in MOVE_DIRECTIONS for (r1, c1) in moves1
                   if board.move_is_legal((r1 + dr, c1 + dc)))
    
    return moves1 | moves2


class CustomPlayer():
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. After each iteration, the branches are
    reordered so that the most promising branch is considered first. This
    improves the performance of the alpha-beta algorithm.
    """
    def __init__(self, score_fn=custom_score, timeout=10.):
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout    
    
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        
        best_path = []
        max_depth = len(game.get_blank_spaces())

        try:
            for depth in range(1, max_depth):
                better_path = self.alphabeta(game, depth, best_path)
                if better_path:
                    best_path = better_path
                else:
                    break

        except SearchTimeout:
            pass

#        print('depth reached by player {}: {}'.format(game.active_player, depth))
        # Return the best move from the last completed search iteration
        return best_path[0] if best_path else (-1, -1)    

    def alphabeta(self, game, depth, preferred_path, alpha = float("-inf"), beta = float("inf")):
        """Implements depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This is a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
            
        preferred_path : list
            The list of moves that seemed the most promising in the last
            iteration step

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        score, path = self.max_value(game, depth, preferred_path, alpha, beta)
        return path
        
    def max_value(self, game, depth, preferred_path, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        player = game.active_player
        if depth == 0 or game.is_loser(player):
            return self.score(game, player), []
        
        moves = game.get_legal_moves()
        if preferred_path and preferred_path[0] in moves:
            moves.remove(preferred_path[0])
            moves = [preferred_path[0]] + moves
            
        best_score = float("-inf")
        best_path = []
        count = 0
        for move in moves:
            count += 1
            after_move = game.forecast_move(move)
            (score, path) = self.min_value(after_move, depth - 1, preferred_path[1:], alpha, beta)
            if score > best_score:
                best_score = score
                best_path = [move] + path
                if best_score >= beta:
                    # beta is what the minimizing player can have at least.
                    # If the maximizing player can have more than beta here,
                    # we can skip the rest of the subbranch. The whole branch
                    # will not be chosen.
                    return (best_score, best_path)
                
                alpha = max(alpha, best_score)
        
        return (best_score, best_path)

    def min_value(self, game, depth, preferred_path, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        player = game.inactive_player
        if depth == 0 or game.is_winner(player):
            return self.score(game, player), []
        
        moves = game.get_legal_moves()
        if preferred_path and preferred_path[0] in moves:
            moves.remove(preferred_path[0])
            moves = [preferred_path[0]] + moves
            
        best_score = float("inf")
        best_path = []
        count = 0
        for move in moves:
            count += 1
            after_move = game.forecast_move(move)
            (score, path) = self.max_value(after_move, depth - 1, preferred_path[1:], alpha, beta)
            if score < best_score:
                best_score = score
                best_path = [move] + path
                if best_score <= alpha:
                    return (best_score, best_path)
                
                beta = min(beta, best_score)
        
        return (best_score, best_path)      
    
    def __str__(self):
        return type(self).__name__ + '|' + str(self.score.__name__)
