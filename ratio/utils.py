# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent
# Team: AIH1
# Author: He Shen, Lanruo Su
# Description: Functions written in A1 with some modifications

from referee.game import PlayerColor, Action, PlaceAction, Coord

import random


def generate_random_action(
        board_size = 11
        ) -> Action:
    
    # Generate a random action
    base_coord = Coord(random.randint(0, board_size-1), 
                       random.randint(0, board_size-1))
    all_tetrominos = get_all_tetrominoes(base_coord)
    shape, tetromino_coords = random.choice(all_tetrominos)
    action = PlaceAction(*tetromino_coords)

    return action


def generate_successor_actions(
        board: dict, 
        color: PlayerColor,
        board_size = 11
        ) -> list:
    
    successors = []
    total_count = 0
    valid_count = 0

    # Generate all possible tetrominos
    if board.turn_count < 2:
        # Random generate in first turn
        is_valid = False
        while not is_valid:
            action = generate_random_action()
            for coord in action.coords:
                if board[coord].player == None:
                    is_valid = True
                else:
                    is_valid = False
                    break
        total_count += 1
        valid_count += 1
        successors.append(action)
    else:
        for x in range(board_size):
            for y in range(board_size):
                base_coord = Coord(x, y)
                all_tetrominos = get_all_tetrominoes(base_coord)
                for shape, tetromino_coords in all_tetrominos:
                    action = PlaceAction(*tetromino_coords)
                    if is_valid_place_action(board, action, color):
                        successors.append(action)
                        valid_count += 1
                    total_count += 1
                    
    return successors, valid_count / total_count


def adjust_coord(r, c):

    # Adjust row to fit the board
    if r < 0:
        r += 11
    elif r >= 11:
        r -= 11

    # Adjust column to fit the board
    if c < 0:
        c += 11
    elif c >= 11:
        c -= 11
        
    return r, c


def get_all_tetrominoes(base_coord: Coord) -> list:

    # Define tetromino shapes
    tetrominoes = []
    shapes = {
        "I": [((0, 0), (1, 0), (2, 0), (3, 0)), ((0, 0), (0, 1), (0, 2), (0, 3))],
        "O": [((0, 0), (0, 1), (1, 0), (1, 1))],
        "T": [
            ((0, 0), (0, 1), (0, 2), (1, 1)),
            ((0, 0), (1, 0), (2, 0), (1, -1)),
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

    # Append all shapes of tetrominoes
    for shape, rotations in shapes.items():
        for rotation in rotations:
            adjusted_coords = []
            for dr, dy in rotation:
                r, c = adjust_coord(base_coord.r + dr, base_coord.c + dy)
                adjusted_coords.append(Coord(r, c))
            tetrominoes.append((shape, adjusted_coords))

    return tetrominoes


def is_valid_place_action(
        board: dict[Coord, PlayerColor], 
        action: PlaceAction,
        color: PlayerColor
        ) -> bool:
    
    # Check if the action is valid
    for coord in action.coords:
        if board[coord].player != None:
            return False

    # Check if the action is adjacent to current color
    if board:  
        adjacent_to = False
        for coord in action.coords:
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = adjust_coord(coord.r + dr, coord.c + dc)
                neighbor = Coord(nr, nc)
                if board[neighbor].player == color:
                    adjacent_to = True
                    return adjacent_to

    return adjacent_to
