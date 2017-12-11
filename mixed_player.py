import game_agent
import alphabeta_improved

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
            return self.autoplayer.get_move(game, time_left)
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