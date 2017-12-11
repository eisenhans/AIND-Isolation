import game_agent
import alphabeta_improved
import isolation
from copy import copy

class PlayoutException(Exception):
    """Subclass base exception for code clarity. """
    pass

class MixedPlayer():
    """Player that chooses a move according to user's input."""

    def __init__(self):
#        self.autoplayer = alphabeta_improved.AdvantageAwareAlphaBetaPlayer()
        self.autoplayer = game_agent.AlphaBetaPlayer()
        self.autoplay = False

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
        if self.autoplay:
            wins = {self.autoplayer: 0, game.inactive_player: 0}
            playouts = 10
            if game.move_count % 2:
                player_1 = game.inactive_player
                player_2 = self.autoplayer
            else:
                player_1 = self.autoplayer
                player_2 = game.inactive_player
            
            for count in range(0, playouts):
                g = isolation.Board(player_1, player_2)
                g._board_state = copy(game._board_state)
                g.move_history = game.move_history
                winner, move_history, termination = g.play()
                if winner == player_2:
                    print('unexpected result in playout {}: {} wins\n{}\n{}'.format(count, winner, g.to_string(), move_history))
                    
                wins[winner] += 1
                
            print('result of {} playouts: {} - {}: {}:{}'.format(playouts, player_1, player_2, wins[player_1], wins[player_2]))
            
            raise(PlayoutException())
                
#            return None
#            return self.autoplayer.get_move(game, time_left)
        
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        print(game.to_string()) #display the board for the human player
        print(('\t'.join(['[%d] %s' % (i, str(move)) for i, move in enumerate(legal_moves)])))

        valid_choice = False
        while not valid_choice:
            try:
                index = int(input('Select move index:'))
                if index == 9:
                    self.autoplay = True
                    return self.get_move(game, time_left)
                
                valid_choice = 0 <= index < len(legal_moves)

                if not valid_choice:
                    print('Illegal move! Try again.')

            except ValueError:
                print('Invalid index! Try again.')

        return legal_moves[index]
    
    def __str__(self):
        return type(self).__name__