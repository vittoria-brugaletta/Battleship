from battleship.board import Board
from abc import ABC, abstractmethod
import random

# I use an abstract class so Player cannot be instantiated on its own
class Player(ABC):

    def __init__(self, name):
        self.name = name
        self.board = Board()
        # The idea you have of your opponent's board
        self.opponent_view = {
            "hits": set(),
            "misses": set(),
            # In the beginning is everything unknown
            "unknown": {(row, column) for row in range(self.board.SIZE) for column in range(self.board.SIZE)}
        }

    def place_fleet(self):
        self.board.place_fleet()

    @abstractmethod
    def choose_shot(self):
        # This must be done in the subclasses
        pass

    def register_result(self, coordinates, result, sunk_len = None):
        # It registers the result after a shot
        # Check result
        result = result.upper()
        if result not in {"HIT", "SUNK", "MISS"}:
            return
        # Remove the coordinates from the unknown set
        self.opponent_view["unknown"].discard(coordinates)
        if result in {"HIT", "SUNK"}:
            self.opponent_view["hits"].add(coordinates)
            # To avoid contradictions
            self.opponent_view["misses"].discard(coordinates)
        else:
            self.opponent_view["misses"].add(coordinates)
            # To avoid contradictions
            self.opponent_view["hits"].discard(coordinates)

    def convert_coordinate_back(self, numeric_coord:tuple[int, int]) -> str:
        # It converts the coordinates from tuple to string (e.g. (0,0) -> A1)
        row, column = numeric_coord
        if not self.board.in_grid((row, column)):
            return None
        row_letter = chr(ord('A') + row)
        col_number = column + 1
        return f"{row_letter}{col_number}"



class HumanPlayer(Player):

    def __init__(self):
        super().__init__("Human")
        self.enemy_afloat = dict(self.board.FLEET)


    def convert_coordinates(self, user_input:str) -> tuple[int, int] | None:
        # Convert coordinates for human player
        # The board goes from A to J on y-axis, and from 1 to 10 on the x-axis
        s = user_input.strip().upper()
        # Check if length of string is correct
        if len(s) not in [2,3] or not s[1:].isnumeric():
            return None
        letter = s[0]
        number = int(s[1:])
        if not letter.isalpha() or not ord("A") <= ord(letter) <= ord("J"):
            return None
        if not 1 <= number <=10:
            return None
        row = ord(letter) - ord("A")
        column = number-1
        return (row, column)

    def choose_shot(self):
        # Asks for coordinates to be shot at via terminal input
        while True:
            print("What coordinate would you like to fire at? Insert e.g. B7")
            string_coordinate = input("Answer: ").strip()
            coordinate = self.convert_coordinates(string_coordinate)
            # Check whether coordinate is valid, and if it has already been chosen
            if coordinate and coordinate in self.opponent_view["unknown"]:
                return coordinate
            print("Invalid coordinate, please try again.")

    def _decrease_counter(self, counter:dict, ship_length:int):
        # If a ship is sunk, it decreases the counter of the remaining ships
        # Counter is like FLEET
        for ship_type, count in counter.items():
            if ship_type.LENGTH == ship_length and count > 0:
                counter[ship_type] = count - 1
                return
        # Only raise if we don't find a matching ship
        raise RuntimeError(f"No remaining ship of length {ship_length}.")


    def register_result(self, coordinates, result, sunk_len = None):
        # This addition is needed for the opponent's fleet counter
        super().register_result(coordinates, result)
        if sunk_len is not None:
            self._decrease_counter(self.enemy_afloat, sunk_len)

    def show_enemy_fleet_status(self):
        # It prints the status of the opponent's fleet at each turn
        print("Enemy's fleet status:")
        for ship_type, counter in self.enemy_afloat.items():
            print(f"{ship_type.__name__} ({ship_type.LENGTH} cells): remaining {counter}")

