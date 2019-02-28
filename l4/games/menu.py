'''
menu to run all games uniformely
'''
import os

games = (
    'YODAXYZ.main',
    'quhaaST.field_of_wonders',
    'Platun0v.game',
    'Dantatartes.game',
    'azatdavletshin.hangman'
)

def _int_input(text, exit_='exit'):
    while True:
        I = input(text).strip()
        if I == exit_:
            exit()

        if I.isnumeric():
            return int(I)
        print('Не понял...  нужно ввести число. Давайте еще раз')

def run_menu(games):
    print('Выберите игру:')
    for i, game in enumerate(games, 1):
        print(f'{i}. {game}')

    while True:
        I = _int_input('Введите номер игры. Для выхода напишите exit: ')
        print(len(games), I)
        if I > len(games) + 1:
            print(f'Нет такой игры: {I}! давай еще раз')
        else:
            exec(f'from {games[I-1]} import main; main()')
            


if __name__ == '__main__':
    run_menu(games)
    

