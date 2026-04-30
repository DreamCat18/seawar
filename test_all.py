
import unittest
from board import Board
from ship import Ship
from player import Player
from game import BattleshipGame
from utils import get_random_attack, validate_coordinates, calculate_ship_health


class TestShip(unittest.TestCase):
    """Тесты для класса Ship"""

    def test_ship_creation(self):
        """Тест создания корабля"""
        ship = Ship("Линкор", 4)
        self.assertEqual(ship.name, "Линкор")
        self.assertEqual(ship.size, 4)
        self.assertEqual(ship.hits, 0)
        self.assertFalse(ship.is_sunk)

    def test_ship_hit_and_sink(self):
        """Тест попадания и потопления корабля"""
        ship = Ship("Катер", 2)
        self.assertFalse(ship.hit())
        self.assertEqual(ship.hits, 1)
        self.assertTrue(ship.hit())
        self.assertEqual(ship.hits, 2)
        self.assertTrue(ship.is_sunk)

    def test_ship_place_ship(self):
        """Тест размещения корабля"""
        ship = Ship("Эсминец", 3)
        positions = [(1, 1), (1, 2), (1, 3)]
        ship.place_ship(positions)
        self.assertEqual(ship.positions, positions)

    def test_ship_str(self):
        """Тест строкового представления корабля"""
        ship = Ship("Линкор", 4)
        str_repr = str(ship)
        self.assertIn("Линкор", str_repr)
        self.assertIn("4", str_repr)
        self.assertIn("нет", str_repr)


class TestBoard(unittest.TestCase):
    """Тесты для класса Board"""

    def test_board_creation(self):
        """Тест создания доски"""
        board = Board()
        self.assertEqual(board.size, 10)
        self.assertEqual(len(board.grid), 10)
        self.assertEqual(len(board.grid[0]), 10)
        self.assertEqual(board.grid[5][5], '~')

    def test_board_place_ship(self):
        """Тест размещения корабля на доске"""
        board = Board(5)
        ship = Ship("Катер", 2)
        positions = [(1, 1), (1, 2)]
        result = board.place_ship(ship, positions)
        self.assertTrue(result)
        self.assertEqual(board.grid[1][1], 'S')
        self.assertEqual(board.grid[1][2], 'S')

    def test_board_attack(self):
        """Тест атаки по доске"""
        board = Board(5)
        ship = Ship("Катер", 2)
        board.place_ship(ship, [(2, 2), (2, 3)])

        result = board.receive_attack(0, 0)
        self.assertEqual(result, "miss")
        self.assertEqual(board.grid[0][0], 'O')

        result = board.receive_attack(2, 2)
        self.assertEqual(result, "hit")
        self.assertEqual(board.grid[2][2], 'X')

    def test_board_invalid_attack(self):
        """Тест неверной атаки"""
        board = Board(5)
        result = board.receive_attack(-1, 0)
        self.assertEqual(result, "invalid")

        result = board.receive_attack(10, 10)
        self.assertEqual(result, "invalid")

    def test_board_already_attacked(self):
        """Тест повторной атаки по той же клетке"""
        board = Board(5)
        board.receive_attack(0, 0)
        result = board.receive_attack(0, 0)
        self.assertEqual(result, "already_attacked")

    def test_board_all_ships_sunk(self):
        """Тест проверки потопления всех кораблей"""
        board = Board(5)
        self.assertTrue(board.all_ships_sunk())

        ship = Ship("Катер", 2)
        board.place_ship(ship, [(0, 0), (0, 1)])
        self.assertFalse(board.all_ships_sunk())

        board.receive_attack(0, 0)
        board.receive_attack(0, 1)
        self.assertTrue(board.all_ships_sunk())

    def test_board_get_available_positions(self):
        """Тест получения доступных позиций"""
        board = Board(5)
        available = board.get_available_positions()
        self.assertEqual(len(available), 25)

        board.receive_attack(0, 0)
        available = board.get_available_positions()
        self.assertEqual(len(available), 24)
        self.assertNotIn((0, 0), available)


