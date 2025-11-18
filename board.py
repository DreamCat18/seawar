class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.hits = []
        self.misses = []

    def place_ship(self, ship, positions):
        """Размещение корабля на доске"""
        for x, y in positions:
            if not self.is_valid_position(x, y) or self.grid[x][y] != '~':
                return False

        for x, y in positions:
            self.grid[x][y] = 'S'

        ship.place_ship(positions)
        self.ships.append(ship)
        return True

    def is_valid_position(self, x, y):
        """Проверка валидности позиции"""
        return 0 <= x < self.size and 0 <= y < self.size

    def receive_attack(self, x, y):
        """Обработка атаки"""
        if not self.is_valid_position(x, y):
            return "invalid"

        if (x, y) in self.hits or (x, y) in self.misses:
            return "already_attacked"

        if self.grid[x][y] == 'S':
            self.grid[x][y] = 'X'
            self.hits.append((x, y))

            # Находим корабль и регистрируем попадание
            for ship in self.ships:
                if (x, y) in ship.positions:
                    is_sunk = ship.hit()
                    return "hit_sunk" if is_sunk else "hit"
        else:
            self.grid[x][y] = 'O'
            self.misses.append((x, y))
            return "miss"

    def all_ships_sunk(self):
        """Проверка, все ли корабли потоплены"""
        return all(ship.is_sunk for ship in self.ships)

    def display(self, show_ships=False):
        """Отображение доски"""
        print("  " + " ".join(str(i) for i in range(self.size)))
        for i in range(self.size):
            row = []
            for j in range(self.size):
                if self.grid[i][j] == 'S' and not show_ships:
                    row.append('~')
                else:
                    row.append(self.grid[i][j])
            print(f"{i} " + " ".join(row))

    def get_available_positions(self):
        """Получение списка доступных позиций"""
        return [(i, j) for i in range(self.size) for j in range(self.size)
                if self.grid[i][j] == '~']
