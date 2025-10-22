import pytest
from battleship.board import Board
from battleship.ship import Battleship

def test_fire_at_water():
    # If an empty cell is fired, there should be no change in the ships
    B = Board()
    B.ships = []
    B.occupied = {}

    # Empty coordinates
    coordinates = (5, 5)
    result, sunk_len = B.fire_at(coordinates)
    # Check that we got a miss
    assert result.upper() == "MISS"
    # Check that the length of the sunk ship is None (no sinking)
    assert sunk_len is None

    # Check that board changed correctly
    assert coordinates in B.misses
    assert coordinates not in B.hits

    # Check that the ships are not changed
    assert len(B.ships) == 0
    assert coordinates not in B.occupied

def test_fire_at_ship_piece():
    # If we fire at one single piece of a ship, there should be no "SUNK" state
    B = Board()
    B.ships = []
    B.occupied = {}

    # Place one ship
    B.place_ship(Battleship, (0, 6), "H")

    # Fire at this ship
    result, sunk_len = B.fire_at((0, 7))
    assert result.upper() == "HIT"
    # If not sunk, ship is None
    assert sunk_len is None

    # Check hit is recorded
    assert len(B.hits) == 1
    assert (0, 7) in B.hits
    assert (0, 7) not in B.misses

def test_fire_at_ship_sunk():
    # We test the sinking of the ship
    B = Board()
    B.ships = []
    B.occupied = {}

    # Place one ship
    B.place_ship(Battleship, (0, 6), "H")

    # Fire at this ship
    B.fire_at((0, 6))
    B.fire_at((0, 7))
    B.fire_at((0, 8))
    result, sunk_len = B.fire_at((0, 9))
    assert result.upper() == "SUNK"
    # Check correct sunk_len
    assert sunk_len.LENGTH == Battleship.LENGTH




