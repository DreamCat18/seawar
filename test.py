from board import Board
from ship import Ship
from player import Player


def test_ship_creation():
    """Тест 1: Проверяем создание корабля"""
    ship = Ship("Линкор", 4)
    assert ship.name == "Линкор"
    assert ship.size == 4
    assert ship.hits == 0
    assert not ship.is_sunk


def test_ship_hit_and_sink():
    """Тест 2: Проверяем попадание и потопление корабля"""
    ship = Ship("Катер", 2)
    
    assert not ship.hit()
    assert ship.hits == 1
    
    assert ship.hit()
    assert ship.hits == 2
    assert ship.is_sunk


def test_board_creation():
    """Тест 3: Проверяем создание игровой доски"""
    board = Board()
    assert board.size == 10
    assert len(board.grid) == 10
    assert len(board.grid[0]) == 10
    assert board.grid[5][5] == '~'


def test_board_place_ship():
    """Тест 4: Проверяем размещение корабля на доске"""
    board = Board(5)
    ship = Ship("Катер", 2)
    
    positions = [(1, 1), (1, 2)]
    result = board.place_ship(ship, positions)
    
    assert result
    assert board.grid[1][1] == 'S'
    assert board.grid[1][2] == 'S'


def test_board_attack():
    """Тест 5: Проверяем атаку по доске"""
    board = Board(5)
    ship = Ship("Катер", 2)
    
    board.place_ship(ship, [(2, 2), (2, 3)])
    
    result = board.receive_attack(0, 0)
    assert result == "miss"
    assert board.grid[0][0] == 'O'
    
    result = board.receive_attack(2, 2)
    assert result == "hit"
    assert board.grid[2][2] == 'X'


def test_player_creation():
    """Тест 6: Проверяем создание игрока"""
    player = Player("Иван")
    
    assert player.name == "Иван"
    assert len(player.ships) == 5
    
    ship_names = [ship.name for ship in player.ships]
    expected_names = ["Авианосец", "Линкор", "Крейсер", "Эсминец", "Катер"]
    
    for name in expected_names:
        assert name in ship_names