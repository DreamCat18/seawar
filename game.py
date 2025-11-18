from player import Player


class BattleshipGame:
    def __init__(self):
        self.players = []
        self.current_player_index = 0

    def setup_players(self):
        """Настройка игроков"""
        print("Добро пожаловать в Морской бой!")

        # Создание игроков
        player1_name = input("Введите имя первого игрока: ") or "Игрок 1"
        player2_name = input("Введите имя второго игрока: ") or "Игрок 2"

        self.players.append(Player(player1_name))
        self.players.append(Player(player2_name))

        # Выбор режима размещения кораблей
        for i, player in enumerate(self.players):
            print(f"\n{player.name}, выберите способ размещения кораблей:")
            print("1 - Автоматически")
            print("2 - Вручную")

            choice = input("Ваш выбор (1/2): ")

            if choice == "1":
                success = player.auto_place_ships()
                if not success:
                    print("Ошибка при автоматическом размещении!")
                    return False
            else:
                player.manual_place_ships()

            print(f"\nКорабли {player.name} размещены!")

        return True

    def switch_player(self):
        """Смена текущего игрока"""
        self.current_player_index = 1 - self.current_player_index

    def get_current_player(self):
        """Получение текущего игрока"""
        return self.players[self.current_player_index]

    def get_opponent(self):
        """Получение противника"""
        return self.players[1 - self.current_player_index]

    def play_turn(self):
        """Очередь хода"""
        current_player = self.get_current_player()
        opponent = self.get_opponent()

        current_player.display_boards()

        print(f"\nХодит {current_player.name}!")

        valid_attack = False
        while not valid_attack:
            try:
                x = int(input("Введите координату X для атаки: "))
                y = int(input("Введите координату Y для атаки: "))

                result = opponent.board.receive_attack(x, y)

                if result == "invalid":
                    print("Неверные координаты! Попробуйте снова.")
                elif result == "already_attacked":
                    print("Вы уже атаковали эту клетку! Попробуйте снова.")
                elif result == "miss":
                    print("Промах!")
                    valid_attack = True
                elif result == "hit":
                    print("Попадание!")
                    valid_attack = True
                elif result == "hit_sunk":
                    print("Попадание! Корабль потоплен!")
                    valid_attack = True

                # Обновляем доску противника у текущего игрока
                current_player.enemy_board = opponent.board

            except ValueError:
                print("Пожалуйста, введите корректные числа!")

    def check_win_condition(self):
        """Проверка условия победы"""
        opponent = self.get_opponent()
        return opponent.board.all_ships_sunk()

    def play_game(self):
        """Основной игровой цикл"""
        if not self.setup_players():
            return

        game_over = False

        while not game_over:
            self.play_turn()

            if self.check_win_condition():
                winner = self.get_current_player()
                print(f"\nПоздравляем! {winner.name} победил!")
                game_over = True
            else:
                self.switch_player()

        # Показать финальные доски
        for player in self.players:
            print(f"\nФинальная доска {player.name}:")
            player.board.display(show_ships=True)
