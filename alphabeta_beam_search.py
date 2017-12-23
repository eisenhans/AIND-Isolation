"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import timeit
import functools

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

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
    
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    return len(player_moves) - len(opponent_moves)

def score_after_move(game, player, move):
    after_move = game.forecast_move(move)
    return custom_score(after_move, player)

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

class AlphaBetaBeamSearchPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

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
        time_millis = lambda: 1000 * timeit.default_timer()
        move_start = time_millis()
        self.time_left = lambda : move_start + 150 - time_millis()
#        self.time_left = time_left
        
        best_path = []
        max_depth = len(game.get_blank_spaces())

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            for depth in range(1, max_depth):
                better_path = self.alphabeta(game, depth, best_path)
                if better_path:
                    best_path = better_path
#                    print('best path for depth ' + str(depth) + ': ' + str(best_path) + ' - time left: ' + str(time_left()) + ' ms')
                else:
                    break

        except SearchTimeout:
#            print('caught search timeout')
            pass  # Handle any actions required after timeout as needed

#        print('depth reached by player {}: {}'.format(game.active_player, depth))
        # Return the best move from the last completed search iteration
        return best_path[0] if best_path else (-1, -1)    

    def alphabeta(self, game, depth, preferred_path, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        score, path = self.max_value(game, depth, preferred_path, alpha, beta)
        return path
        
    def max_value(self, game, depth, preferred_path, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        active_player = game.active_player
        if depth == 0 or game.is_loser(active_player):
            return (self.score(game, active_player), [])
        
        moves = self.sort_moves(game.get_legal_moves(), preferred_path, game, active_player)
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
                    # beta is what the minimizing player can have at least. If the maximizing player can have more
                    # than beta here, we can skip the rest of the subbranch. The whole branch will not be chosen.
#                    print('beta pruning after checking {}/{} moves'.format(count, len(moves)))
                    return (best_score, best_path)
                
                alpha = max(alpha, best_score)
        
        return (best_score, best_path)

    def min_value(self, game, depth, preferred_path, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        active_player = game.active_player
        if depth == 0 or game.is_loser(active_player):
            return (-self.score(game, active_player), [])
        
        moves = self.sort_moves(game.get_legal_moves(), preferred_path, game, active_player)
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
#                    print('alpha pruning after checking {}/{} moves'.format(count, len(moves)))
                    return (best_score, best_path)
                
                beta = min(beta, best_score)
        
        return (best_score, best_path)      
    
    def sort_moves(self, moves, preferred_path, game, player):
        key_func = functools.partial(score_after_move, game, player)
        moves_sorted = sorted(moves, key = key_func, reverse = True)
#        move_counts = ''
#        for move in moves_sorted:
#            move_counts += ' ' + str(score_after_move(game, player, move))
#        print('move counts:{}'.format(move_counts))
#        moves_sorted = moves
        if preferred_path and preferred_path[0] in moves_sorted:
            moves_sorted.remove(preferred_path[0])
            moves_sorted = [preferred_path[0]] + moves_sorted
        
        return moves_sorted
    
    def __str__(self):
        return type(self).__name__ + '|' + str(self.score.__name__)
