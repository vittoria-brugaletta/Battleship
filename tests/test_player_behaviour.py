import pytest
from battleship.player import HumanPlayer, ComputerPlayer
from battleship.ship import Battleship

def test_register_result_updates_opponent_view_for_miss():
    # If the player shots to the water, the opponent view must get a miss, not a hit or unknown
    coordinates = (0, 0)
    # Test for human player
    Alice = HumanPlayer()
    Alice.register_result(coordinates, "MISS", None)
    assert coordinates in Alice.opponent_view["misses"]
    assert coordinates not in Alice.opponent_view["hits"]
    assert coordinates not in Alice.opponent_view["unknown"]
    # Test for computer player
    Computer = ComputerPlayer()
    coordinates = (1, 1)
    Computer.register_result(coordinates, "MISS", None)
    assert coordinates in Computer.opponent_view["misses"]
    assert coordinates not in Computer.opponent_view["hits"]
    assert coordinates not in Computer.opponent_view["unknown"]

def test_register_result_updates_opponent_view_for_hit():
    # If a ship is shot, the coordinates of the hit should move to the "hits"
    # Test for human player
    coordinates = (0, 0)
    Alice = HumanPlayer()
    Alice.register_result(coordinates, "HIT", None)
    assert coordinates in Alice.opponent_view["hits"]
    assert coordinates not in Alice.opponent_view["misses"]
    assert coordinates not in Alice.opponent_view["unknown"]
    # Check that the hit doesn't change the fleet counter
    assert Alice.enemy_afloat == Alice.board.FLEET
    # Test for computer player
    Computer = ComputerPlayer()
    coordinates = (1, 1)
    Computer.register_result(coordinates, "HIT", None)
    assert coordinates in Computer.opponent_view["hits"]
    assert coordinates not in Computer.opponent_view["misses"]
    assert coordinates not in Computer.opponent_view["unknown"]

def test_register_result_decreases_opponent_fleet_on_sunk():
    # If a computer player's ship is sunk, the fleet counter should decrease by one
    coordinates = (0, 0)
    Alice = HumanPlayer()
    before = Alice.enemy_afloat[Battleship]
    Alice.register_result(coordinates, "HIT", Battleship.LENGTH)
    assert Alice.enemy_afloat[Battleship] == before - 1

