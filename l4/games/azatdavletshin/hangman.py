import os
import random

pics = ['''
=========''', '''
       
       |
       |
       |
       |
       |
=========''', '''
    ---+   
       |
       |
       |
       |
       |
=========''', '''
   +---+
   |   |
       |
       |
       |
       |
=========''', '''
   
   +---+
   |   |
   0   |
       |
       |
       |
=========''', '''
   +---+
   |   |
   0   |
  /|\  |
       |
       |
=========''', '''
   +---+
   |   |
   0   |
  /|\  |
  / \  |
       |
=========''']

words = 'БИЗОН ДЕЛЬФИН ОМАР ОБЕЗЬЯНА ОРЕЛ ПОНИ КОРОВА ЛОШАДЬ ОЛЕНЬ УТКА ГУСЬ КУРИЦА КРОЛИК ЗАЯЦ ПАУК ВОЛК ЛИСА МЕДВЕДЬ ' \
        'ЛЕВ СВИНЬЯ ТИГР ЗМЕЯ АКУЛА РЫБА ЛОСОСЬ ОКУНЬ ПЕТУХ КОШКА СОБАКА ВОРОНА ГОЛУБЬ УЖ ПИТОН ФУТБОЛ ВОЛЕЙБОЛ БАСКЕТБОЛ' \
        'ПЛАВАНЬЕ ТЕННИС ГИМНАСТИКА ТЕТРАДЬ ШКОЛА ПАРТА СТОЛ СТУЛ КРОВАТЬ ВОДОПАД'.split()

letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'


def check_letter(let, w, dict, z, x, array):
    let.upper()
    array.append(let)
    if let in w:
        dict[let] = 1
        z += 1
        return 1
    elif x == 6:
        print(pics[x])
        return 0
    else:
        print(pics[x])
        x += 1
        print("Этой буквы нет, попробуйте еще раз!")
        return 0

def players(p, pl2):
    if p == 2:
        print(pl2, ', ', 'угадайте букву:', sep='')
    else:
        print("Угадайте букву:")

def main():  # changed by Philipp Kats for consistency

    # Philipp: lambda assignment is considered bad practice
    console_clear = lambda: os.system('cls')  # also cls is not a sh command - not compatible!

    guessed_letters = {}  # moved by Philipp Kats for consistency
    numbers_of_steps = 0
    remaining_attempts = 0
    used_letters = []
    rus_let = 0

    player2 = '0'
    number_of_players = 0
    while number_of_players != 1 and number_of_players != 2:
        print("Введите количество игроков(1 или 2):")
        number_of_players = int(input())
    if number_of_players == 2:
        print("Введите имя первого игрока:")
        player1 = input()
        print("Введите имя второго игрока:")
        player2 = input()
        print(player1, "загадайте слово:")
        word = input().upper()
        while rus_let != len(word):
            rus_let = 0
            for i in range(len(word)):
                if word[i] in letters:
                    rus_let += 1
            if rus_let == len(word):
                break
            print("Введите слово, состоящее только из русских букв")
            word = input().upper()
        print("Нажмите Enter и передайте ход второму игроку")
        input()
    else:
        j = random.randint(0, len(words)-1)
        word = words[j]
    console_clear()
    while remaining_attempts != 7:
        players(number_of_players, player2)
        letter = input().upper()
        while letter not in letters or len(letter) != 1:
            print("Неправильный формат ввода, введите букву русского алфавита")
            letter = input().upper()
        while letter in used_letters:
            print("Эта буква была, попробуйте другую")
            letter = input().upper()
        if check_letter(letter, word, guessed_letters, numbers_of_steps, remaining_attempts, used_letters) == 1:
            numbers_of_steps += 1
        else:
            remaining_attempts += 1
        check_guessed_letters = 0
        for i in range(len(word)):
            if word[i] in guessed_letters.keys():
                print(word[i], end='')
                check_guessed_letters += 1
            else:
                print("_", end='')
        if check_guessed_letters == len(word):
            print()
            print("Поздравляем, вы справились за", remaining_attempts + numbers_of_steps, "ходов!!!")
            exit()
        print()
    print("К сожалению вы проиграли, удачи в следующий раз!")
    print("Было загадано слово:", word)


if __name__ == '__main__':
    main()