
from random import randint
import timeit
import math
import game_agent
import sample_players
import isolation
from copy import copy

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

def tentative_score(game, player):
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
        return 0.

    if game.is_winner(player):
        return 1.

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    score = own_moves / (own_moves + opp_moves)
#    print('player/opponent moves: {}/{}, score: {}'.format(own_moves, opp_moves, score))
    
    return score

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
    depth = 2
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

def get_moves(game, loc):
    """Generate the list of possible moves for an L-shaped motion (like a
    knight in chess).
    """
    if loc == isolation.Board.NOT_MOVED:
        return game.get_blank_spaces()

    r, c = loc
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    valid_moves = [(r + dr, c + dc) for dr, dc in directions
                   if game.move_is_legal((r + dr, c + dc))]
    
#    print('valid moves from ' + str(loc) + ': ' + str(valid_moves))
    return valid_moves    

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
        
        if not randint(0, 7):
            return legal_moves[randint(0, len(legal_moves) - 1)]
#            _, move = max([(custom_score_2(game.forecast_move(m), self), m) for m in legal_moves])
#            return move
        
        _, move = max([(improved_score(game.forecast_move(m), self), m) for m in legal_moves])
        return move

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

class MonteCarloPlayer(game_agent.IsolationPlayer):
    
    PLAYOUT_MOVE_COUNT = 6
    EXPLORATION_PARAM = 5#math.sqrt(2)
#    playout_player_1 = RandomPlayer()
#    playout_player_2 = RandomPlayer()
#    playout_player_1 = GreedyPlayer(score_fn = improved_score)
    playout_player_1 = GreedyPlayer()
    playout_player_2 = GreedyPlayer()
    
    def __init__(self):
        self.root = None
        self.frontier = []
        super(MonteCarloPlayer, self).__init__()
    
    def update_root(self, new_root):
        old_root = self.root
        
        new_root.parent = None
        self.root = new_root
        
        count = len(self.frontier)
        new_frontier = []
        for frontier_node in self.frontier:
            if self.is_ancestor(new_root, frontier_node):
                new_frontier.append(frontier_node)
#            print('keeping frontier_node {} after setting root to {}: {}'.format(frontier_node, new_root, keep))
            
        if not new_frontier:
            new_frontier.append(new_root)
            
        self.frontier = new_frontier
#        print('updated root: {} -> {}'.format(old_root, self.root))
#        print('children of new root: {}'.format(self.root.children))
#        print('updated frontier: {} -> {}'.format(count, len(self.frontier)))
        
    def is_ancestor(self, ancestor, node):
        if not node:
            return False
        return node == ancestor or self.is_ancestor(ancestor, node.parent)
        
    def get_move(self, board, time_left):
        time_millis = lambda: 1000 * timeit.default_timer()
        move_start = time_millis()
        self.time_left = lambda : move_start + 150 - time_millis()
        
#        self.time_left = time_left
        
        current_location = board.get_player_location(board.active_player)
        
        if not board.get_legal_moves():
#            print('No more legal moves - I lost')
            return None
        
        node = self.find_child_node(board)
        if node:
            self.update_root(node)
        else:
            self.root = MonteCarloNode(board, None)
            self.frontier = [self.root]
        
        print('opponent played {}, updated root node: {}'.format(
                board.get_player_location(board.inactive_player), node))
        
        try:
            while True:
                self.check_time()
                
                node = self.select_next_node()
                self.check_time()
                if not node:
#                    print('no more nodes to expand - root: {}, children: {}, frontier: {}'.format(
#                            self.root, self.root.children, self.frontier))
                    break
#                print('root is {}, selected next node: {}, time left: {}'.format(self.root, node, self.time_left()))
#                print('frontier before expansion {}'.format(self.frontier))
#                frontier_size = len(self.frontier)
                new_nodes = self.expand_node(node)
                self.check_time()
