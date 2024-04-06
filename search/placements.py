# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress
# Authors: He Shen, Lanruo Su


from .core import Coord, Direction, PlayerColor, PlaceAction
from .a_star import a_star_search, get_heuristic


def handle_special_placement(
        path: list[Coord],
        board: dict[Coord, PlayerColor],
        dim: str,
        pos: int
        ) -> list[PlaceAction]:

    special_actions = []

    if len(path) == 3:

        # Perfectly horizontal
        if path[0].r == path[1].r == path[2].r:

            # Try T (1)
            if (path[1] + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Down))
        
            # Try T (3)
            elif (path[1] + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Up))
        
            # Try J (2)
            elif (path[0] + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Up))

            # Try J (4)
            elif (path[2] + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Down))

            # Try L (2)
            elif (path[0] + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Down))

            # Try L (4)
            elif (path[2] + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Up))

            # Try Z (1) Left
            elif path[2].c > path[0].c and (path[1] + Direction.Down) not in board and (path[2] + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Down, path[2] + Direction.Down))

            # Try Z (1) Right
            elif path[2].c < path[0].c and (path[1] + Direction.Up) not in board and (path[2] + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Up, path[2] + Direction.Up))

            # Try S (1) Left
            elif path[2].c > path[0].c and (path[1] + Direction.Up) not in board and (path[2] + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Up, path[2] + Direction.Up))

            # Try S (1) Right
            elif path[2].c < path[0].c and (path[1] + Direction.Down) not in board and (path[2] + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Down, path[2] + Direction.Down))

        # Perfectly vertical
        elif path[0].c == path[1].c == path[2].c:
                
            # Try T (2)
            if (path[1] + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Left))
            
            # Try T (4)
            elif (path[1] + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Right))
            
            # Try J (1)
            elif (path[0] + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Left))
    
            # Try J (3)
            elif (path[2] + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Right))
    
            # Try L (1)
            elif (path[0] + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Right))
    
            # Try L (3)
            elif (path[2] + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Left))

            # Try Z (2) Top
            elif path[2].r > path[0].r and (path[1] + Direction.Left) not in board and (path[2] + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Left, path[2] + Direction.Left))

            # Try Z (2) Bottom
            elif path[2].r < path[0].r and (path[1] + Direction.Right) not in board and (path[2] + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Right, path[2] + Direction.Right))

            # Try S (2) Top
            elif path[2].r > path[0].r and (path[1] + Direction.Right) not in board and (path[2] + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Right, path[2] + Direction.Right))

            # Try S (2) Bottom
            elif path[2].r < path[0].r and (path[1] + Direction.Left) not in board and (path[2] + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Left, path[2] + Direction.Left))

        # Has turining
        else:

            # First two are vertical
            if path[0].c == path[1].c:

                # Downward - Right
                if path[1].r - path[0].r == 1 and path[2].c - path[1].c == 1:

                    # Try O
                    if (path[0] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Right))

                    # Try T (3)
                    elif (path[1] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Left))

                    # Try T (4)
                    elif (path[1] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Down))

                    # Try J (2)
                    elif (path[2] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Right))

                    # Try L (1)
                    elif (path[0] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Up))

                    # Try Z (1)
                    elif (path[0] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Left))

                    # Try S (2)
                    elif (path[2] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Down))

                # Downward - Left
                elif path[1].r - path[0].r == 1 and path[1].c - path[0].c == 1:

                    # Try O
                    if (path[0] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Left))

                    # Try T (2)
                    elif (path[1] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Down))

                    # Try T (3)
                    elif (path[1] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Right))

                    # Try J (1)
                    elif (path[0] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Up))

                    # Try L (4)
                    elif (path[2] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Left))

                    # Try Z (2)
                    elif (path[2] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Down))

                    # Try S (1)
                    elif (path[0] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Right))

                # Upward - Right
                elif path[0].r - path[1].r == 1 and path[2].c - path[1].c == 1:

                    # Try O
                    if (path[0] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Right))

                    # Try T (1)
                    elif (path[1] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Left))

                    # Try T (4)
                    elif (path[1] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Up))

                    # Try J (3)
                    elif (path[0] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Down))

                    # Try L (2)
                    elif (path[2] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Right))

                    # Try Z (2)
                    elif (path[2] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Up))

                    # Try S (1)
                    elif (path[0] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Left))

                # Upward - Left
                elif path[0].r - path[1].r == 1 and path[1].c - path[2].c == 1:

                    # Try O
                    if (path[0] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Left))

                    # Try T (1)
                    elif (path[1] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Right))

                    # Try T (2)
                    elif (path[1] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Up))

                    # Try J (4)
                    elif (path[2] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Left))

                    # Try L (3)
                    elif (path[0] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Down))

                    # Try Z (1)
                    elif (path[0] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Right))

                    # Try S (2)
                    elif (path[2] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Up))

            # First two are horizontal
            elif path[0].r == path[1].r:
                    
                # Rightward - Down
                if path[1].c - path[0].c == 1 and path[2].r - path[1].r == 1:
    
                    # Try O
                    if (path[0] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Down))
    
                    # Try T (1)
                    elif (path[1] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Right))
    
                    # Try T (2)
                    elif (path[1] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Up))
    
                    # Try J (4)
                    elif (path[0] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Left))
    
                    # Try L (3)
                    elif (path[2] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Down))
    
                    # Try Z (1)
                    elif (path[2] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Right))
    
                    # Try S (2)
                    elif (path[0] + Direction.Up) not in board:
                            special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Up))
    
                # Rightward - Up
                elif path[1].c - path[0].c == 1 and path[1].r - path[2].r == 1:
    
                    # Try O
                    if (path[0] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Up))

                    # Try T (2)
                    elif (path[1] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Down))
    
                    # Try T (3)
                    elif (path[1] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Right))

                    # Try J (1)
                    elif (path[2] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Up))
    
                    # Try L (4)
                    elif (path[0] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Left))
    
                    # Try Z (2)
                    elif (path[0] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Down))
    
                    # Try S (1)
                    elif (path[2] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Right))

                # Leftward - Down
                elif path[0].c - path[1].c == 1 and path[2].r - path[1].r == 1:
    
                    # Try O
                    if (path[0] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Down))
    
                    # Try T (1)
                    elif (path[1] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Left))
    
                    # Try T (4)
                    elif (path[1] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Up))
    
                    # Try J (3)
                    elif (path[2] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Down))
    
                    # Try L (2)
                    elif (path[0] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Right))
    
                    # Try Z (2)
                    elif (path[0] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Up))
    
                    # Try S (1)
                    elif (path[2] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Left))

                # Leftward - Up
                elif path[0].c - path[1].c == 1 and path[1].r - path[2].r == 1:
    
                    # Try O
                    if (path[0] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Up))
    
                    # Try T (3)
                    elif (path[1] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Left))
    
                    # Try T (4)
                    elif (path[1] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[1] + Direction.Down))
    
                    # Try J (2)
                    elif (path[0] + Direction.Right) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Right))
    
                    # Try L (1)
                    elif (path[2] + Direction.Up) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Up))
    
                    # Try Z (1)
                    elif (path[2] + Direction.Left) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[2] + Direction.Left))
    
                    # Try S (2)
                    elif (path[0] + Direction.Down) not in board:
                        special_actions.append(PlaceAction(path[0], path[1], path[2], path[0] + Direction.Down))

    elif len(path) == 2:
            
        # Horizontal
        if path[0].r == path[1].r:
    
            # Try O Upper
            if (path[0] + Direction.Down) not in board and (path[1] + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[0] + Direction.Down, path[1] + Direction.Down))

            # Try O Lower
            elif (path[0] + Direction.Up) not in board and (path[1] + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[0] + Direction.Up, path[1] + Direction.Up))

            # Try T (2)
            elif path[1].c > path[0].c and (path[1] + Direction.Up) not in board and (path[1] + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Up, path[1] + Direction.Down))

            # Try T (4)
            elif path[1].c < path[0].c and (path[1] + Direction.Down) not in board and (path[1] + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Down, path[1] + Direction.Up))

            # Try J (1)
            elif path[1].c > path[0].c and (path[1] + Direction.Up) not in board and (path[1] + Direction.Up + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Up, path[1] + Direction.Up + Direction.Up))

            # Try J (3)
            elif path[1].c < path[0].c and (path[1] + Direction.Down) not in board and (path[1] + Direction.Down + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Down, path[1] + Direction.Down + Direction.Down))

            # Try L (1)
            elif path[1].c < path[0].c and (path[1] + Direction.Up) not in board and (path[1] + Direction.Up + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Up, path[1] + Direction.Up + Direction.Up))

            # Try L (3)
            elif path[1].c > path[0].c and (path[1] + Direction.Down) not in board and (path[1] + Direction.Down + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Down, path[1] + Direction.Down + Direction.Down))

            # Try Z (2)
            elif (path[0] + Direction.Down) not in board and (path[1] + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[0] + Direction.Down, path[1] + Direction.Up))

            # Try S (2)
            elif (path[0] + Direction.Up) not in board and (path[1] + Direction.Down) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[0] + Direction.Up, path[1] + Direction.Down))

        # Vertical
        elif path[0].c == path[1].c:

            # Try O Left
            if (path[0] + Direction.Right) not in board and (path[1] + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[0] + Direction.Right, path[1] + Direction.Right))

            # Try O Right
            elif (path[0] + Direction.Left) not in board and (path[1] + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[0] + Direction.Left, path[1] + Direction.Left))

            # Try T (1)
            elif path[1].r < path[0].r and (path[1] + Direction.Left) not in board and (path[1] + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Left, path[1] + Direction.Right))

            # Try T (3)
            elif path[1].r > path[0].r and (path[1] + Direction.Right) not in board and (path[1] + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Right, path[1] + Direction.Left))

            # Try J (2)
            elif path[1].r > path[0].r and (path[1] + Direction.Right) not in board and (path[1] + Direction.Right + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Right, path[1] + Direction.Right + Direction.Right))

            # Try J (4)
            elif path[1].r < path[0].r and (path[1] + Direction.Left) not in board and (path[1] + Direction.Left + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Left, path[1] + Direction.Left + Direction.Left))

            # Try L (2)
            elif path[1].r < path[0].r and (path[1] + Direction.Right) not in board and (path[1] + Direction.Right + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Right, path[1] + Direction.Right + Direction.Right))

            # Try L (4)
            elif path[1].r > path[0].r and (path[1] + Direction.Left) not in board and (path[1] + Direction.Left + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[1] + Direction.Left, path[1] + Direction.Left + Direction.Left))

            # Try Z (1)
            elif (path[0] + Direction.Left) not in board and (path[1] + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[0] + Direction.Left, path[1] + Direction.Right))

            # Try S (1)
            elif (path[0] + Direction.Right) not in board and (path[1] + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[1], path[0] + Direction.Right, path[1] + Direction.Left))

    elif len(path) == 1:

        # Concave to column
        if dim == "col":

            # Try I (2)
            if (path[0] + Direction.Up) not in board and (path[0] + Direction.Up + Direction.Up) not in board and (path[0] + Direction.Up + Direction.Up + Direction.Up) not in board:
                special_actions.append(PlaceAction(path[0], path[0] + Direction.Up, path[0] + Direction.Up + Direction.Up, path[0] + Direction.Up + Direction.Up + Direction.Up))

            # Try Z (1)
            elif (path[0] + Direction.Right) not in board and (path[0] + Direction.Right + Direction.Down) not in board and (path[0] + Direction.Right + Direction.Down + Direction.Right) not in board:
                special_actions.append(PlaceAction(path[0], path[0] + Direction.Right, path[0] + Direction.Right + Direction.Down, path[0] + Direction.Right + Direction.Down + Direction.Right))
 
        # Concave to row
        elif dim == "row":

            # Try I (1)
            if (path[0] + Direction.Left) not in board and (path[0] + Direction.Left + Direction.Left) not in board and (path[0] + Direction.Left + Direction.Left + Direction.Left) not in board:
                special_actions.append(PlaceAction(path[0], path[0] + Direction.Left, path[0] + Direction.Left + Direction.Left, path[0] + Direction.Left + Direction.Left + Direction.Left))

    return special_actions


