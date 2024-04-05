# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress
# Authors: He Shen, Lanruo Su


from .core import PlayerColor, Coord, PlaceAction, Direction
from .utils import render_board
from .placements import handle_special_placement, handle_final_placement
from queue import PriorityQueue


def find_init_row_col(
        board: dict[Coord, PlayerColor], 
        target: Coord
        ) -> tuple[str, int]:
    
    row_empty_spaces = 0
    col_empty_spaces = 0
    board_size = 11

    # Count empty spaces in the target's row
    for c in range(board_size):
        if Coord(target.r, c) not in board:
            row_empty_spaces += 1

    # Count empty spaces in the target's column
    for r in range(board_size):
        if Coord(r, target.c) not in board:
            col_empty_spaces += 1

    # Determine which dimension has fewer empty spaces and return it
    if row_empty_spaces < col_empty_spaces:
        return ("row", target.r)
    else:
        return ("col", target.c)


def get_heuristic(
        coord1: Coord, 
        coord2: Coord
        ) -> int:
    
    # Use manhattan distance as heuristic for goal cost
    distance = abs(coord1.r - coord2.r) + abs(coord1.c - coord2.c)
    return distance


def sort_reds_by_distance(
        board: dict[Coord, PlayerColor],
        dimension: str, 
        position: int
        ) -> list[Coord]:
    
    empty_spaces = []
    distances = []

    # Collect empty cells in targeted row or column
    if dimension == "row":
        for c in range(11):
            if Coord(position, c) not in board:
                empty_spaces.append(Coord(position, c))
    elif dimension == "col":
        for r in range(11):
            if Coord(r, position) not in board:
                empty_spaces.append(Coord(r, position))

    # Calculate distance between red blocks and empty cells
    for coord, player in board.items():
        if player == PlayerColor.RED:

            # Count total empty cells on the row and column
            total_empty = 0
            for i in range(11):
                if Coord(i, coord.c) not in board:
                    total_empty += 1
            for j in range(11):
                if Coord(coord.r, j) not in board:
                    total_empty += 1

            # Append tuple with distance and empty cell
            for empty_space in empty_spaces:
                distance = get_heuristic(coord, empty_space)
                distances.append((coord, distance, empty_space, total_empty))

    # Sort by distance size
    distances.sort(key=lambda x: (x[1], -x[3]))

    return distances


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


def update_board(
        board: dict[Coord, PlayerColor],
        action: PlaceAction
        ):
    
    # Set Tetromino coordinates to red
    board[action.c1] = PlayerColor.RED
    board[action.c2] = PlayerColor.RED
    board[action.c3] = PlayerColor.RED
    board[action.c4] = PlayerColor.RED
  

def gen_place_actions(
        path: list[Coord], 
        board:dict[Coord, PlayerColor], 
        dim: str, 
        pos: int
        ) -> list[PlaceAction]:
    
    i = 1
    step_counter = 0
    place_actions = []
    special_actions = []
    final_actions = []

    for i in range(1, len(path) - 1):
        step_counter += 1

        # Generate 4-continuous place actions
        if step_counter % 4 == 0:
            place_actions.append(
                PlaceAction(path[i-3], path[i-2], path[i-1], path[i]))
            
            # Update board status
            update_board(board, place_actions[-1])
            
        # Stop when reaching blank edge of columm
        if dim == "col":

            # Current position is at the edge of the column
            if abs(path[i].c - pos) == 1 or abs(path[i].c - pos) == 10:

                # check if neighbor is empty or not
                if Coord(path[i].r, pos) not in board:
                    break

        # Or stop when reaching blank edge of row
        elif dim == "row":

            # Current position is at the edge of the row
            if abs(path[i].r - pos) == 1 or abs(path[i].r - pos) == 10:

                # check if neighbor is empty or not
                if Coord(pos, path[i].c) not in board:
                    break

    # Handle special placement when there are remaining steps
    if i > 1:
        special_actions = handle_special_placement(
            path[i - (step_counter % 4) + 1: i + 1],
            board,
            dim,
            pos)
        update_board(board, special_actions[-1])
        
    # Handle final placements in target row or column
    handle_final_placement()

    # Combine all placements
    place_actions = place_actions + special_actions + final_actions

    return place_actions


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
    print(render_board(board, target, ansi=True))

    # Some impressive AI stuff here to find the solution...
    
    # 1. Choose row/column with the least blank cells
    dim, pos = find_init_row_col(board, target)

    # 2. Use heuristic to sort red blocks by distance to empty cells
    red_blocks = sort_reds_by_distance(board, dim, pos)

    if not red_blocks:
        return None

    # 3. Use A* to generate path to nearest empty cell
    can_generate = False

    for red_block in red_blocks:
        start, distance, goal, total = red_block
        path = a_star_search(board, start, goal)
        if path:
            can_generate = True
            break

    if not can_generate:
        return None
    
    # 4. Place actions
    place_actions = gen_place_actions(path, board, dim, pos)

    print(render_board(board, target, ansi=True))

    if not place_actions:
        return None

    return place_actions