#                print('frontier after expansion {}'.format(self.frontier))
#                print('newly expanded nodes: {}'.format(new_nodes))
#                print('frontier expanded: {} -> {}, {} new nodes'.format(frontier_size, len(self.frontier), len(new_nodes)))
                
                for new_node in new_nodes:
                    self.check_time()
                    score = self.simulate(new_node)
                    self.check_time()
#                    print('player won: {}'.format(is_win))
                    self.propagate_back(new_node, score)
                    
#                print('expanded node {}, {} new nodes: {}'.format(node, len(new_nodes), new_nodes))

        except SearchTimeout:
#            print('timeout caught')
            pass
        
        best_child = self.find_best_child_node()
        self.update_root(best_child)
        move = best_child.get_last_move()
        print('I play {} -> {} (playout result {}/{})'.format(current_location, move, best_child.score, best_child.simulations))
        return move
     
    def check_time(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
    
    def find_best_child_node(self):
        best_child = None
        max_value = -1
        for child in self.root.children:
            if not child.simulations:
                continue
            value = child.score / child.simulations
            if value > max_value:
                max_value = value
                best_child = child
                
        print('selected child position: {} - {} alternatives were {}'.format(best_child, len(self.root.children), self.root.children))
        return best_child
    
    def find_child_node(self, board):
        if not self.root:
            return None
#        print('trying to find current position in one of {} child nodes'.format(len(self.root.children)))
        for node in self.root.children:
#            print('comparing boards\n{}\nand\n{}\n'.format(node.board.to_string(), board.to_string()))
            if node.board.get_player_location(board.inactive_player) == board.get_player_location(board.inactive_player):
#                print("found child node with position after opponent's move: {}".format(node))
                return node
        
#        print('board not found:\n{}'.format(board.to_string()))
        return None
    
    def uct(self, node):
        if not node.simulations:
            return float('inf')
        if not node.board.get_legal_moves():
#            print('end position found:\n{}'.format(node.board.to_string()))
            return 0
        
        exploitation = node.score / node.simulations
        exploration = self.EXPLORATION_PARAM * math.sqrt(math.log(self.root.simulations) / node.simulations)
#        print('uct for node {}: {}'.format(node, (exploitation + exploration)))
        return exploitation + exploration
    
    def select_next_node(self):
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
#        if not moves:
#            print('no more legal moves')
#            return None
        new_nodes = []
        for move in moves:
            new_board = node.board.forecast_move(move)
            new_node = MonteCarloNode(new_board, node)
            new_nodes.append(new_node)
            node.add_child(new_node)
            
        self.frontier.remove(node)
        self.frontier.extend(new_nodes)
        
        return new_nodes
        
    def simulate(self, node):
        playout_board = self.copy_board(node.board, self.playout_player_1, self.playout_player_2)
        inactive_player = playout_board.inactive_player
        winner, history, outcome, board = playout_board.play_moves(self.PLAYOUT_MOVE_COUNT, 10)
        
        return tentative_score(board, inactive_player)
        
    def propagate_back(self, node, score):
        current_node = node
        while current_node:
#            print('propagating back for pos {}, win: {}'.format(position, is_win))
            current_node.simulations += 1
            current_node.score += score
#            if is_win:
#                current_node.wins += 1
            current_node = current_node.parent
            score = 1. - score
            
    def copy_board(self, board, player_1, player_2):
        new_board = isolation.Board(player_1, player_2)
        new_board.move_count = board.move_count
        new_board._board_state = copy(board._board_state)
        
        if new_board.move_count % 2:
            new_board._active_player = player_2
            new_board._inactive_player = player_1
        
        return new_board        
            
class MonteCarloNode:
    def __init__(self, board, parent = None):
        self.board = board
        self.parent = parent
        self.children = []
        self.simulations = 0
        self.score = 0.
        
    def get_last_move(self):
        return self.board.get_player_location(self.board.inactive_player)
        
    def add_child(self, child):
        self.children.append(child)
        
    def __repr__(self):
        path = []
        node = self
        while node:
            path = [node.get_last_move()] + path
            node = node.parent
        return 'path={}, value={}/{}'.format(path, self.score, self.simulations)
        