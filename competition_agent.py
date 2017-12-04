"""Implement your own custom search agent using any combination of techniques
you choose.  This agent will compete against other students (and past
champions) in a tournament.

         COMPLETING AND SUBMITTING A COMPETITION AGENT IS OPTIONAL
"""
import random
import math
import game_agent
import sample_players
import isolation
from copy import copy

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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
    raise NotImplementedError


class MonteCarloPlayer(game_agent.IsolationPlayer):
    
    EXPLORATION_PARAM = math.sqrt(2)
    expand_player_1 = sample_players.RandomPlayer()
    expand_player_2 = sample_players.RandomPlayer()
    playout_player_1 = sample_players.RandomPlayer()
    playout_player_2 = sample_players.RandomPlayer()
    
    def __init__(self):
        self.root = None
        self.frontier = []
        super(MonteCarloPlayer, self).__init__()
    
    def update_root(self, new_root):
        new_root.parent = None
        self.root = new_root
        
        count = len(self.frontier)
        for frontier_node in self.frontier:
            if not self.is_ancestor(new_root, frontier_node):
                self.frontier.remove(frontier_node)
        
        print('updated root: {}'.format(self.root))
        print('updated frontier: {} -> {}'.format(count, len(self.frontier)))
        
    def is_ancestor(self, ancestor, node):
        if not node.parent:
            return False
        return node.parent == ancestor or self.is_ancestor(ancestor, node.parent)
        
    def get_move(self, board, time_left):
#        time_millis = lambda: 1000 * timeit.default_timer()
#        move_start = time_millis()
#        self.time_left = lambda : move_start + 150 - time_millis()
        
        self.time_left = time_left
        
        self.root = MonteCarloPosition(board, None)
        self.frontier = [self.root]
        
        try:
            while True:
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
                
                node = self.select_next_node()
                print('root eval is {}/{}, selected next node: {}, time left: {}'.format(
                        self.root.wins, self.root.simulations, node, self.time_left()))
                new_nodes = self.expand_node(node)
#                print('created new nodes: {}'.format(new_nodes))
                
                for new_node in new_nodes:
                    is_win = self.simulate(new_node)
#                    print('player won: {}'.format(is_win))
                    self.propagate_back(new_node, is_win)

        except SearchTimeout:
            print('timeout caught')
            pass
        
        move = self.do_move()
        print('selected move: {}'.format(move))
        return move
     
    def do_move(self):
        best_child = None
        max_value = -1
        for child in self.root.children:
            value = child.wins / child.simulations
            if value > max_value:
                max_value = value
                best_child = child
                
        print('selected child position: {}'.format(best_child))
        self.update_root(best_child)
        return best_child.move
    
    def uct(self, node):
        if not node.simulations:
            return float('inf')
        if not node.board.get_legal_moves():
#            print('end position found:\n{}'.format(node.board.to_string()))
            return 0
        
        exploitation = node.wins / node.simulations
        exploration = self.EXPLORATION_PARAM * math.sqrt(math.log(self.root.simulations) / node.simulations)
        return exploitation + exploration
    
    def select_next_node(self):
        if not self.frontier:
            raise Exception('frontier is empty - root: ' + str(self.root))
        
        max_utc = -1
        next_node = None
        for node in self.frontier:
            utc = self.uct(node)
            if utc > max_utc:
                max_utc = utc
                next_node = node
                
        return next_node

    def expand_node(self, node):
        moves = node.board.get_legal_moves()
        if not moves:
            raise Exception('no legal moves from node ' + str(node))
        new_nodes = []
        for move in moves:
            new_board = node.board.forecast_move(move)
            new_node = MonteCarloPosition(new_board, move, node)
            new_nodes.append(new_node)
            node.add_child(new_node)
            
        self.frontier.remove(node)
        self.frontier.extend(new_nodes)
        
#        expand_board = self.copy_board(node.board, self.expand_player_1, self.expand_player_2)
#        move = expand_board.active_player.get_move(expand_board, 10)
#        if move == (-1, -1):
#            print('could not expand board:\n{}'.format(expand_board.to_string()))
#            print('hmmm')
#        expand_board.apply_move(move)
#        new_node = MonteCarloPosition(expand_board, move, node)
#        self.frontier.append(new_node)
#        
#        if all(item[2] == 0 for child in node.children)
#        self.frontier.remove(node)
        
        return new_nodes
        
    def simulate(self, node):
        playout_board = self.copy_board(node.board, self.playout_player_1, self.playout_player_2)
        active_player = playout_board.active_player
        winner, history, outcome = playout_board.play(10)
        return winner == active_player
        
    def propagate_back(self, node, is_win):
        current_node = node
        while current_node:
#            print('propagating back for pos {}, win: {}'.format(position, is_win))
            current_node.simulations += 1
            if is_win:
                current_node.wins += 1
            current_node = current_node.parent
            is_win = not is_win
            
    def copy_board(self, board, player_1, player_2):
        new_board = isolation.Board(player_1, player_2)
        new_board.move_count = board.move_count
        new_board._board_state = copy(board._board_state)
        
        if new_board.move_count % 2:
            new_board._active_player = player_2
            new_board._inactive_player = player_1
        
        return new_board        
            
class MonteCarloPosition:
    def __init__(self, board, last_move, parent = None):
        self.board = board
        self.move = last_move
        self.parent = parent
        self.children = []
        self.simulations = 0
        self.wins = 0
        
    def add_child(self, child):
        self.children.append(child)
        
    def __repr__(self):
        path = []
        node = self
        while node and node.move:
            path = [node.move] + path
            node = node.parent
        return 'path={}, value={}/{}'.format(path, self.wins, self.simulations)
        

class CustomPlayer:
    """Game-playing agent to use in the optional player vs player Isolation
    competition.

    You must at least implement the get_move() method and a search function
    to complete this class, but you may use any of the techniques discussed
    in lecture or elsewhere on the web -- opening books, MCTS, etc.

    **************************************************************************
          THIS CLASS IS OPTIONAL -- IT IS ONLY USED IN THE ISOLATION PvP
        COMPETITION.  IT IS NOT REQUIRED FOR THE ISOLATION PROJECT REVIEW.
    **************************************************************************

    Parameters
    ----------
    data : string
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted.  Note that
        the PvP competition uses more accurate timers that are not cross-
        platform compatible, so a limit of 1ms (vs 10ms for the other classes)
        is generally sufficient.
    """

    def __init__(self, data=None, timeout=1.):
        self.score = custom_score
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
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
        # OPTIONAL: Finish this function!
        raise NotImplementedError
