from .core import Coord, PlayerColor, Direction
from queue import PriorityQueue


def get_heuristic(
        coord1: Coord, 
        coord2: Coord
        ) -> int:
    
    # Use manhattan distance as heuristic for goal cost
    distance = abs(coord1.r - coord2.r) + abs(coord1.c - coord2.c)
    return distance


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