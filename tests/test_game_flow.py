import pytest
from battleship.game import Game

def test_play_game_loop(monkeypatch):
    # Check whether the board is shown only once for a single round
    # Check ordering of the instructions in play_game()
    game = Game()

    # Simulate the output of play_turn() for three turns: start turn (Human, False),
    # second turn (Computer, False), last turn (Human, True)
    outcomes = iter([False, False, True]) # iterator

    # Count how many times the boards and the fleet are drawn
    draw_count = {"boards": 0, "fleet": 0}
    # Log of what happens
    log = []

    # Replace the Game.setup() and Game._final_message() with dummy functions
    # that only keep track of being called
    monkeypatch.setattr(game, "setup", lambda: log.append("setup"))
    monkeypatch.setattr(game, "_final_message", lambda: log.append("final_message"))

    # Fake turn, it mimics play_turn()
    def fake_play_turn():
        val = next(outcomes)
        log.append(f"play_turn: {val}, ({'Human' if game.current_player is game.human else 'Computer'})")
        return val

    # It mimics switch_turn()
    def fake_switch_turn():
        if game.current_player is game.human:
            game.current_player = game.computer
        else:
            game.current_player = game.human
        log.append(f"switch_turn: {game.current_player.name}")

    # It mimics show_boards()
    def fake_show_boards():
        # Doesn't show anything, only increase counter
        draw_count["boards"] += 1
        log.append("Show boards")

    # It mimics show_enemy_fleet_status()
    def fake_fleet_status():
        draw_count["fleet"] += 1
        log.append("show_enemy_fleet_status")

    # We substitute the real methods with our fake ones
    monkeypatch.setattr(game, "play_turn", fake_play_turn)
    monkeypatch.setattr(game, "switch_turn", fake_switch_turn)
    monkeypatch.setattr(game, "show_boards", fake_show_boards)
    monkeypatch.setattr(game.human, "show_enemy_fleet_status", fake_fleet_status)

    # Ensure that the game starts with human player (as done in the code)
    game.current_player = game.human

    # Run the play_game loop
    game.play_game()

    # In this small loop we should only show once the boards and the fleet status
    assert draw_count["boards"] == 1
    assert draw_count["fleet"] == 1

    # Check that setup has been called
    assert "setup" in log
    # Check that show_boards has been called
    assert "Show boards" in log
    # Check that show boards appeared only after the computer's turn
    ind = log.index("Show boards")
    assert "play_turn: False, (Computer)" in log[:ind]
    # Check that final message has been printed
    assert "final_message" in log



