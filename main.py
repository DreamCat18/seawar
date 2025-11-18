from game import BattleshipGame


def main():
    while True:
        game = BattleshipGame()
        game.play_game()

        play_again = input("\nХотите сыграть еще раз? (y/n): ").lower()
        if play_again != 'y':
            print("Спасибо за игру!")
            break


if __name__ == "__main__":
    main()
