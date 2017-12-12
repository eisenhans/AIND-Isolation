"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import time
import timeit
import isolation

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def improved_score(game, player):
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
    # TODO: finish this function!
    #raise NotImplementedError
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')
    
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
#    print('possible moves for player from ' + str(game.get_player_location(player)) + ': ' + str(player_moves))
#    print('possible moves for opponent from ' + str(game.get_player_location(game.get_opponent(player))) + ': ' + str(opponent_moves))
#    print('possible moves for player/opponent: ' + str(len(player_moves)) + '/' + str(len(opponent_moves)))
    
    return len(player_moves) - len(opponent_moves)

def custom_score_advantage_aware(game, player):
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')
    
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    common_moves = set(player_moves) & set(opponent_moves)
    
    same_color = is_same_color(game.get_player_location(player), game.get_player_location(game.get_opponent(player)))
    
    common_score = 2 * len(common_moves)
    if not same_color:
        common_score = - common_score
    
    score = len(player_moves) - len(opponent_moves) + common_score
#    print('score: player - opp + common = {} - {} + {} = {}'.format(len(player_moves), len(opponent_moves), common_score, score))
    return score
    
#    print('calculating custom score for player {}'.format(player))
    
#    current_square_player = game.get_player_location(player)
#    current_square_opponent = game.get_player_location(game.get_opponent(player))
#    
#    player_moves = len(game.get_legal_moves(player))
#    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
#    
#    move_score = player_moves - opponent_moves
#    
#    move_score = player_moves / (player_moves + opponent_moves)
#    path_score = path_count(game, current_square_player, current_square_opponent) / 4
#    path_score = distance(current_square_player, current_square_opponent) / 72
#    if not is_same_color(current_square_player, current_square_opponent):
#        path_score = 1 - path_score
    
#    print('score move + path = sum: {} + {} = {}'.format(move_score, path_score, move_score + path_score))
#    return move_score #+ path_score
    
#    return 2 * len(player_moves) - len(opponent_moves)

def distance(square_1, square_2):
    row_1, col_1 = square_1
    row_2, col_2 = square_2
    return float((row_2 - row_1)**2 + (col_2 - col_1)**2)
    

def path_count(board, square_1, square_2):
    visited = set(get_moves(board, square_1))
    frontier = list(visited)
    near_square_2 = set(get_moves(board, square_2))
    
    count = 0
    while True:
        new_frontier = []
        for square in frontier:
            if square in near_square_2:
                count += 1
                if count >= 4:
                    return count
            new_frontier.extend(get_moves(board, square))
        
#        print('count: {}, frontier: {}'.format(count, frontier))
        frontier = [x for x in new_frontier if x not in visited]
        visited |= set(frontier)
        if not frontier:
            break
        
    return count

def player_distance_score(board, player):
    current_square_player = board.get_player_location(player)
    current_square_opponent = board.get_player_location(board.get_opponent(player))
    same_color = is_same_color(current_square_player, current_square_opponent)
    
def distance(board, square_1, square_2):
    if is_distance_1(square_1, square_2):
        return 1
    
    squares_1 = {square_1}
    squares_2 = {square_2}
    
    for count in range(1, board.width * board.height):
        if count % 2:
            squares_1, increased = add_distance_1_squares(board, squares_1)
            if not increased:
                return -1
        else:
            squares_2, increased = add_distance_1_squares(board, squares_2)
            if not increased:
                return -1
        
#        print('count: {}, squares_1: {}, squares_2: {}'.format(count, squares_1, squares_2))
        
        if squares_1.intersection(squares_2):
#            print('intersection found: {}, returning {}'.format(squares_1.intersection(squares_2), count))
            return count
    
    raise RuntimeError('could not calculate distance from ' + str(square_1) + ' to ' + str(square_2))

def add_distance_1_squares(board, square_set):
    current_size = len(square_set)
    new_square_set = set(square_set)
    for square in square_set:
        new_square_set.update(get_moves(board, square))
#        print('added squares: {} -> {}'.format(square_set, new_square_set))
        
    increased = len(new_square_set) > current_size
    return new_square_set, increased

def is_distance_1(square_1, square_2):
    row, col = square_1
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    for row_dir, col_dir in directions:
        if (row + row_dir, col + col_dir) == square_2:
            return True
        
    return False
    
def is_same_color(square_1, square_2):
    return is_dark_square(square_1) == is_dark_square(square_2)

def is_dark_square(square):
    return (square[0] + square[1]) % 2    

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

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
    
    current_square_player = game.get_player_location(player)
    visited_squares_player = {current_square_player}
    depth = 5
#    print('looking for squares from ' + str(current_square_player) + ' (depth ' + str(depth) + ')')
    visit_squares(game, current_square_player, visited_squares_player, depth)
#    print('squares found: ' + str(visited_squares_player))
    
    current_square_opponent = game.get_player_location(game.get_opponent(player))
    visited_squares_opponent = {current_square_opponent}
    visit_squares(game, current_square_opponent, visited_squares_opponent, depth)
    
    return len(visited_squares_player) - len(visited_squares_opponent)
    
