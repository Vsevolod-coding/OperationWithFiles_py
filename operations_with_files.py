'''
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
'''
from csv import DictReader, DictWriter
from os.path import exists
from termcolor import colored

class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt

def get_info():
    flag = False
    while not flag:
        try:
            first_name = input('Имя: ' )
            if len(first_name) < 2:
                raise NameError('Слишком короткое имя.')
            second_name = input('Введите фамилию: ')
            if len(second_name) < 4:
                raise NameError('Слишком короткая фамилия.')
            phone_number = input('Введите номер телефона: ')
            if len(phone_number) < 11:
                raise NameError('Слишком короткий номер телефона.')
        except NameError as err:
            print(err)
        else:
            flag = True
    return [first_name, second_name, phone_number]

def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()

def write_file(file_name):
    user_data = get_info()
    res = read_file(file_name)
    new_obj = {'first_name': user_data[0], 'second_name': user_data[1], 'phone_number': user_data[2]}
    res.append(new_obj)
    standart_write(file_name, res)
    

def read_file(file_name):
    with open(file_name, encoding='utf-8') as data:
        f_r = DictReader(data)
        return list(f_r) #ящик со словарями


# ДЗ - КОПИРОВАНИЕ ДАННЫХ В ДРУГОЙ ФАЙЛ
def copy_data(src_file, dest_file):
    try:
        src_data = read_file(src_file)
        if not src_data:
            print(colored('Исходный файл пуст или не существует.', 'red'))
            return

        line_number = int(input('Введите номер строки для копирования: '))

        if line_number < 1 or line_number > len(src_data):
            print(colored(f'Введите правильный номер строки от 1 до {len(src_data)}.', 'red'))
            return
        
        row_to_copy = src_data[line_number - 1]

        if exists(dest_file):
            dest_data = read_file(dest_file)
        else:
            dest_data = []
        
        dest_data.append(row_to_copy)
        standart_write(dest_file, dest_data)

        print(colored('Строка успешно скопирована.', 'green'))
    
    except ValueError:
        print(colored('Введите корректное число.', 'red'))
# ДЗ - КОПИРОВАНИЕ ДАННЫХ В ДРУГОЙ ФАЙЛ


def remove_row(file_name):
    search = int(input('Введите номер строки для удаления: '))
    res = read_file(file_name)
    if search <= len(res):
        res.pop(search - 1)
        standart_write(file_name, res)
    else:
        print(colored(f'Введите другую строку из доступных: {len(res)}', 'red'))


def standart_write(file_name, res):
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
        f_w.writerows(res)

file_name = 'phone.csv'
dest_file_name = 'phone_2.csv'

def main():
    while True:
        command = input(colored('Введите команду: ', 'blue'))
        if command == 'info':
            print(colored('\nСписок команд:', 'black', 'on_white'))
            print('\nw - запись данных\nr - вывод данных на экран\nc - копирование данных из одного файла в другой\ndel - удаление введенной строки в файле\nq - завершение программы\n')
        if command == 'q':
            print(colored('Программа успешно закрылась.', 'blue'))
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
        elif command == 'r':
            if not exists(file_name):
                print(colored('Файла нет, создайте его.', 'red'))
                continue
            print(*read_file(file_name))
        elif command == 'del':
            if not exists(file_name):
                print(colored('Файла нет, создайте его.', 'red'))
                continue
            remove_row(file_name)
        elif command == 'c':
            if not exists(file_name):
                print(colored('Исходного файла нет, создайте его.', 'red'))
                continue
            copy_data(file_name, dest_file_name)

main()

'''
копирование из файла А в файл Б
написать отдельную фукнкцию copy_data
прочитать список словарей
записать его в новый файл используя функцию standart_write
дополнить функцию main
из phone.csv в phone_2.csv
'''