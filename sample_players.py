"""This file contains a collection of player classes for comparison with your
own agent and example heuristic functions.

    ************************************************************************
    ***********  YOU DO NOT NEED TO MODIFY ANYTHING IN THIS FILE  **********
    ******************************2******************************************
"""

import random
import game_agent
import alphabeta_improved
import opening_player
import mixed_player
import math
import isolation

def null_score(game, player):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return 0.


def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


def improved_score(game, player):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


def center_score(game, player):
    """Outputs a score equal to square of the distance from the center of the
    board to the position of the player.

    This heuristic is only used by the autograder for testing.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    return float((h - y)**2 + (w - x)**2)

def custom_score_1(game, player):
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')
    
    move_score = len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.get_opponent(player)))
#    distance_score = distance(game.get_player_location(player), game.get_player_location(game.get_opponent(player)))
    path_score = path_count(game, game.get_player_location(player), game.get_player_location(game.get_opponent(player)))  
    
    if not is_same_color(game.get_player_location(player), game.get_player_location(game.get_opponent(player))):
        path_score = - path_score
#        
    return move_score + path_score
#    return 0.
  
def is_same_color(square_1, square_2):
    return is_dark_square(square_1) == is_dark_square(square_2)

def is_dark_square(square):
    return (square[0] + square[1]) % 2     

    #    current_square_player = game.get_player_location(player)
#    current_square_opponent = game.get_player_location(game.get_opponent(player))

def distance(square_1, square_2):
    row_1, col_1 = square_1
    row_2, col_2 = square_2
    return math.sqrt(float((row_2 - row_1)**2 + (col_2 - col_1)**2))

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

class RandomPlayer():
    """Player that chooses a move randomly."""

    def get_move(self, game, time_left):
        """Randomly select a move from the available legal moves.

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
        ----------
        (int, int)
            A randomly selected legal move; may return (-1, -1) if there are
            no available legal moves.
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        return legal_moves[randint(0, len(legal_moves) - 1)]


class GreedyPlayer():
    """Player that chooses next move to maximize heuristic score. This is
    equivalent to a minimax search agent with a search depth of one.
    """

    def __init__(self, score_fn=open_move_score):
        self.score = score_fn

    def get_move(self, game, time_left):
        """Select the move from the available legal moves with the highest
        heuristic score.

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
        ----------
        (int, int)
            The move in the legal moves list with the highest heuristic score
            for the current game state; may return (-1, -1) if there are no
            legal moves.
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        _, move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])
        return move


class HumanPlayer():
    """Player that chooses a move according to user's input."""

    def get_move(self, game, time_left):
        """
        Select a move from the available legal moves based on user input at the
        terminal.

        **********************************************************************
        NOTE: If testing with this player, remember to disable move timeout in
              the call to `Board.play()`.
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
        ----------
        (int, int)
            The move in the legal moves list selected by the user through the
            terminal prompt; automatically return (-1, -1) if there are no
            legal moves
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        print(game.to_string()) #display the board for the human player
        print(('\t'.join(['[%d] %s' % (i, str(move)) for i, move in enumerate(legal_moves)])))

        valid_choice = False
        while not valid_choice:
            try:
                index = int(input('Select move index:'))
                valid_choice = 0 <= index < len(legal_moves)

                if not valid_choice:
                    print('Illegal move! Try again.')

            except ValueError:
                print('Invalid index! Try again.')

        return legal_moves[index]
    
    def __str__(self):
        return type(self).__name__


def play_match(player_1, player_2, rounds):
    games = []
    wins = {player_1: 0, player_2: 0}
    timeouts = 0
    forfeits = 0
    
    for round in range(rounds):
        game = Board(player_1, player_2)
        
#        game.apply_moves([(3, 5), (4, 0), (4, 3), (2, 1), (2, 2), (4, 2), (4, 1), (6, 3), (3, 3), (5, 1), (5, 2), (3, 2), (3, 1), (1, 3)])
#        game.apply_moves([(6, 0), (5, 5), (5, 2), (3, 4), (4, 4), (1, 5), (3, 6), (2, 3), (2, 4), (1, 1), (0, 3), (3, 2), (2, 2)])
#        history = game.move_history
#        print('starting game from position after {}'.format(history))
        
#        [(4, 1), (1, 4), (3, 3), (2, 2), (2, 1), (0, 3), (1, 3), (1, 1), (3, 2), (3, 0), (4, 0), (5, 1), (5, 2), (6, 3), (4, 4), (5, 5)] 
        
        move_1 = random.choice(game.get_legal_moves())
        game.apply_move(move_1)
        move_2 = random.choice(game.get_legal_moves())
        
        while not is_same_color(move_1, move_2):
            move_2 = random.choice(game.get_legal_moves())
            
        game.apply_move(move_2)
#     
        winner, move_history, termination = game.play(time_limit=300000)
        wins[winner] += 1
        
        if winner != player_1:
            print('player 2 ({}) won unexpectedly:\n{}\n{}\n'.format(winner, game.to_string(), move_history))
#        print('winner: {}\n{}\n{}\n'.format(winner, game.to_string(), move_history))
    
        if termination == "timeout":
            timeouts += 1
        elif termination == "forfeit":
            forfeits += 1
            print('\nforfeited game:\n{}\n{}'.format(game.to_string(), move_history))
            
    print('Match result {} - {}: {}:{}'.format(player_1, player_2, wins[player_1], wins[player_2]))
    
#    game = Board(player_1, player_2)
#
#    game.apply_move((2, 3))
#    game.apply_move((0, 5))
#    print(game.to_string())
#
#    winner, history, outcome = game.play(time_limit=60000)
#    who = 'Player ' + ('1' if winner == player_1 else '2')
#    print("\nWinner: {} - {}\nOutcome: {}".format(who, winner, outcome))
#    print(game.to_string())
#    print("Move history:\n{!s}".format(history))
    

if __name__ == "__main__":
    from isolation import Board

    # create an isolation board (by default 7x7)
#    player_2 = game_agent.AlphaBetaPlayer()
    player_1 = opening_player.OpeningPlayer()
#    player_2 = mixed_player.MixedPlayer()
#    player_1 = alphabeta_improved.AdvantageAwareAlphaBetaPlayer()
#    player2 = game_agent.MinimaxPlayer()
#    player2 = HumanPlayer()
    player_2 = game_agent.AlphaBetaPlayer(score_fn=improved_score)
#    player2 = monte_carlo_player.MonteCarloPlayer()
    
    try:
        play_match(player_1, player_2, 1)
        
    except mixed_player.PlayoutException:
        pass