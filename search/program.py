# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction
from .utils import render_board
from queue import PriorityQueue
import math, time


def heuristic(target: Coord, board: dict[Coord, PlayerColor], board_size=11) -> int:
    min_distance = float("inf")
    # xx = float("inf")
    # yy = float("inf")
    pot = 0
    empty_in_row, empty_in_col = board_size, board_size

    for i in range(board_size):
        if Coord(target.r, i) in board:
            empty_in_row -= 1
        if Coord(i, target.c) in board:
            empty_in_col -= 1

    for coord, color in board.items():
        if color == PlayerColor.RED: 
            dx = min(abs(target.r - coord.r), board_size - abs(target.r - coord.r))
            dy = min(abs(target.c - coord.c), board_size - abs(target.c - coord.c))

            min_distance = min(min_distance, dx + dy)

            # txx = abs(abs(target.c - coord.c)- abs(board_size - abs(target.c - coord.c)))
            # tyy = abs(abs(target.r - coord.r)- abs(board_size - abs(target.r - coord.r)))
            # xx = min(xx, txx)
            # yy = min(yy, tyy)

    # pot = (xx + yy) / 100
    pot = (empty_in_col + empty_in_row) / 100
    # pot = (dx + dy) / 100
                
    heuristic_cost = (min(empty_in_row, empty_in_col) + min_distance) * pot
    return heuristic_cost if heuristic_cost != float("inf") else 0


def generate_successor_actions(board: dict, target:Coord, board_size=11) -> list:
    successors = []
    
    for x in range(board_size):
        for y in range(board_size):
            base_coord = Coord(x, y)
            all_tetrominos = get_all_tetrominoes(base_coord)
            for shape, tetromino_coords in all_tetrominos:
                action = PlaceAction(*tetromino_coords)
                if is_valid_place_action(board, action):
                    successors.append((shape, action))
    return successors


def adjust_coord(r, c):
    if r < 0:
        r += 11
    elif r >= 11:
        r -= 11
    if c < 0:
        c += 11
    elif c >= 11:
        c -= 11
    return r, c


def get_all_tetrominoes(base_coord: Coord) -> list:
    tetrominoes = []
    shapes = {
        "I": [((0, 0), (1, 0), (2, 0), (3, 0)), ((0, 0), (0, 1), (0, 2), (0, 3))],
        "O": [((0, 0), (0, 1), (1, 0), (1, 1))],
        "T": [
            ((0, 0), (0, 1), (0, 2), (1, 1)),
            ((0, 0), (1, 0), (2, 0), (-1, 1)),
            ((0, 0), (0, 1), (0, 2), (-1, 1)),
            ((0, 0), (1, 0), (2, 0), (1, 1)),
        ],
        "J": [
            ((0, 0), (1, 0), (2, 0), (2, -1)),
            ((0, 0), (1, 0), (2, 0), (0, 1)),
            ((0, 0), (0, 1), (0, 2), (-1, 0)),
            ((0, 0), (0, 1), (0, 2), (1, 2)),
        ],
        "L": [
            ((0, 0), (1, 0), (2, 0), (2, 1)),
            ((0, 0), (1, 0), (2, 0), (0, -1)),
            ((0, 0), (0, 1), (0, 2), (1, 0)),
            ((0, 0), (0, 1), (0, 2), (-1, 2)),
        ],
        "Z": [((0, 0), (0, 1), (1, 1), (1, 2)), ((0, 0), (0, 1), (1, 0), (-1, 1))],
        "S": [((0, 0), (0, 1), (-1, 1), (-1, 2)), ((0, 0), (0, 1), (-1, 0), (1, 1))],
    }

    for shape, rotations in shapes.items():
        for rotation in rotations:
            adjusted_coords = []
            for dr, dy in rotation:
                r, c = adjust_coord(base_coord.r + dr, base_coord.c + dy)
                adjusted_coords.append(Coord(r, c))
            tetrominoes.append((shape, adjusted_coords))

    return tetrominoes


def apply_place_action(board: dict[Coord, PlayerColor], action: PlaceAction) -> dict:
    new_board = dict(board) 

    for coord in action.coords:
        new_board[coord] = PlayerColor.RED

    rows, cols = set(), set()
    for coord in action.coords:
        rows.add(coord.r)
        cols.add(coord.c)

    for row1 in rows:
        if all(Coord(row1, col1) in new_board for col1 in range(11)):
            for col11 in range(11):
                del new_board[Coord(row1, col11)]
                # print(render_board(new_board, Coord(row1, col11), ansi=True))

    for col2 in cols:
        if all(Coord(row2, col2) in new_board for row2 in range(11)):
            for row21 in range(11):
                del new_board[Coord(row21, col2)]
                # print(render_board(new_board, Coord(row21, col2), ansi=True))

    return new_board


def is_valid_place_action(board: dict[Coord, PlayerColor], action: PlaceAction) -> bool:
    for coord in action.coords:
        if coord in board:
            return False

    if board:  
        adjacent_to_red = False
        for coord in action.coords:
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = adjust_coord(coord.r + dr, coord.c + dc)
                neighbor = Coord(nr, nc)
                if neighbor in board and board[neighbor] == PlayerColor.RED:
                    adjacent_to_red = True
                    return adjacent_to_red

    return adjacent_to_red


def search(board: dict[Coord, PlayerColor], target: Coord) -> list[PlaceAction] | None:
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
    start_time = time.time()

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...
    frontier = PriorityQueue()
    count = 0
    frontier.put(
        (0, 0, count := count + 1, [], board)
    )  
    visited = set()

    while not frontier.empty():
        total_cost, cost, _, actions, current_board = frontier.get()
        
        successors = generate_successor_actions(current_board, target)

        for shape, action in successors:
            if not is_valid_place_action(current_board, action):
                continue
            new_board = apply_place_action(current_board, action)
            # new_actions = actions + [(shape, action)]
            new_actions = actions + [action]

            if target not in new_board:
                print(render_board(new_board, target, ansi=True))
                end_time = time.time()
                total_time = end_time - start_time
                print(f"Total running time: {total_time} seconds\n")

                return new_actions

            board_state_key = frozenset(
                new_board.items()
            ) 
            if board_state_key in visited:
                continue
            visited.add(board_state_key)

            g = cost + 1 
            h_cost = heuristic(target, new_board) 
            # print(h_cost, new_actions)
            frontier.put((g + h_cost, g, count := count + 1, new_actions, new_board))

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total running time: {total_time} seconds\n")

    return None

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
