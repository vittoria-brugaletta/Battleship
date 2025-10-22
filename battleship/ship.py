class Ship:

    def __init__(self, name, length, position):
        self.name = name
        self.length = length
        self.hits = set()
        if not isinstance(position, set):
            raise TypeError('position must be a set')
        self.position = frozenset(position)  # Position never changes

    def check_coordinates(self):
        # Check whether the number of coordinates is equal to length
        if (len(self.position) != self.length):
            raise ValueError("Ship position must have length equal to ship length")

    def occupies(self, coordinate):
        # Checks whether the ship sits on a given coordinate
        return coordinate in self.position

    def register_hit(self, coordinate):
        # Returns True if the ship has been hit, otherwise False
        if coordinate in self.position:
            self.hits.add(coordinate)
            return True
        else:
            return False

    def is_sunk(self):
        return self.position == self.hits

# The ship types belonging to the fleet
class Battleship(Ship):
    LENGTH = 4
    def __init__(self, position):
        # Takes the method from parent class
        # Hits are initialized as empty set
        super().__init__("Battleship", Battleship.LENGTH, position)
        # Check coordinates to be of the right lenght
        self.check_coordinates()

class Cruiser(Ship):
    LENGTH = 3
    def __init__(self, position):
        super().__init__("Cruiser", Cruiser.LENGTH, position)
        self.check_coordinates()

class Destroyer(Ship):
    LENGTH = 2
    def __init__(self, position):
        super().__init__("Destroyer", Destroyer.LENGTH, position)
        self.check_coordinates()

class Submarine(Ship):
    LENGTH = 1
    def __init__(self, position):
        super().__init__("Submarine", Submarine.LENGTH, position)
        self.check_coordinates()
