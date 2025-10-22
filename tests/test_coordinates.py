import pytest
from battleship.player import HumanPlayer

# Check coordinates conversions
# From tuple to letter + numerical value (e.g. C5)
def test_tuple_to_label_conversion():
    Alice = HumanPlayer()
    #Extremes of the board
    result = Alice.convert_coordinate_back((0, 0))
    assert result == "A1"
    result = Alice.convert_coordinate_back((9, 9))
    assert result == "J10"
    # Invalid values
    result = Alice.convert_coordinate_back((10, 10))
    assert result is None

def test_label_to_tuple_conversion():
    Alice = HumanPlayer()
    # Test board boundaries
    result = Alice.convert_coordinates("A1")
    assert result == (0, 0)
    result = Alice.convert_coordinates("J10")
    assert result == (9, 9)
    # Test invalid values
    result = Alice.convert_coordinates("10")
    assert result is None
    result = Alice.convert_coordinates("A0")
    assert result is None
    # Test lower case input
    result = Alice.convert_coordinates("a1")
    assert result == (0, 0)
    # Test presence of spaces in input
    result = Alice.convert_coordinates(" a1 ")
    assert result == (0, 0)
    # A few bad inputs
    result = Alice.convert_coordinates("")
    assert result is None
    result = Alice.convert_coordinates("AA1")
    assert result is None
    result = Alice.convert_coordinates("A*1")
    assert result is None


