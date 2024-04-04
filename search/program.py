# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress
# Authors: He Shen, Lanruo Su

from .core import PlayerColor, Coord, PlaceAction, Direction
from .utils import render_board
from queue import PriorityQueue

def get_heuristic(
        coord1: Coord, coord2: Coord
        ) -> int:
    
    # Use manhattan distance as heuristic for goal cost
    return abs(coord1.r - coord2.r) + abs(coord1.c - coord2.c)

def find_empty_neighbors(
        board: dict[Coord, PlayerColor],
        ) -> set[Coord]:
    
    empty_neighbors = set()

    for coord, color in board.items():
        if color == PlayerColor.RED:
            # Check neighbors of red pieces
            for direction in [Direction.Up, Direction.Down, Direction.Left, Direction.Right]:
                # Get neighbor coordinate
                neighbor = coord + direction.value
                # Record if neighbor is empty
                if neighbor not in board or board.get(neighbor) not in [PlayerColor.RED, PlayerColor.BLUE]:
                    empty_neighbors.add(neighbor)

    return empty_neighbors

def find_nearest_to_blue_target(
        board: dict[Coord, PlayerColor],
        empty_neighbors: set[Coord],
        target: Coord,
        get_heuristic) -> Coord | None:
    
    # Neighbors are empty
    if not empty_neighbors:
        return None
    
    # Find the nearest empty neighbor to the target
    neighbors_with_cost = [(neighbor, get_heuristic(neighbor, target)) for neighbor in empty_neighbors]
    
    # Sort neighbors by cost
    sorted_neighbors = sorted(neighbors_with_cost, key=lambda x: x[1])

    return [coord for coord, cost in sorted_neighbors]

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

    # Step 1: Find empty neighbors of red pieces
    empty_neighbors = find_empty_neighbors(board)
    print(empty_neighbors)
    
    # Step 2: Find the nearest empty neighbor to the target
    nearest_coord = find_nearest_to_blue_target(board, 
                                                 empty_neighbors, 
                                                 target, 
                                                 get_heuristic)
    print(nearest_coord)

    # Step 3: Generate place actions
    

    # Sample "hardcoded" actions
    # return [
    #     PlaceAction(Coord(2, 5), Coord(2, 6), Coord(3, 6), Coord(3, 7)),
    #     PlaceAction(Coord(1, 8), Coord(2, 8), Coord(3, 8), Coord(4, 8)),
    #     PlaceAction(Coord(5, 8), Coord(6, 8), Coord(7, 8), Coord(8, 8)),
    # ]
    # Return `None` when no place actions are possible
    return None
