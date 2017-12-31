
from random import randint
import timeit
import math
import game_agent
import isolation
from copy import copy

def improved_score(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)

def tentative_score(game, player):
    if game.is_loser(player):
        return 0.

    if game.is_winner(player):
        return 1.

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    score = own_moves / (own_moves + opp_moves)
    
    return score

class GreedyPlayer():
    def __init__(self, score_fn=improved_score):
        self.score = score_fn

    def get_move(self, game, time_left):
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        
        if not randint(0, 7):
            return legal_moves[randint(0, len(legal_moves) - 1)]
        
        _, move = max([(improved_score(game.forecast_move(m), self), m) for m in legal_moves])
        return move

class SearchTimeout(Exception):
    pass

class MonteCarloPlayer(game_agent.IsolationPlayer):
    """An agent that implements a Monte Carlo tree search (as described in the
    Wikipedia article: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search).
    
    This approach is much weaker than alpha-beta. Some implementations details
    could certainly be improved.
    """
    PLAYOUT_MOVE_COUNT = 6
    playout_player_1 = GreedyPlayer()
    playout_player_2 = GreedyPlayer()
    
    def __init__(self, EXPLORATION_PARAM = 5):
        self.root = None
        self.frontier = []
        self.TIMER_THRESHOLD = 40.
        self.EXPLORATION_PARAM = EXPLORATION_PARAM
        super(MonteCarloPlayer, self).__init__()
    
    def update_root(self, new_root):
        new_root.parent = None
        self.root = new_root
        
        new_frontier = []
        for frontier_node in self.frontier:
            if self.is_ancestor(new_root, frontier_node):
                new_frontier.append(frontier_node)
            
        if not new_frontier:
            new_frontier.append(new_root)
            
        self.frontier = new_frontier
        
    def is_ancestor(self, ancestor, node):
        if not node:
            return False
        return node == ancestor or self.is_ancestor(ancestor, node.parent)
        
    def get_move(self, board, time_left):
        self.time_left = time_left
        
        if not board.get_legal_moves():
            return None
        
        if board.move_count <= 3:
            # a new game has started
            self.root = MonteCarloNode(board, None)
            self.frontier = [self.root]
        else:
            node = self.find_child_node(board)
            if node:
                self.update_root(node)
            else:
                # node has not been expanded yet, so just use it as the new root
                self.root = MonteCarloNode(board, None)
                self.frontier = [self.root]
                
        try:
            while True:
                self.check_time()
                
                node = self.select_next_node()
                self.check_time()
                if not node:
                    break
                
                new_nodes = self.expand_node(node)
                self.check_time()
                
                for new_node in new_nodes:
                    self.check_time()
                    score = self.simulate(new_node)
                    self.check_time()
                    self.propagate_back(new_node, score)
                    
        except SearchTimeout:
            pass
        
        best_child = self.find_best_child_node()
        if not best_child:
            print('no best child found among children {}, root: {}'.format(self.root.children, self.root))
            print('legal moves: {}'.format(board.get_legal_moves()))
            raise(RuntimeError)
        
        self.update_root(best_child)
        move = best_child.get_last_move()
#        print('I play {} -> {} (playout result {}/{})'.format(current_location, move, best_child.score, best_child.simulations))
        return move
     
    def check_time(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
    
    def find_best_child_node(self):
        best_child = self.root.children[0] if self.root.children else None
        max_value = -1
        for child in self.root.children:
            if not child.simulations:
                continue
            value = child.score / child.simulations
            if value > max_value:
                max_value = value
                best_child = child
        
#        print('selected child position: {} - {} alternatives were {}'.format(best_child, len(self.root.children), self.root.children))
        return best_child
    
    def find_child_node(self, board):
        if not self.root:
            return None
        for node in self.root.children:
            if node.board.get_player_location(node.board.inactive_player) == board.get_player_location(board.inactive_player):
                return node
        
        return None
    
    def uct(self, node):
        if not node.simulations:
            return float('inf')
        if not node.board.get_legal_moves():
            return 0
        
        exploitation = node.score / node.simulations
        exploration = self.EXPLORATION_PARAM * math.sqrt(math.log(self.root.simulations) / node.simulations)

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
        playout_board = self.create_playout_board(node.board, self.playout_player_1, self.playout_player_2)
        inactive_player = playout_board.inactive_player
        
#        winner, history, outcome, board = playout_board.play_moves(self.PLAYOUT_MOVE_COUNT)
#        return tentative_score(board, inactive_player)
        
        winner, history, outcome = playout_board.play()
        return 1 if winner == inactive_player else 0
        
    def propagate_back(self, node, score):
        current_node = node
        while current_node:
            current_node.simulations += 1
            current_node.score += score

            current_node = current_node.parent
            score = 1. - score
            
    def create_playout_board(self, board, player_1, player_2):
        playout_board = PlayoutBoard(player_1, player_2)
        playout_board.move_count = board.move_count
        playout_board._board_state = copy(board._board_state)
        
        if playout_board.move_count % 2:
            playout_board._active_player = player_2
            playout_board._inactive_player = player_1
        
        return playout_board    

    def __str__(self):
        return type(self).__name__    
            
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
 
class PlayoutBoard(isolation.Board):
    TIME_LIMIT_MILLIS = 150
    
    def play_moves(self, move_count, time_limit=TIME_LIMIT_MILLIS):
        move_history = []
        move_history.append(list(self.get_player_location(self._active_player)))
        move_history.append(list(self.get_player_location(self._inactive_player)))

        time_millis = lambda: 1000 * timeit.default_timer()

        while len(move_history) < move_count * 2:
            legal_player_moves = self.get_legal_moves()
            game_copy = self.copy()

            move_start = time_millis()
            time_left = lambda : time_limit - (time_millis() - move_start)
            curr_move = self._active_player.get_move(game_copy, time_left)
            move_end = time_left()

            if curr_move is None:
                curr_move = isolation.Board.NOT_MOVED

            if move_end < 0:
                return self._inactive_player, move_history, "timeout", self

            if curr_move not in legal_player_moves:
                if len(legal_player_moves) > 0:
                    return self._inactive_player, move_history, "forfeit", self
                return self._inactive_player, move_history, "illegal move", self

            move_history.append(list(curr_move))

            self.apply_move(curr_move)
            
        return None, move_history, "game running", self    
        
