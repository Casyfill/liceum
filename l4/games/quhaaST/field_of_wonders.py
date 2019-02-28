import os
from random import randint, choice
from collections import deque
from time import sleep
from pathlib import Path

# очищаем консоль
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


# бордер, обозначающий конец хода
def border():
    for i in range(110):
        print('-', end='')
    print()
    sleep(1.5)


# круть анимация
def round_animation():
    for i in range(3):
        print('*круть*')
        sleep(0.8)


class Game:
    letters = list('абвгдежзиклмнопрстуфхцчшщьыъэюя')
    drum_variants = [600, 800, '+1', 400, 900, 0, 'П', 500, 300, 200, 'x3', 700, 'Б', 1000, 100, 'x2']
    score = 0

    # сама игра
    # Philipp: у вас нет функции __init__;
    # конечно, она есть у класса-щаблона, но было бы логичнно туда убрать все self.question=question, и так далее.

    def start_game(self, word, question):
        clear_console()
        self.question = question
        need_word = list(word)
        unused_letters_list = self.letters.copy()
        guessed_letters = [0] * len(need_word)
        greet()
        player_name = get_name()
        players = [player_name, 'Женя', 'Виктор']
        current_player_id = randint(0, 2)
        print('Что же, начнём нашу игру!')
        print('А вот и задание:', question)

        while True:
            border()
            print('Напишите "задание", если нужно повторить задание.')
            sleep(1)
            current_player_name = players[current_player_id]
            if current_player_name == player_name:
                print('ВАШ ХОД')
            print('----', f'{current_player_name}, крутите барабан!', '----', sep='')
            sleep(1)
            round_animation()
            drum_result = self.round_drum()
            if drum_result == '+1':                        # проверка выпадения +1 на барабане
                self.print_word(need_word, guessed_letters)
                if current_player_name == player_name:
                    num = read_num(guessed_letters)
                    letter_to_show = need_word[num]
                    for i in range(len(need_word)):
                        if need_word[i] == letter_to_show:
                            guessed_letters[i] = 1
                else:
                    letter_to_show = self.rand_num(guessed_letters)
                print('Откройте букву ', letter_to_show)
                continue

            self.print_word(need_word, guessed_letters)
            self.unused_letters(unused_letters_list)
            if current_player_name == player_name:
                while True:
                    input_letter = read_letter()
                    if input_letter in unused_letters_list:
                        break
                    else:
                        print('Эта буква уже была использована!')
            else:
                sleep(3)
                input_letter = self.auto_choose(unused_letters_list)

            print(f"Вы выбрали букву '{input_letter}', и... ")
            sleep(3)

            if input_letter in need_word:                 # проверка на наличие буквы в слове
                print('Верно!')
                sleep(1)
                print('Вы получаете обещанную награду.')
                unused_letters_list.remove(input_letter)
                for i in range(len(guessed_letters)):
                    if need_word[i] == input_letter:
                        guessed_letters[i] = 1
                if current_player_name == player_name:
                    if isinstance(drum_result, int):
                        self.score += drum_result
                    else:
                        if drum_result == 'x2':
                            self.score *= 2
                        elif drum_result == 'x3':
                            self.score *= 3
                        elif drum_result == 'П':
                            print('Приз или деньги? [1|2]')
                            if current_player_name != player_name:
                                sleep(1)
                                print('Вы получаете 5000 рублей! Какое везение.')
                            decision = read_prize_or_money()
                            if decision == 1:
                                print('Так...')
                                sleep(1)
                                print('Вы выиграли соленья! Ха-ха-ха.')
                            else:
                                print('На нет и суда нет. Вы получаете 5000 рублей!')
                        elif drum_result == 'Б':
                            self.score = 0
                            continue
            else:
                print('К сожалению такой буквы нет.')
                current_player_id += 1
                if current_player_id > 2:
                    current_player_id = 0
                unused_letters_list.remove(input_letter)

            end_of_game = self.check_word_guessness(word, guessed_letters)
            if end_of_game:                                 # проверка на отгаданность слова
                sleep(3)
                if current_player_name == player_name:
                    print(f'Поздравляю Вас с победой, {player_name}! Ваш счет равен {self.score}.',
                          ' Ждём Вас в следующей игре.', sep='\n')
                else:
                    print(f'Итак, в сегодняшней игре выиграл игрок {current_player_name}.',
                          'На этом наше мероприятие заканчивается.', sep='\n')
                break
            sleep(3)

    # кручение барабана
    def round_drum(self):
        value_out = {
            600: 'Вы получите 600 очков, если верно откроете букву.',
            800: 'Вы получите 800 очков, если верно откроете букву.',
            400: 'Вы получите 400 очков, если верно откроете букву.',
            900: 'Вы получите 900 очков, если верно откроете букву.',
            0: 'Упс... Вы ничего не получите, если верно откроете букву.',
            500: 'Вы получите 500 очков, если верно откроете букву.',
            300: 'Вы получите 300 очков, если верно откроете букву.',
            200: 'Вы получите 200 очков, если верно откроете букву.',
            1000: 'Вы получите целую 1000 очков, если верно откроете букву.',
            100: 'Вы получите 100 очков, если верно откроете букву.',
            700: 'Вы получите 700 очков, если верно откроете букву.',
            '+1': 'Ого! Выбирайте номер буквы, которую вы хотите открыть.',
            'П': 'Вы можете выиграть приз или деньги за правильный ответ!',
            'Б': 'Оу... Как не повезло. К сожалению, Вы теперь банкрот.',
            'x3': 'Вау, количество ваших очков увеличится в 3 раза, если Вы верно откроете букву.',
            'x2': 'Вау, количество ваших очков удвоится, если Вы верно откроете букву.'
        }
        rand_value = randint(1, 12)
        deq = deque(self.drum_variants)  # Philipp - игш
        deq.rotate(rand_value)
        self.drum_variants = list(deq)
        print(f'Сектор {self.drum_variants[0]} на барабане!')
        print(value_out[self.drum_variants[0]])
        return self.drum_variants[0]

    # вывод доступных для выбора букв
    def unused_letters(self, unused_letters_list):
        list_size = len(unused_letters_list)
        print('Выберите желаемую букву из списка доступных: ', end='')
        for i in range(list_size - 1):
            print(unused_letters_list[i], '|', end='', sep='')
        print(unused_letters_list[list_size - 1])

    # вывод табла с открытыми/закрытыми буквами
    def print_word(self, word_in, guessed_letters):
        sleep(2)
        print('Табло: |', end='')
        for i in range(len(word_in)):
            if guessed_letters[i] == 1:
                print(word_in[i], end='')
            else:
                print('*', end='')
        print('|')

    # проверка, если слово отгадано
    def check_word_guessness(self, word_in, guessed_letters):
        flag = True
        for i in range(len(guessed_letters)):
            if guessed_letters[i] == 0:
                flag = False
        if flag:
            print(f'Браво! Вы отгадали слово. Правильный ответ действительно "{word_in}".')
            return True
        else:
            return False

    # выбор буквы для открытия (ботом)
    def auto_choose(self, unused):
        unused_letters_num = len(unused)
        return unused[randint(0, unused_letters_num - 1)]

    # выбор номера буквы для показа (ботом)
    def rand_num(self, guessed):
        unguessed_letters = []
        for i in range(len(guessed)):
            if guessed[i] == 0:
                unguessed_letters.append(i + 1)
        num_to_open = choice(unguessed_letters)
        return num_to_open


