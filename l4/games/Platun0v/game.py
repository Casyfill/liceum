import os
from Platun0v import gallows_ascii
from Platun0v import words


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class Game:
    alphabet = list('abcdefghijklmnopqrstuvwxyz')

    def __init__(self, word):
        self.word = word
        self.unused_letters = self.alphabet.copy()
        self.not_guessed_letters = set(word)
        self.n_try = 0

    def start(self):
        while True:
            clear_console()
            print(gallows_ascii.lst[self.n_try])
            self.write_unused_letters()
            self.print_word()

            letter = read(lst=self.unused_letters, s_out="You have used this letter", letter=True)

            if letter in self.not_guessed_letters:
                self.not_guessed_letters.discard(letter)
                self.unused_letters.remove(letter)
                if len(self.not_guessed_letters) == 0:
                    self.win()
                    return
            else:
                self.unused_letters.remove(letter)
                self.n_try += 1
                if self.n_try == len(gallows_ascii.lst) - 1:
                    self.lose()
                    return

    def lose(self):
        clear_console()
        print(gallows_ascii.lst[-1])
        print("You lose. It was {}".format(self.word))

    def win(self):
        clear_console()
        print(gallows_ascii.win)
        print("You win. True, it was {}".format(self.word))

    def write_unused_letters(self):
        print('Unused letters')
        print('|'.join(self.unused_letters))

    def print_word(self):
        print('Word')
        for e in self.word:
            if e in self.not_guessed_letters:
                print('*', end='')
            else:
                print(e, end='')
        print()

# Philipp: абсолютно правильный подход, но тогда лоничго сделать
# единую функуцию чтения/лупа, и ее так или иначе модифицировать (или ей передавать метод валидации строки )
# чем несколько отдельных функций городить
def read_num(s='> '): 
    while True:
        n = input(s)
        try:
            n = int(n)
            return n
        except ValueError:
            print('Invalid value entered')


def read_letter(s='> '):
    while True:
        letter = input(s)
        if len(letter) != 1:
            print('Invalid value entered')
            continue

        letter = letter.lower()
        if 'a' <= letter <= 'z':
            pass
        else:
            print('Invalid value entered')
            continue

        return letter


def read(from_=None, to=None, lst=None, s_in='> ', s_out='Unexpected value', letter=False, num=False):
    if lst is None:
        if isinstance(from_, str):
            lst = [chr(i) for i in range(ord(from_), ord(to) + 1)]
        elif isinstance(from_, int):
            lst = [i for i in range(from_, to + 1)]

    if letter:
        fun = read_letter
    elif num:
        fun = read_num
    else:
        fun = input

    while True:
        inp = fun(s_in)
        if inp in lst:
            return inp
        else:
            print(s_out)


def play_game():  # renamed for consistency
    categories = {i: e for i, e in enumerate(words.urls_by_categories.keys())}
    for key, elem in categories.items():
        print(f'[{key}] -> {elem}')

    print('Choose the theme')

    num = read(from_=0, to=len(categories) - 1, num=True)
    category = categories[num]

    word = words.get_word(category)
    game = Game(word)
    game.start()

    letter = read(lst=['y', 'n', 'Y', 'N'],  #
                  s_in='Want to play again? [Y/n] ',
                  letter=True).lower()
    if letter == 'n':
        exit()

def main():
    while True:
        play_game()


if __name__ == '__main__':
    main()
