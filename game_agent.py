class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    The score is calculated from the squares that can be reached by each player
    in the next two moves. The return value is the number of squares that the
    current player can reach minus the number of squares that the opponent can
    reach plus or minus the number of squares that both players can reach
    (depending on whether the current player is the attacker or the defender).

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')
    
    player_square = game.get_player_location(player)
    player_squares = squares_2_moves(game, player_square)
    
    opp_square = game.get_player_location(game.get_opponent(player))
    opp_squares = squares_2_moves(game, opp_square)
    
    common_square_factor = 0.5 if is_attacker(game, player) else -0.5
    
    return len(player_squares) - len(opp_squares) + common_square_factor * len(player_squares & opp_squares)

def custom_score_2(game, player):
    """This score function is similar to improved_score. If the current player
    can make a move that will prevent his opponent from making the same move,
    a constant value of 3 is added to the score.
    """
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')

    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    score = float(len(player_moves) - len(opponent_moves))
    
    if bool(set(player_moves) & set(opponent_moves)):
        if is_attacker(game, player):
            return score + 3.
        return score - 3.
    
    return score

def custom_score_3(game, player):
    """This score function compares the number of squares that can be reached
    by each player in the next two moves.
    """
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')
    
    player_square = game.get_player_location(player)
    player_squares = squares_2_moves(game, player_square)
    
    opp_square = game.get_player_location(game.get_opponent(player))
    opp_squares = squares_2_moves(game, opp_square)
    
    return float(len(player_squares) - len(opp_squares))

def is_attacker(game, player):
    player_1_location = game._board_state[-1]
    player_2_location = game._board_state[-2]
    initiative = game._board_state[-3]
    
    return bool((player_1_location + player_2_location + initiative) % 2) == (player == game._player_2)

MOVE_DIRECTIONS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

def squares_2_moves(board, square):
    r, c = square
    
    moves1 = set((r + dr, c + dc) for dr, dc in MOVE_DIRECTIONS if board.move_is_legal((r + dr, c + dc)))
    
    moves2 = set((r1 + dr, c1 + dc) for dr, dc in MOVE_DIRECTIONS for (r1, c1) in moves1
                   if board.move_is_legal((r1 + dr, c1 + dc)))
    
    return moves1 | moves2


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search.
    """
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.
        This is a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        score, move = self.max_value(game, depth)
        return move
    
    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        player = game.active_player
        if depth == 0 or game.is_loser(player):
            return self.score(game, player), (-1, -1)
        
        moves = game.get_legal_moves()
        best_score = float("-inf")
        best_move = moves[0] if moves else None
        for move in moves:
            after_move = game.forecast_move(move)
            (score, min_move) = self.min_value(after_move, depth - 1)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_score, best_move
        
    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        player = game.inactive_player
        if depth == 0 or game.is_winner(player):
            return self.score(game, player), (-1, -1)
        
        moves = game.get_legal_moves()
        best_score = float("inf")
        best_move = (-1, -1)
        for move in moves:
            after_move = game.forecast_move(move)
            score, max_move = self.max_value(after_move, depth - 1)
            if score < best_score:
                best_score = score
                best_move = move
        
        return best_score, best_move
    
    def __str__(self):
        return type(self).__name__ + '|' + str(self.score.__name__)    

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning.
    """
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
        
        best_move = (-1, -1)
        max_depth = len(game.get_blank_spaces())

        try:
            for depth in range(1, max_depth):
                better_move = self.alphabeta(game, depth)
                if better_move != (-1, -1):
                    best_move = better_move
                else:
                    break

        except SearchTimeout:
            pass

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        _, move = self.max_value(game, depth, alpha, beta)
        return move
        
    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        player = game.active_player
        if depth == 0 or game.is_loser(player):
            return self.score(game, player), (-1, -1)
        
        moves = game.get_legal_moves()
        best_score = float("-inf")
        best_move = (-1, -1)
        for move in moves:
            after_move = game.forecast_move(move)
            score, _ = self.min_value(after_move, depth - 1, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
                if best_score >= beta:
                    return best_score, best_move
                
                alpha = max(alpha, best_score)
        
        return best_score, best_move

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        player = game.inactive_player
        if depth == 0 or game.is_winner(player):
            return self.score(game, player), (-1, -1)
        
        moves = game.get_legal_moves()
        best_score = float("inf")
        best_move = (-1, -1)
        for move in moves:
            after_move = game.forecast_move(move)
            score, _ = self.max_value(after_move, depth - 1, alpha, beta)
            if score < best_score:
                best_score = score
                best_move = move
                if best_score <= alpha:
                    return best_score, best_move
                
                beta = min(beta, best_score)
        
        return best_score, best_move   
    
    def __str__(self):
        return type(self).__name__ + '|' + str(self.score.__name__)

