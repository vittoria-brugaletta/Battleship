import pytest
from battleship.board import Board

def test_random_placement_places_all_ships():
    # Check that the random placement actually places all ships
    B = Board()
    B.ships = []
    B.occupied = {}
    # Place all fleet
    B._place_ship_randomly()
    # Count how many occupancies you expect
    counter = 0
    for ship, count in B.FLEET.items():
        counter = counter + ship.LENGTH * count
    assert len(B.occupied) == counter
    # Check also that the number of allocated ships is right
    assert len(B.ships) == sum(B.FLEET.values())




