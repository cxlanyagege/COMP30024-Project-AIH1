# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent
# Team: AIH1
# Author: He Shen, Lanruo Su

from referee.game import PlayerColor, Action, PlaceAction, Coord, board
from .utils import heuristic, generate_successor_actions


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
        
        # Return place action
        return actions[0]

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
