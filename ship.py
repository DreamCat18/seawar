class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = 0
        self.is_sunk = False

    def place_ship(self, positions):
        """Размещение корабля на доске"""
        self.positions = positions

    def hit(self):
        """Попадание по кораблю"""
        self.hits += 1
        if self.hits == self.size:
            self.is_sunk = True
        return self.is_sunk

    def __str__(self):
        return f"{self.name} (размер: {self.size}, потоплен: {'да' if self.is_sunk else 'нет'})"
