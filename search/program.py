# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress
# Authors: He Shen, Lanruo Su

from .core import PlayerColor, Coord, PlaceAction, Direction
from .utils import render_board
from queue import PriorityQueue

def get_heuristic(
        coord1: Coord, 
        coord2: Coord
        ) -> int:
    
    # Use manhattan distance as heuristic for goal cost
    distance = abs(coord1.r - coord2.r) + abs(coord1.c - coord2.c)
    return distance

def sort_reds_by_distance(
        board: dict[Coord, PlayerColor],
        target: Coord
        ) -> list[Coord]:
    
    # Initialize a list to store red blocks
    red_blocks = []

    # Iterate over all board positions
    for coord, player in board.items():
        # If the block is red
        if player == PlayerColor.RED:
            # Append the coordinate to the list
            red_blocks.append(coord)

    # Sort the list by Manhattan distance to the target
    red_blocks.sort(key=lambda coord: get_heuristic(coord, target))

    return red_blocks

def get_neighbors(
        coord: Coord, 
        board: dict[Coord, PlayerColor], 
        goal: Coord
        ) -> list[Coord]:
    
    # Accessible neighbors of a given coordinate.
    neighbors = []
    for direction in [Direction.Up, 
                      Direction.Down, 
                      Direction.Left, 
                      Direction.Right]:
        
        next_coord = coord + direction

        # Only consider empty cells or goal as valid
        if board.get(next_coord, None) == None or next_coord == goal:
            neighbors.append(next_coord)

    return neighbors

def reconstruct_path(came_from, 
                     start, 
                     goal):
    
    # Reconstruct a path from start to goal by backtracking
    current = goal
    path = [current]

    while current != start:
        current = came_from[current]
        path.append(current)

    path.reverse()

    return path

def a_star_search(board: dict[Coord, PlayerColor], 
                  start: Coord, 
                  goal: Coord
                  ) -> list[Coord] | None:
    
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: get_heuristic(start, goal)}

    while not open_set.empty():
        current = open_set.get()[1]

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return path

        for neighbor in get_neighbors(current, board, goal):
            tentative_g_score = g_score[current] + 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + get_heuristic(neighbor, goal)
                
                if not any(neighbor == item[1] for item in open_set.queue):
                    open_set.put((f_score[neighbor], neighbor))

    # No path was found
    return None

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

    # 1. Use heuristic to sort red blocks by distance to target
    red_blocks = sort_reds_by_distance(board, target)
    if not red_blocks:
        return None

    # 2. Use A* search to find the optimal path
    start = red_blocks[0]
    path = a_star_search(board, start, target)
    if path:
        print("Path found:", path)
        return path
    else:
        print("No path found")
        return None
    
    # Sample "hardcoded" actions
    # return [
    #     PlaceAction(Coord(2, 5), Coord(2, 6), Coord(3, 6), Coord(3, 7)),
    #     PlaceAction(Coord(1, 8), Coord(2, 8), Coord(3, 8), Coord(4, 8)),
    #     PlaceAction(Coord(5, 8), Coord(6, 8), Coord(7, 8), Coord(8, 8)),
    # ]
    # Return `None` when no place actions are possible
    return None
