import random


def get_random_attack(board):
    """Получение случайной атаки для AI"""
    available = board.get_available_positions()
    return random.choice(available) if available else None


def validate_coordinates(x, y, board_size):
    """Валидация координат"""
    return 0 <= x < board_size and 0 <= y < board_size


def calculate_ship_health(player):
    """Расчет оставшегося здоровья флота"""
    total_health = sum(ship.size for ship in player.ships)
    current_health = sum(ship.size - ship.hits for ship in player.ships)
    return current_health, total_health
