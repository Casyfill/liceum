from YODAXYZ import toetic as tic
from YODAXYZ import weather as weather
from YODAXYZ import blackJack as blackJack


class StartMenu(object):
    """  Start menu  """
    choice = 0  # chose menu
    game_choice = 0
    c = {
    }

    def greeting(self):
        print("Hello !!!")

    def que_menu(self):
        """  Text for menu in class start_game  """
        print("1) Game")
        print("2) Weather")
        while True:
            try:
                self.choice = int(input())
                if self.choice not in [1, 2]:
                    v = 1 / 0# when you get to know how to throw exception do that
                break
            except:
                pass

        if self.choice == 1:
            print('1) Tic tac toe')
            print('2) BlackJack')
            while True:
                try:
                    self.game_choice = int(input())
                    if self.game_choice not in [1, 2]:
                        v = 1 / 0  # when you get to know how to throw exception do that
                    break
                except:
                    pass

            if self.game_choice == 1:
                tic.main()
            if self.game_choice == 2:
                blackJack.new_game()
        if self.choice == 2:
            weather.main()


def main():
    game = StartMenu()
    game.greeting()
    game.que_menu()


if __name__ == '__main__':
    main()
