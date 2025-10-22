import pytest
from battleship.board import Board
from battleship.ship import Battleship

def test_placement_accepts_edge_coordinates():
    # Test whether a ship can finish at the edge
    B = Board()
    B.ships = []
    B.occupied = {}
    # Horizontal orientation, finishing at right edge
    result = B.place_ship(Battleship, (0, 6), "H")
    assert result is True
    # Vertical orientation, finishing at the bottom row
    result = B.place_ship(Battleship, (6, 3), "V")
    assert result is True

def test_placement_rejects_out_of_bounds():
    # If a ship is at a start point that would finish out-of-bounds, reject placement
    B = Board()
    B.ships = []
    B.occupied = {}
    # Horizontal orientation, finishing beyond right edge
    result = B.place_ship(Battleship, (0, 7), "H")
    assert result is False
    # Vertical orientation, finishing beyond the bottom row
    result = B.place_ship(Battleship, (7, 3), "V")
    assert result is False

def test_placement_rejects_overlap():
    # If a ship overlaps with another, reject placement
    B = Board()
    B.ships = []
    B.occupied = {}
    # Place first ship
    B.place_ship(Battleship, (0, 6), "H")
    # Place second ship
    result = B.place_ship(Battleship, (0, 6), "V")
    assert result is False

def test_placement_rejects_orthogonal_neighbor():
    # A ship cannot be placed next to another one in the orthogonal directions
    B = Board()
    B.ships = []
    B.occupied = {}
    # Place first ship
    B.place_ship(Battleship, (0, 6), "H")
    # Place second ship
    result = B.place_ship(Battleship, (1, 6), "V")
    assert result is False

def test_placement_accepts_diagonal_neighbor():
    # A ship can be placed near another in the diagonal direction
    B = Board()
    B.ships = []
    B.occupied = {}
    # Place first ship
    B.place_ship(Battleship, (0, 6), "H")
    # Place second ship
    result = B.place_ship(Battleship, (1, 5), "V")
    assert result is True