def visit_squares(game, square, visited, depth):
    new_squares = set(get_moves(game, square)) - visited
#    print('visited so far: ' + str(visited) + ', current square: ' + str(square) + ', new squares found: ' + str(new_squares) + ', remaining depth: ' + str(depth))
    visited.update(new_squares)
    if depth == 1:
        return
    
    for next_square in new_squares:
        visit_squares(game, next_square, visited, depth - 1)
     
def get_moves(board, square):
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

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

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
    # TODO: finish this function!
    raise NotImplementedError


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
    def __init__(self, search_depth=3, score_fn=improved_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

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

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

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

        # TODO: finish this function!
        #raise NotImplementedError
        start_time = time.time()
        
        (score, move) = self.max_value(game, depth)
        
#        print('best move: ' + str(game.get_player_location(game.active_player)) + ' -> ' + str(move))
        end_time = time.time()
#        print('execution time for minimax: ' + str(end_time - start_time) + ' sec')
        return move
    
    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        active_player = game.active_player
        if depth == 0 or game.is_loser(active_player):
            return (self.score(game, active_player), None)
        
        moves = game.get_legal_moves()
        best_score = float("-inf")
        best_move = moves[0] if moves else None
        for move in moves:
            after_move = game.forecast_move(move)
#            print('evaluating player 1 move ' + str(move))
            (score, min_move) = self.min_value(after_move, depth - 1)
            if score > best_score:
#                print('adjusting max score for depth ' + str(depth) + ': ' + str(best_score) + ' -> ' + str(score))
#                print('current best max move for depth ' + str(depth) + ': ' + str(game.get_player_location(active_player)) + ' -> ' + str(move))
                best_score = score
                best_move = move
        
#        print('best max move for depth ' + str(depth) + ': ' + str(game.get_player_location(active_player)) + ' -> ' + str(best_move) + ' - score ' + str(best_score))
        return (best_score, best_move)
        
    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        active_player = game.active_player
        if depth == 0 or game.is_loser(active_player):
            return (-self.score(game, active_player), None)
        
        moves = game.get_legal_moves()
        best_score = float("inf")
        best_move = moves[0] if moves else None
        for move in moves:
            after_move = game.forecast_move(move)
#            print('evaluating player 2 move ' + str(move))
            (score, max_move) = self.max_value(after_move, depth - 1)
            if score < best_score:
#                print('adjusting min score for depth ' + str(depth) + ': ' + str(best_score) + ' -> ' + str(score))
#                print('current best min move for depth ' + str(depth) + ': ' + str(game.get_player_location(active_player)) + ' -> ' + str(move))
                best_score = score
                best_move = move
        
#        print('best min move for depth ' + str(depth) + ': ' + str(game.get_player_location(active_player)) + ' -> ' + str(best_move) + ' - score ' + str(best_score))
        return (best_score, best_move)
    

class AlphaBetaPlayer(IsolationPlayer):
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
        # TODO: finish this function!
#        print('finding move for player {}'.format(game.active_player))
        current_square_player = game.get_player_location(game.active_player)
        current_square_opponent = game.get_player_location(game.inactive_player)
#        print('paths from player 1 to player 2 after move {}: {}'.format(game.move_count,
#              path_count(game, current_square_player, current_square_opponent)))
        
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
#                    print('no more moves for depth ' + str(depth))
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
#            print('raising timeout: time left is ' + str(self.time_left()))
            raise SearchTimeout()

        start_time = time.time()
        score, path = self.max_value(game, depth, preferred_path, alpha, beta)
        end_time = time.time()
#        print('execution time for alphabeta: ' + str((end_time - start_time) * 1000) + ' ms')
        return path
        
    def max_value(self, game, depth, preferred_path, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
#            print('raising timeout: time left is ' + str(self.time_left()))
            raise SearchTimeout()
        
        active_player = game.active_player
        if depth == 0 or game.is_loser(active_player):
            return (self.score(game, active_player), [])
        
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
                    # beta is what the minimizing player can have at least. If the maximizing player can have more
                    # than beta here, we can skip the rest of the subbranch. The whole branch will not be chosen.
#                    print('beta pruning after checking {}/{} moves'.format(count, len(moves)))
                    return (best_score, best_path)
                
#                print('no beta pruning')
                alpha = max(alpha, best_score)
        
        return (best_score, best_path)

    def min_value(self, game, depth, preferred_path, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
#            print('raising timeout: time left is ' + str(self.time_left()))
            raise SearchTimeout()
        
        active_player = game.active_player
        if depth == 0 or game.is_loser(active_player):
            return (-self.score(game, active_player), [])
        
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
#                    print('alpha pruning after checking {}/{} moves'.format(count, len(moves)))
                    return (best_score, best_path)
                
#                print('no alpha pruning')
#                if best_score < beta:
#                    print('updating beta: {} -> {}'.format(beta, best_score))
                beta = min(beta, best_score)
        
        return (best_score, best_path)      
    
    def __str__(self):
        return type(self).__name__ + '|' + str(self.score.__name__)
