# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent
# Team: AIH1
# Author: He Shen, Lanruo Su

from referee.game import PlayerColor, Action, PlaceAction, board
from .utils import heuristic, generate_successor_actions
from .transposition_table import TranspositionTable

import random

class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """

        # Record the color of the agent
        self._color = color
        match color:
            case PlayerColor.RED:
                print("RED Agent: I am playing as RED")
            case PlayerColor.BLUE:
                print("BLUE Agent: I am playing as BLUE")

        # Establish the board state
        self.board = board.Board()

        # Set the initial max depth
        self.max_depth = 1

        # Initialize transposition table
        self.transposition_table = TranspositionTable()

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        # Set opponent's color
        match self._color:
            case PlayerColor.RED:
                opponent = PlayerColor.BLUE
            case PlayerColor.BLUE:
                opponent = PlayerColor.RED

        # Generate possible action list
        actions = generate_successor_actions(self.board, self._color)
        best_actions = []
        best_action_score = float("-inf")

        # Dynamic distributing depth
        if 50 <= self.board.turn_count < 100:
            self.max_depth = 2
        elif 100 <= self.board.turn_count < 150:
            self.max_depth = 3

        # Find optimal action
        for action in actions:

            # Calculate the score of the action
            self.board.apply_action(action)
            action_score = self.search(1, opponent, float("-inf"), float("inf"), actions)
            self.board.undo_action()

            # Update the best action
            if action_score > best_action_score:
                best_actions = [action]
                best_action_score = action_score
            elif action_score == best_action_score:
                best_actions.append(action)
        
        # Return place action
        return random.choice(best_actions)
    
    def search(
            self, 
            depth: int, 
            color: PlayerColor,
            alpha: float,
            beta: float,
            prev_actions: list[Action]
            ) -> float:
        
        """
        This method is a recursive search algorithm that implements the minimax
        algorithm with alpha-beta pruning. It should return the score of the
        action given the current board state.
        """

        # Generate current board state hash
        board_hash = self.transposition_table.generate_hash(self.board._state)
        lookup_result = self.transposition_table.lookup(board_hash, depth)

        # Look up transposition table
        if lookup_result:
            print(lookup_result)
            return lookup_result
        
        # Set opponent's color
        match self._color:
            case PlayerColor.RED:
                opponent = PlayerColor.BLUE
            case PlayerColor.BLUE:
                opponent = PlayerColor.RED

        # Generate possible action list
        actions = generate_successor_actions(self.board, color)

        # Check if the game is over
        if self.board.winner_color == self._color:
            return float("inf")
        elif self.board.winner_color == opponent:
            return float("-inf")
        
        # Check if the search depth is reached
        if depth == self.max_depth:
            return heuristic(self._color, actions, color, prev_actions)

        # Minimax with alpha-beta pruning
        if color == self._color:
            for action in actions:

                # Apply the action to the board
                self.board.apply_action(action)
                score = self.search(depth + 1, opponent, alpha, beta, actions)
                self.board.undo_action()

                # Update alpha
                alpha = max(alpha, score)

                # Prune the search tree
                if alpha >= beta:
                    return alpha
                
            # Record current board into table
            self.transposition_table.store(board_hash, depth, alpha)
        else:
            for action in actions:

                # Apply the action to the board
                self.board.apply_action(action)
                score = self.search(depth + 1, self._color, alpha, beta, actions)
                self.board.undo_action()

                # Update beta
                beta = min(beta, score)

                # Prune the search tree
                if beta <= alpha:
                    return beta
                
            # Record current board into table
            self.transposition_table.store(board_hash, depth, beta)
                
        return alpha if color == self._color else beta

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        # Update applying the action to the board
        self.board.apply_action(action)

        # Display placing log
        print(f"{self._color} Agent acknowledged: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")
