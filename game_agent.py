"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math
import logging


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def close_game_score(game, player):
    """This heuristic assumes that a close game (less total options)
    allows the player to win the game quickly.

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

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    score = (own_moves - opp_moves) / (own_moves + opp_moves)

    return float(score)


def open_game_score(game, player):
    """This heuristic assumes that an open game (more total options)
    allows the player to get better options in the logn run and win.

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

    score = (own_moves - opp_moves) * (own_moves + opp_moves)

    return float(score)



def close_opponent_score(game, player):
    """This heuristic assumes that closing the options of the opponent
    allows the player to win.

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

    n = 4
    score = (own_moves - n * opp_moves)

    return float(score)


def custom_score(game, player):
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
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    score = (-opp_moves)

    return float(score)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)  This parameter should be ignored when iterative = True.

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).  When True, search_depth should
        be ignored and no limit to search depth.

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def config_log():
        logger = logging.getLogger("isolation_logger")
        logger.basicConfig(filename='isolation.log', filemode='w', level=logging.DEBUG)

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.best_move = (-1, -1)
        self.final_depth = 0

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

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

        legal_moves : list<(int, int)>
            DEPRECATED -- This argument will be removed in the next release

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

        best_move = (-1, -1)

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
            return best_move

        blank_spaces = game.get_blank_spaces()
        total_spaces = game.height * game.width

        if (blank_spaces == total_spaces):
            center = math.floor(game.height / 2)
            best_move = (center, center)
            return best_move

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            # my_moves = game.
            if self.iterative:
                for depth in range(1, len(blank_spaces)):
                    score, best_move = self.minimax(game, depth, True)
                    logging.info('Iterative. Current depth: ' + str(depth))
                    self.best_move = best_move
                    self.final_depth = depth
                    logging.info('Iterative for. Best move: ' + str(self.best_move))
                    logging.info('Iterative for. Depth: ' + str(self.final_depth))
                return best_move
            else:
                score, best_move = self.minimax(game, self.search_depth, True)
                return best_move
        except Timeout:
            # Handle any actions required at timeout, if necessary
            logging.info('Timeout Iterative. Best move: ' + str(self.best_move))
            logging.info('Timeout Iterative. Depth: ' + str(self.final_depth))
            return self.best_move

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        # Exit timeout condition
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Get the legal moves
        legal_moves = game.get_legal_moves()
        # Check whether there are legal moves and return the final score when none
        if not legal_moves:
            score = game.utility(game.active_player)
            move = (-1, -1)
            return score, move

        logging.debug('Maximizing player: ' + str(maximizing_player))
        logging.debug('Depth: ' + str(depth))
        depth -= 1
        # Get the values of the nodes at maximum depth
        if (0 >= depth):
            if maximizing_player:
                # Get scores for the active player and find the maximun score
                scores = [
                    self.score(game.forecast_move(legal_move), game.active_player)
                    for legal_move in legal_moves
                ]
                score = max(scores)
            else:
                # Get scores for the inactive player and find the minimun score
                scores = [
                    self.score(game.forecast_move(legal_move), game.inactive_player)
                    for legal_move in legal_moves
                ]
                score = min(scores)

            # Get the current best move
            index = scores.index(score)
            move = legal_moves[index]
            # self.best_move = move
        # Iterate recursively and toggle between max and min
        else:
            games = [game.forecast_move(legal_move) for legal_move in legal_moves]
            scores_moves = [self.minimax(game, depth, not maximizing_player) for game in games]
            logging.info('Scores moves: \n' + str(scores_moves))
            scores = [s for s, m in scores_moves]
            # Check for the max/min values returned by the nodes and find the best move
            if maximizing_player:
                score = max(scores)
            else:
                score = min(scores)
            index = scores.index(score)
            move = legal_moves[index]
            # self.best_move = move

        logging.debug('Legal moves: \n' + str(legal_moves))
        logging.debug('Scores: \n' + str(scores))
        logging.debug('Game: \n' + game.to_string())

        return score, move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

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

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Get the legal moves
        legal_moves = game.get_legal_moves()
        # Check whether there are legal moves and return the current score
        if not legal_moves:
            score = game.utility(game.active_player)
            move = (-1, -1)
            return score, move

        logging.debug('Maximizing player: ' + str(maximizing_player))
        logging.debug('Depth: ' + str(depth))

        # Iterate recursively and toggle between max and min
        if (0 < depth):
            if maximizing_player:
                best_score = float('-inf')
                best_move = (-1, -1)
                for move in legal_moves:
                    node_score, node_move = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, not maximizing_player)
                    # Update maximum score
                    if (best_score <= node_score):
                        best_score = node_score
                        best_move = move
                    # Check whether alpha must be updated with new max
                    alpha = max(alpha, best_score)
                    if (beta <= alpha):
                        break
            else:
                best_score = float('inf')
                best_move = (-1, -1)
                for move in legal_moves:
                    node_score, node_move = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta,not maximizing_player)
                    # Update minimum score
                    if (node_score <= best_score):
                        best_score = node_score
                        best_move = move
                    # Check whether beta must be updated with new min
                    beta = min(beta, best_score)
                    if (beta <= alpha):
                        break
            # Return best score and best move
            # self.best_move = best_move
            return best_score, best_move
        # Return the score and move at maximum depth
        else:
            score = self.score(game, game.active_player)
            move = game.get_player_location(game.active_player)
            return score, move

        logging.debug('Legal moves: \n' + str(legal_moves))
        logging.debug('Scores: \n' + str(scores))
        logging.debug('Game: \n' + game.to_string())

        return score, move
