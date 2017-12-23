
import game_agent

def custom_score_advantage_aware(game, player):
    if game.is_winner(player):
        return float('inf')
    if game.is_loser(player):
        return float('-inf')

    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(game.get_opponent(player))
    
    if bool(set(player_moves) & set(opponent_moves)):
        distance_score = 1
#        print('dist plus - player: {}, opp: {}'.format(game.get_player_location(player), game.get_player_location(game.get_opponent(player))))
#    elif is_move_distance(game.get_player_location(player), game.get_player_location(game.get_opponent(player))):
#        distance_score = -1
#        print('dist minus - player: {}, opp: {}'.format(game.get_player_location(player), game.get_player_location(game.get_opponent(player))))
    else:
        distance_score = 0
        
    score = len(player_moves) - len(opponent_moves) + 3 * distance_score
#    print('score: player - opp + 2 * dist = {} - {} + 2 * {} = {} (player: {}, opp: {}'.format(len(player_moves), len(opponent_moves), distance_score, score, game.get_player_location(player), game.get_player_location(game.get_opponent(player))))                
    return score

def is_move_distance(square_1, square_2):
    row_1, col_1 = square_1
    row_2, col_2 = square_2
    return (abs(row_1 - row_2) == 1 and abs(col_1 - col_2) == 2) or (abs(row_1 - row_2) == 2 and abs(col_1 - col_2) == 1)

class AdvantageAwareAlphaBetaPlayer(game_agent.AlphaBetaPlayer):
    
    def get_move(self, board, time_left):
        self.score = custom_score_advantage_aware
        
        return game_agent.AlphaBetaPlayer.get_move(self, board, time_left)
    
    def __str__(self):
       return type(self).__name__  