from battleship.ship import Ship, Battleship, Cruiser, Destroyer, Submarine
import random

class Board:
    # This game considers a 10x10 board
    SIZE = 10
    # This is needed for the random placement of the fleet
    MAX_TRIES = 1000
    # The composition of the fleet
    FLEET = {Battleship:1, Cruiser:2, Destroyer:3, Submarine:4}
    def __init__(self):
        self.ships = []
        self.occupied = {}
        self.hits = set()
        self.misses = set()


    def in_grid(self, coordinate):
        # Checks that a given coordinate is in the grid
        row = coordinate[0]
        column = coordinate[1]
        return 0 <= row < self.SIZE and 0 <= column < self.SIZE

    def _orthogonal_neighbors(self, coordinate):
        # For each hit coordinate of a ship, compute the north/south/east/west neighbours
        row, column = coordinate
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if self.in_grid((row + dr, column + dc)):
                yield (row + dr, column + dc)

    def _has_orthogonal_conflict(self, position):
        # There must be at least one-cell distance between ships in the orthogonal direction
        # This method checks if there is a conflict
        pos_set = set(position)
        for pos in position:
            for neighbor in self._orthogonal_neighbors(pos):
                if neighbor not in pos_set and neighbor in self.occupied:
                    return True # conflict
        return False


    def place_ship(self, ship_type, start, orientation):
        # Given a ship type, its initial coordinate and orientation, we place the ship on the board
        # Check if the ship_type is allowed
        if not issubclass(ship_type, Ship) or ship_type is Ship:
            raise TypeError('ship_type must be a subclass of Ship')
        # Check if start coordinates are in the grid
        start_row, start_column = start
        if not self.in_grid((start_row, start_column)):
            return False
        # Force orientation to be in upper case and check if it is valid
        orientation = orientation.upper()
        if orientation not in {"H", "V"}:
            return False

        # Check whether the end of the ship is in the grid
        if orientation == "H":
            if not self.in_grid((start_row, start_column + ship_type.LENGTH - 1)):
                return False
        else:
            if not self.in_grid((start_row + ship_type.LENGTH - 1, start_column)):
                return False

        # Given a start point compute coordinates of the ship
        new_positions = []
        for i in range(ship_type.LENGTH):
            if orientation == "H":
                # Horizontal orientation
                row = start_row
                column = start_column + i
                # Check for overlaps with other ships
                if (row, column) in self.occupied:
                    return False
                new_positions.append((row, column))
            else:
                # Vertical orientation
                row = start_row + i
                column = start_column
                if (row, column) in self.occupied:
                    return False
                new_positions.append((row, column))

        if self._has_orthogonal_conflict(new_positions):
            return False

        # Create the ship
        ship = ship_type(set(new_positions))
        # Add ship to the list of ships for the Board
        self.ships.append(ship)
        # Add the coordinates to the dictionary with occupancies
        for coordinate in new_positions:
            self.occupied[coordinate] = ship
        return True

    def _place_ship_randomly(self):
        # Place the entire fleet on the board randomly
        # Our fleet - how many ships we need according to type
        fleet = Board.FLEET

        for ship_type, count in fleet.items():
            for _ in range(count):
                placed = False
                for attempt in range(self.MAX_TRIES):
                    # Choose orientation randomly
                    orientation = random.choice(['H', 'V'])
                    # Choose in-bounds start coordinates
                    if orientation == "H":
                        start_row = random.randint(0, self.SIZE - 1)
                        start_col = random.randint(0, self.SIZE - ship_type.LENGTH)
                    else:
                        start_row = random.randint(0, self.SIZE - ship_type.LENGTH)
                        start_col = random.randint(0, self.SIZE - 1)

                    coordinate = (start_row, start_col)
                    # Try to allocate the ship
                    placed = self.place_ship(ship_type, coordinate, orientation)
                    if placed:
                        # If the ship is placed exit
                        break

                if not placed:
                    # Proceed with deterministic approach
                    # Take the first place possible
                    for direction in ["H", "V"]:
                        if direction == "H":
                            for row in range(self.SIZE):
                                for column in range(self.SIZE-ship_type.LENGTH + 1):
                                    placed = self.place_ship(ship_type, (row, column), direction)
                                    if placed:
                                        break
                                if placed:
                                    break

                        elif direction == "V":
                            for column in range(self.SIZE):
                                for row in range(self.SIZE-ship_type.LENGTH + 1):
                                    placed = self.place_ship(ship_type, (row, column), direction)
                                    if placed:
                                        break
                                if placed:
                                    break
                        if placed:
                            break

                    if not placed:
                        raise RuntimeError('Failed to place ship')


    def place_fleet(self):
        # Public interface to place all ships automatically
        self._place_ship_randomly()

    def fire_at(self, coordinates):
        # It shoots at the given coordinates
        #Check whether the coordinates are a tuple
        if not isinstance(coordinates, tuple) or len(coordinates) != 2:
            raise TypeError('coordinates must be a 2-tuple')
        # Check whether the coordinates are inside the boundaries
        if not self.in_grid(coordinates):
            return ("Invalid", None)
        # Check whether these coordinates have already been fired at
        if coordinates in self.hits or coordinates in self.misses:
            return ("Repeat", None)
        # Check whether there is a ship at those coordinates
        if coordinates in self.occupied:
            # Register hit on the board
            self.hits.add(coordinates)
            # Recover which ship was shot
            ship = self.occupied[coordinates]
            # Register the hit
            ship.register_hit(coordinates)
            # Check whether the ship is sunk
            if ship.is_sunk():
                return ("Sunk", ship)
            else:
                return ("Hit", None)
        else:
            # Add missed coordinates to the board
            self.misses.add(coordinates)
            return ("Miss", None)

    def all_ships_sunk(self):
        # returns True if all ships are sunk, False otherwise
        return all(ship.is_sunk() for ship in self.ships)