# приветствие
def greet():
    print('Добро пожаловать на "Поле Чудес"!')
    sleep(2)


# считывание имени игрока
def get_name():
    print('Как Вас зовут, мой дорогой друг?')
    while True:
        name = input()
        if len(name) <= 1:
            print('Пожалуйста, введите своё имя')
        else:
            if any(map(str.isdigit, name)):
                print('Имя не должно содержать цифр!')
            else:
                return name


# считывание буквы для ответа
def read_letter():
    while True:
        letter = input()
        if letter == 'задание' or letter == 'Задание':  # PHILIPP: может лучше просто все в ловер кейс сразу?
            show_question()
            sleep(2)
            print('Итак, Ваша буква?')  # не проверяет на английские буквы
            continue
        if len(letter) != 1:
            print('Введите только одну букву!')
        else:
            if letter.lower() in list('абвгдежзиклмнопрстуфхцчшщьыъэюя'):
                return letter.lower()
            else:
                print('Введите русскую букву!')

# ввод числа для выбора приза или денег
def read_prize_or_money():
    while True:
        number_in = input()
        try:
            number_in = int(number_in)
            if number_in == 1 or number_in != 2:
                return number_in
            else:
                print('Введите 1 или 2')
        except:
            print('Введите число!')


# считывание номера буквы для открытия
def read_num(guessed_nums):
    sleep(2)
    while True:
        num = input()
        try:
            num = int(num)
        except:
            print('Введите число!')
        if isinstance(num, int):
            if guessed_nums[num - 1] == 0:
                return num - 1
            else:
                print('Буква под этим номером уже известна.')


#повторение задания
def show_question():
    print('Повторю задание:', quest)

questions_path = Path(__file__).parent / 'questions.txt'
with questions_path.open('r', encoding='utf8') as f:
    file = f.read()

keys_list = []
values_list = []
cnt = 0

# Тут мы считываем слово   
# Philipp: а ведь можно было просто после вопроса через запятую или пайп (|) написать, и потом делить
# ~ 10 строк короче было бы
for line in file:
    line = line.strip()
    if cnt % 2 == 0:
        values_list.append(line)
    else:
        keys_list.append(line.lower())
    cnt += 1

words_map = dict()

for i in range(len(keys_list)):
    words_map[keys_list[i]] = values_list[i]

wished_word_index = randint(0, len(keys_list) - 1)  # Philipp: неправильно, таким образом последний вопрос никогда не задан
wished_word = keys_list[wished_word_index]
quest = values_list[wished_word_index]  # Philipp: вообще раз уж есть класс игры, лучше это хранить там - иначе вопрос выбирается раз на ран скрипта


def main():  # added by Philipp Kats
    print(wished_word, quest)
    game = Game()
    game.start_game(wished_word, quest)


if __name__ == '__main__':
    main()
