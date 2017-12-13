
import game_agent
import functools

def custom_score_advantage_aware(advantage, game, player):
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')
    
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    common_moves = set(player_moves) & set(opponent_moves)    
    
    common_score = 2 * len(common_moves)
    if not advantage:
        common_score = - common_score
    
    score = len(player_moves) - len(opponent_moves) + common_score
#    print('score: player - opp + common = {} - {} + {} = {}'.format(len(player_moves), len(opponent_moves), common_score, score))
    return score

class AdvantageAwareAlphaBetaPlayer(game_agent.AlphaBetaPlayer):
    
    def get_move(self, board, time_left):
        current_square_player = board.get_player_location(board.active_player)
        current_square_opponent = board.get_player_location(board.inactive_player)
        advantage = game_agent.is_same_color(current_square_player, current_square_opponent)
        
        self.score = functools.partial(custom_score_advantage_aware, advantage)
        
        return game_agent.AlphaBetaPlayer.get_move(self, board, time_left)
    
    def __str__(self):
       return type(self).__name__  