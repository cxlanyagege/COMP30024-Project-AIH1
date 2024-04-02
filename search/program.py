# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress
# Authors: He Shen, Lanruo Su

from .core import PlayerColor, Coord, PlaceAction, Direction
from .utils import render_board
from queue import PriorityQueue

def get_initials(
        board: dict[Coord, PlayerColor], 
        red_neighbors: set
        ) -> list[PlaceAction]:
    
    # Find all possible initial placements
    initial_placements = []

    # Append free neighbors of the existing red pieces
    for coord in red_neighbors:
        for direction in Direction:
            new_coord = coord + direction.value
            if new_coord in board:
                continue   # Skip non-empty cell
            initial_placements.append(PlaceAction(new_coord, PlayerColor.RED))

    return initial_placements

def get_neighbors(
        coord: Coord, 
        board: dict[Coord, PlayerColor]
        ) -> list[Coord]:
    
    # Generate all possible neighbors
    neighbors = []
    for direction in Direction:
        neighbor = coord + direction.value
        if neighbor in board and board[neighbor] == PlayerColor.BLUE:
            continue  # Skip blue cells
        neighbors.append(neighbor)

    return neighbors

def get_heuristic(
        coord1: Coord, coord2: Coord
        ) -> int:
    
    # Use manhattan distance as heuristic for goal cost
    return abs(coord1.r - coord2.r) + abs(coord1.c - coord2.c)

def search(
        board: dict[Coord, PlayerColor], 
        target: Coord
        ) -> list[PlaceAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        A list of "place actions" as PlaceAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, target, ansi=False))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...

    # Return `None` when no place actions are possible
    return None