class ComputerPlayer(Player):

    def __init__(self):
        super().__init__("Computer")
        self.untried = {(row, col) for row in range(self.board.SIZE) for col in range (self.board.SIZE)}
        self.parity_pos = {(row, col) for (row, col) in self.untried if (row + col) % 2 == 0}
        self.mode = "hunt"
        self.hit_seed = None
        self.connected_hits = set()
        self.candidates = set()
        self.orientation = None
        self.counter = {4:1, 3:2, 2:3, 1:4} # Length:number of ships

    def choose_shot(self):
        # "Hunt" is random choice, "Target" is deterministic once a ship has been hit
        # Searching for any ship
        if self.mode == "hunt":
            return self._hunt_cell()
        # We hit a ship, so we are looking for the rest of it
        else:
            return self._target_cell()

    def _use_parity(self):
        # If there are ships longer than 1 left we use parity
        # This means that only every two-cells we check the board, instead of each cell
        # -> Random search gets optimized by 50%
        # Returns true if there are ships longer than 1 cell left
        return any(length > 1 and count > 0 for length, count in self.counter.items())

    def register_result(self, coordinates, result, sunk_len=None):
        # It registers each shot's result
        result = result.upper()
        # Call the code defined in the parent class
        super().register_result(coordinates, result)

        # If there was a hit
        if result == "HIT":
            if self.mode == "hunt":
                # Switch to targeting
                self._start_targeting(coordinates)
            else:
                self.connected_hits.add(coordinates)
                if len(self.connected_hits) >= 2:
                    # Check whether they are aligned
                    hits = list(self.connected_hits)
                    hit1, hit2 = hits[0], hits[1]
                    if hit1[0] == hit2[0] or hit1[1] == hit2[1]:
                        self._update_orientation(hit1, hit2)
                if self.orientation is None:
                    self._neighbours(coordinates)
                else:
                    # if orientation is known, keep only candidates in the same line
                    if self.orientation == "H":
                        # Find the row
                        row = next(iter(self.connected_hits))[0]
                        # Filter out the candidates that are not on that row
                        self.candidates = {c for c in self.candidates if c[0] == row}
                        # Extend the line at both ends
                        cols = [c for _,c in self.connected_hits] # All columns
                        col_min, col_max = min(cols), max(cols)
                        # Find columns left to the min and right to the max
                        left = (row, col_min - 1)
                        right = (row, col_max + 1)
                        # Add these neighbours to the candidates
                        for nxt in (left, right):
                            if self.board.in_grid(nxt) and nxt in self.untried:
                                self.candidates.add(nxt)
                    else:
                        # Vertical orientation - Do the same for the columns
                        # Find the column
                        column = next(iter(self.connected_hits))[1]
                        # Filter out the candidates that are not in that column
                        self.candidates = {c for c in self.candidates if c[1] == column}
                        # Extend the line at both ends
                        rows = [r for r,_ in self.connected_hits] # All rows
                        row_min, row_max = min(rows), max(rows)
                        # Find rows upper than min and lower than max
                        up = (row_min - 1, column)
                        down = (row_max + 1, column)
                        # Add these neighbours to the candidates
                        for nxt in (up, down):
                            if self.board.in_grid(nxt) and nxt in self.untried:
                                self.candidates.add(nxt)

        # Decrease the self.counter every time a ship is sunk
        if result == "SUNK" and sunk_len is not None:
            if sunk_len in self.counter and self.counter[sunk_len] > 0:
                self.counter[sunk_len] -= 1
            self._clear_target_state()

        self.untried.discard(coordinates)
        self.parity_pos.discard(coordinates)

    def _hunt_cell(self):
        # The coordinate to be shot at is chosen randomly
        # Choose the target cell depending on parity mode
        if self._use_parity():
            # Parity untried cells
            candidates = self.parity_pos & self.untried
        else:
            candidates = self.untried
        if not candidates:
            raise RuntimeError("No more cells to shoot at.")

        coordinate = random.choice(list(candidates))
        self.parity_pos.discard(coordinate)
        self.untried.discard(coordinate)
        return coordinate

    def _neighbours(self, hit_cell):
        # Compute the four cells south/north/west/east than the hit one
        row_hit, column_hit = hit_cell
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            neighbour = (row_hit + dx, column_hit + dy)
            if self.board.in_grid(neighbour) and neighbour in self.untried:
                self.candidates.add(neighbour)

    def _start_targeting(self, hit_cell):
        # If a ship is hit, switch mode to target
        # Clear structures from previous targeting
        self.mode = "target"
        self.hit_seed = hit_cell
        self.connected_hits = set()
        self.candidates = set()
        self.orientation = None
        # Add the hit cell to the connected hits
        self.connected_hits.add(hit_cell)
        self._neighbours(hit_cell)


    def _update_orientation(self, hit1, hit2):
        # Given two aligned hits, compute the orientation of the ship (horizontal, vertical)
        row1, col1 = hit1
        row2, col2 = hit2

        if row1 == row2:
            self.orientation = "H"
        elif col1 == col2:
            self.orientation = "V"
        else:
            raise RuntimeError("Hits are not aligned")

    def _target_cell(self):
        # Target mode - once a ship is hit, check the rest of it in the neighbouring cells
        available_candidates = self.candidates & self.untried
        if self.orientation is None:
            if not available_candidates:
                self.mode = "hunt"
                return self._hunt_cell()
            # If orientation is not known, pick a random neighbour
            coordinate = random.choice(list(available_candidates))
        elif self.orientation == "H":
            # If orientation is horizontal, pick a neighbour in the same row
            ref_row = next(iter(self.connected_hits))[0]
            horizontal_candidates = {cell for cell in available_candidates if cell[0] == ref_row}
            if not horizontal_candidates:
                coordinate = random.choice(list(available_candidates))
            else:
                coordinate = random.choice(list(horizontal_candidates))
        else:
            # If orientation is vertical, pick a neighbour in the same column
            ref_col = next(iter(self.connected_hits))[1]
            vertical_candidates = {cell for cell in available_candidates if cell[1] == ref_col}
            if not vertical_candidates:
                coordinate = random.choice(list(available_candidates))
            else:
                coordinate = random.choice(list(vertical_candidates))
        self.parity_pos.discard(coordinate)
        self.untried.discard(coordinate)
        self.candidates.discard(coordinate)
        return coordinate

    def _clear_target_state(self):
        # After target is finished, switch back to hunt mode
        self.mode = "hunt"
        self.connected_hits.clear()
        self.candidates.clear()
        self.orientation = None
        self.hit_seed = None
