from board import Board
from ship import Ship


class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.enemy_board = Board()
        self.ships = self.create_ships()

    def create_ships(self):
        """Создание флота кораблей"""
        return [
            Ship("Авианосец", 5),
            Ship("Линкор", 4),
            Ship("Крейсер", 3),
            Ship("Эсминец", 3),
            Ship("Катер", 2)
        ]

    def auto_place_ships(self):
        """Автоматическое размещение кораблей"""
        import random

        for ship in self.ships:
            placed = False
            attempts = 0

            while not placed and attempts < 100:
                # Случайное направление
                horizontal = random.choice([True, False])

                if horizontal:
                    x = random.randint(0, self.board.size - 1)
                    y = random.randint(0, self.board.size - ship.size)
                    positions = [(x, y + i) for i in range(ship.size)]
                else:
                    x = random.randint(0, self.board.size - ship.size)
                    y = random.randint(0, self.board.size - 1)
                    positions = [(x + i, y) for i in range(ship.size)]

                # Проверка на пересечение с другими кораблями
                valid = True
                for pos_x, pos_y in positions:
                    # Проверка соседних клеток
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            check_x, check_y = pos_x + dx, pos_y + dy
                            if (0 <= check_x < self.board.size and
                                    0 <= check_y < self.board.size and
                                    self.board.grid[check_x][check_y] == 'S'):
                                valid = False
                                break
                        if not valid:
                            break
                    if not valid:
                        break

                if valid:
                    placed = self.board.place_ship(ship, positions)

                attempts += 1

            if not placed:
                print(f"Не удалось разместить {ship.name}")
                return False

        return True

    def manual_place_ships(self):
        """Ручное размещение кораблей"""
        print(f"\n{self.name}, разместите ваши корабли:")

        for ship in self.ships:
            placed = False

            while not placed:
                self.board.display(show_ships=True)
                print(f"\nРазмещение {ship.name} (размер: {ship.size})")

                try:
                    x = int(input("Введите координату X: "))
                    y = int(input("Введите координату Y: "))
                    horizontal = input("Горизонтально? (y/n): ").lower() == 'y'

                    if horizontal:
                        positions = [(x, y + i) for i in range(ship.size)]
                    else:
                        positions = [(x + i, y) for i in range(ship.size)]

                    placed = self.board.place_ship(ship, positions)

                    if not placed:
                        print("Невозможно разместить корабль здесь!")

                except ValueError:
                    print("Пожалуйста, введите корректные числа!")

    def make_attack(self, x, y):
        """Совершение атаки"""
        return self.enemy_board.receive_attack(x, y)

    def display_boards(self):
        """Отображение обеих досок игрока"""
        print(f"\n{self.name}:")
        print("Ваша доска:")
        self.board.display(show_ships=True)
        print("\nДоска противника:")
        self.enemy_board.display(show_ships=False)