class TestPlayer(unittest.TestCase):
    """Тесты для класса Player"""

    def test_player_creation(self):
        """Тест создания игрока"""
        player = Player("Иван")
        self.assertEqual(player.name, "Иван")
        self.assertEqual(len(player.ships), 5)

        ship_names = [ship.name for ship in player.ships]
        expected_names = ["Авианосец", "Линкор", "Крейсер", "Эсминец", "Катер"]
        for name in expected_names:
            self.assertIn(name, ship_names)

    def test_player_auto_place_ships(self):
        """Тест автоматического размещения кораблей"""
        player = Player("Петр")
        result = player.auto_place_ships()
        self.assertTrue(result)

        # Проверяем, что все корабли размещены
        for ship in player.ships:
            self.assertEqual(len(ship.positions), ship.size)

    def test_player_make_attack(self):
        """Тест атаки игрока"""
        player = Player("Анна")
        opponent = Player("Борис")

        opponent.auto_place_ships()
        result = player.make_attack(0, 0)
        self.assertIn(result, ["hit", "miss", "hit_sunk"])

    def test_player_calculate_ship_health(self):
        """Тест расчета здоровья кораблей"""
        player = Player("Дмитрий")
        current, total = calculate_ship_health(player)
        self.assertEqual(total, 17)  # 5+4+3+3+2
        self.assertEqual(current, 17)


class TestGame(unittest.TestCase):
    """Тесты для класса BattleshipGame"""

    def test_game_creation(self):
        """Тест создания игры"""
        game = BattleshipGame()
        self.assertEqual(len(game.players), 0)
        self.assertEqual(game.current_player_index, 0)

    def test_game_switch_player(self):
        """Тест смены игрока"""
        game = BattleshipGame()
        game.players = [Player("Игрок1"), Player("Игрок2")]

        current = game.get_current_player()
        self.assertEqual(current.name, "Игрок1")

        game.switch_player()
        current = game.get_current_player()
        self.assertEqual(current.name, "Игрок2")

    def test_game_get_opponent(self):
        """Тест получения противника"""
        game = BattleshipGame()
        game.players = [Player("Игрок1"), Player("Игрок2")]

        opponent = game.get_opponent()
        self.assertEqual(opponent.name, "Игрок2")

        game.switch_player()
        opponent = game.get_opponent()
        self.assertEqual(opponent.name, "Игрок1")

    def test_game_check_win_condition(self):
        """Тест проверки условия победы"""
        game = BattleshipGame()
        game.players = [Player("Игрок1"), Player("Игрок2")]

        # Размещаем корабли противника
        opponent = game.get_opponent()
        opponent.auto_place_ships()

        # Изначально никто не победил (корабли размещены, но не потоплены)
        self.assertFalse(game.check_win_condition())

        # Потопляем все корабли противника
        for ship in opponent.ships:
            for pos in ship.positions:
                opponent.board.receive_attack(pos[0], pos[1])

        # Теперь текущий игрок должен победить
        self.assertTrue(game.check_win_condition())


class TestUtils(unittest.TestCase):
    """Тесты для утилит"""

    def test_validate_coordinates(self):
        """Тест валидации координат"""
        self.assertTrue(validate_coordinates(0, 0, 10))
        self.assertTrue(validate_coordinates(5, 5, 10))
        self.assertTrue(validate_coordinates(9, 9, 10))

        self.assertFalse(validate_coordinates(-1, 0, 10))
        self.assertFalse(validate_coordinates(0, -1, 10))
        self.assertFalse(validate_coordinates(10, 0, 10))
        self.assertFalse(validate_coordinates(0, 10, 10))

    def test_calculate_ship_health(self):
        """Тест расчета здоровья кораблей"""
        player = Player("Тест")
        current, total = calculate_ship_health(player)
        self.assertEqual(total, 17)
        self.assertEqual(current, 17)

        # Наносим урон первому кораблю
        player.ships[0].hit()
        current, total = calculate_ship_health(player)
        self.assertEqual(total, 17)
        self.assertEqual(current, 16)

    def test_get_random_attack(self):
        """Тест случайной атаки"""
        board = Board(5)
        attack = get_random_attack(board)
        self.assertIsNotNone(attack)
        self.assertIn(attack[0], range(5))
        self.assertIn(attack[1], range(5))

        # После атаки позиция должна быть недоступна
        board.receive_attack(attack[0], attack[1])
        new_attack = get_random_attack(board)
        self.assertNotEqual(attack, new_attack)


if __name__ == '__main__':
    unittest.main()
