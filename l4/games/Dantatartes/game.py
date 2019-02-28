from random import choice

state = ['''
 *---*
    |
    |
    |
  =====''', '''
 *---*
 O   |
     |
     |
   =====''', '''
 *---*
 O   |
 |   |
     |
   =====''', '''
 *---*
 O   |
/|   |
     |
   =====''', '''
 *---*
 O   |
/|\  |
     |
   ===== ''', '''  
 *---*
 O  |
/|\ |
/   |
   =====''', '''
 *---*
 O  |
/|\ |
/ \ |
   ===='''][::-1]


class Game:

    def __init__(self, vocabulary=['игра', 'взрыв', 'яблоко', 'математика']):
        print("Игра виселица")

        # делает из 'игры' 'И Г Р У'
        def cook_vocab(raw_vocab):
            return [' '.join(word.upper()) for word in raw_vocab]

        # делает из 'И Г Р Ы' 'И _ _ У'
        def encode_word(word):
            word.upper()
            mid = word[1:-2]
            for i in range(len(mid)):
                if mid[i] is not " ":
                    mid = f"{mid[:i]}{'_'}{mid[i + 1:]}"
            mid = f'{mid}{" "}'

            return f"{word[0]}{mid}{word[-1]}"

        self.vocab = cook_vocab(vocabulary)
        self.__hp = 6
        self.__word = choice(self.vocab)
        self.__encoded_word = encode_word(self.__word)

    def play(self):
        print(state[self.__hp])
        print(self.__encoded_word)

        print("Введите предполагаемую букву:")
        letter = str(input()).upper()

        if letter in self.__word:
            print("Такая есть!")
            # Показывает все угаданные буквы
            for i in range(len(self.__word)):
                if letter == self.__word[i]:
                    self.__encoded_word = f"{self.__encoded_word[:i]}{letter}{self.__encoded_word[i + 1:]}"
        else:
            print("Такой буквы нет.")
            self.__hp -= 1

        if self.__word == self.__encoded_word:
            print(f"{self.__word}\nПоздравляю, вы выиграли!")
            exit()
        elif self.__hp < 0:
            print("Похоже, вы проиграли ):")
            exit()


def main():
    vocabulary = ['корабль', 'разочарование', 'вариативность', 'распределение',
                  'игра', 'взрыв', 'яблоко', 'математика', 'ирония', 'проигрыш']
    game = Game(vocabulary=vocabulary)
    while True:
        game.play()


if __name__ == '__main__':
    main()