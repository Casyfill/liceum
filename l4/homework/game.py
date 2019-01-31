''' пример игры для вашего домашнего задания. 
Используйте любые части кода чтобы создать вашу собственную игру.
'''
RULES = '''
Игра "Угадай число".

Компьютер загадывает число от 1 до 10 включительно. Ваша задача - угадать число
за минимум попыток. если вы не угадаете число за 6 попыток, вы проиграли.

Если вы не угадали, но число попыток < 6, компьютер сообщит вам, 
больше ли секретное число чем ваша попытка, или меньше.'''
import random
# from colorama import init, Fore, Back, Style



def get_input(question:str):
    first_try = True

    while True:
        I = input(question if first_try else '\nОтвет должен быть целым числом!').strip()
        if I.isnumeric():
            return int(I)
        elif I == 'exit':
            print('До свидания!')
            exit()

        first_try = False
        
    

def main():
    print(RULES)
    secret_number = random.randint(1, 10)
    counter = 0
    max_tries = 6

    while counter <= 6+1:
        counter += 1

        guess = get_input(f'\nПопытка {counter}. Какое число попробуем?')

        if guess == secret_number:
            print(f'Правильно! Вы выиграли всего c {counter} попыток! Сможете быстрее?')
            exit()  # или можно спросить, не хочет ли еще раз сыграть
        elif secret_number < guess:
            print('Нет, загадонное число меньше!')
        else:
            print('Нет, загадонное число больше!')


if __name__ == '__main__':
    main()