def handle_final_placement(
        place_actions: list[PlaceAction],
        special_actions: list[PlaceAction],
        board: dict[Coord, PlayerColor],
        dim: str,
        pos: int
        ) -> list[PlaceAction]:
    
    last_action = []
    final_actions = []
    path = []

    # Check last touching action position
    if not special_actions:
        if place_actions:
            last_action = place_actions[-1]
    else:
            last_action = special_actions[-1]

    # Check empty availability
    step_count = 0
    if dim == "col":
        r = 0
        while r < 11:

            # Empty continues
            if Coord(r, pos) not in board:
                path.append(Coord(r, pos))
                step_count += 1

            # Empty discontinuous
            else:
                if step_count == 1:
                    step_count = 0
                    
                    
                    if final_actions:
                        a_path = a_star_search(board, final_actions[-1].c4, Coord(r - 1, pos))

                        if len(a_path) - 1 == 4:
                            final_actions.append(PlaceAction(a_path[1], a_path[2], a_path[3], a_path[4]))
                            path = []
                            continue
                        elif len(a_path) - 1 == 3:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            path = []
                            continue
                        elif len(a_path) - 1 == 2:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            path = []
                            continue
                        elif len(a_path) - 1 == 1:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            path = []
                            continue

                elif step_count == 2:
                    step_count = 0

                    if final_actions:
                        a_path = a_star_search(board, final_actions[-1].c4, Coord(r - 2, pos))

                        if len(a_path) - 1 == 4:
                            final_actions.append(PlaceAction(a_path[1], a_path[2], a_path[3], a_path[4]))
                            r -= 1
                            path = []
                            continue
                        elif len(a_path) - 1 == 3:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            r -= 1
                            path = []
                            continue
                        elif len(a_path) - 1 == 2:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            r -= 1
                            path = []
                            continue
                        elif len(a_path) - 1 == 1:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            r -= 1
                            path = []
                            continue


                elif step_count == 3:
                    step_count = 0

                    if final_actions:
                        a_path = a_star_search(board, final_actions[-1].c4, Coord(r - 3, pos))

                        if len(a_path) - 1 == 4:
                            final_actions.append(PlaceAction(a_path[1], a_path[2], a_path[3], a_path[4]))
                            r -= 2
                            path = []
                            continue
                        elif len(a_path) - 1 == 3:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            r -= 2
                            path = []
                            continue
                        elif len(a_path) - 1 == 2:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            r -= 2
                            path = []
                            continue
                        elif len(a_path) - 1 == 1:
                            temp_actions = handle_special_placement(a_path[1:], board, dim, pos)
                            if temp_actions:
                                final_actions += temp_actions
                            r -= 2
                            path = []
                            continue
                        

            # 4 continuous placements
            if step_count == 4:
                final_actions.append(PlaceAction(Coord(r-3, pos), Coord(r-2, pos), Coord(r-1, pos), Coord(r, pos)))
                step_count = 0
                path = []

            r += 1
        
    elif dim == "row":
        pass

    return final_actions
