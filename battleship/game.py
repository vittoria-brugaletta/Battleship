from battleship.player import HumanPlayer, ComputerPlayer
class Game:

    def __init__(self):
        self.human = HumanPlayer()
        self.computer = ComputerPlayer()
        self.current_player = None
        self.opponent = None
        self.round_number = 1

    def setup(self):
        self._initial_message()
        # Both players place their fleets
        self.human.place_fleet()
        self.computer.place_fleet()
        # Show boards
        self.show_boards()
        # Human start first
        self.current_player = self.human
        self.opponent = self.computer

    def _initial_message(self):
        print("Welcome to Battleship!")
        print("This is a small game implemented by V. Brugaletta")
        print("Are you ready to defeat the fleet of your enemy? Then let's start!")


    def switch_turn(self):
        # Swap roles of current player and its opponent
        temp = self.current_player
        self.current_player = self.opponent
        self.opponent = temp
        # Increase turn counter
        self.round_number += 1

    def play_turn(self):
        # Current player choose coordinate to shot at
        coordinates = self.current_player.choose_shot()
        # The board of the opponent is shot at the chosen coordinate
        result, ship = self.opponent.board.fire_at(coordinates)
        # Show result
        coord_string = self.current_player.convert_coordinate_back(coordinates)
        print(f"{self.current_player.name} shoots at {coord_string} -> " + result.upper() + "!")
        # Register the result for the current player
        self.current_player.register_result(coordinates, result, ship.length if (result.upper() == "SUNK" and ship is not None) else None)
        # Check if the entire fleet of the opponent is sunk
        return self.opponent.board.all_ships_sunk()

    def _final_message(self):
        print(f"And the winner is... {self.current_player.name}!")
        print("Thanks for playing!")

    def show_boards(self):
        # Show the two boards side by side
        left = self._render_human_board().splitlines()
        right = self._render_computer_board().splitlines()
        space = "               "
        # Title
        print("YOUR BOARD".ljust(len(left[0])) + space + "COMPUTER")
        # Print line by line
        for L, R in zip(left, right):
            print(L + space + R)

    def _render_human_board(self):
        show_ships = True
        hits = self.human.board.hits
        misses = self.human.board.misses
        return self.draw_boards(self.human.board, show_ships, hits, misses)

    def _render_computer_board(self):
        show_ships = False
        hits = self.human.opponent_view["hits"]
        misses = self.human.opponent_view["misses"]
        return self.draw_boards(self.computer.board, show_ships, hits, misses)

    def draw_boards(self, board, show_ships, hits, misses):
        size = board.SIZE
        lines = []

        # Header
        header_nums = " ".join(f"{i:>2}" for i in range(1, size + 1))
        lines.append("  " + header_nums)

        #Print rows
        for r in range(size):
            row_header = chr(ord("A") + r)
            cells = []
            for c in range(size):
                coordinate = (r, c)
                if coordinate in hits:
                    cells.append("X")
                elif coordinate in misses:
                    cells.append("O")
                elif show_ships and coordinate in self.human.board.occupied:
                    # If it's the human player board also draw the ships
                    cells.append("S")
                else:
                    cells.append("~")
            lines.append(f"{row_header} " + " ".join(f"{ch:>2}" for ch in cells))
        return "\n".join(lines)


    def play_game(self):
        self.setup()
        finish = self.play_turn()
        while not finish:
            self.switch_turn()
            if self.current_player is self.human:
                self.show_boards()
                self.human.show_enemy_fleet_status()
            finish = self.play_turn()
        self._final_message()

