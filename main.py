from csv import reader
from datetime import datetime
import xml.dom.minidom as minidom
import os


def open_table():
    try:
        with open('books.csv', 'r', encoding='cp1251') as csvfile:
            table = list(reader(csvfile, delimiter=';'))
            table = table[1:]
            return table
    except FileNotFoundError:
        print('Файл не найден!')
        return 0


def get_year(string):
    #дата "19.10.2026 9:22"
    date = datetime.strptime(string.split(' ')[0], '%d.%m.%Y')
    return date.year


#Вывод количества записей, у которых в поле Название строка длиннее 30 символов
def count_long(table):
    count = 0
    for row in table:
        if len(row[1]) > 30:
            count += 1
    print(f'Записей с названием длиннее 30 символов: {count}')
    input('Нажмите Enter')


#Поиск книги по автору от 2016 до 2018 года
def search(table):
    searchline = input('Введите автора: ')
    if searchline in ['0', '']:
        return 0
    elif searchline.isalpha() == False:
        return 0
    flag = 0
    for row in table:
        year = get_year(row[6])
        if year < 2016 or year > 2018:
            continue
        if find_string(searchline, row[3]) != -1:
            print(f'{row[3]}. {row[1]} - {year}')
            flag += 1
    if flag == 0:
        print('Ничего не найдено!')
    else:
        print(f'Найдено позиций: {flag}')
    input('Нажмите Enter')


def find_string(searchline, string):
    string = string.lower()
    index = string.find(searchline.lower())
    return index


#Генератор библиографических ссылок для 20 записей
def bib_links(table):
    good = []
    for row in table:
        if row[3] != '':
            good.append(row)
    chosen = good[::5][:20]
    output = open('result.txt', 'w', encoding='utf-8')
    number = 1
    for row in chosen:
        line = f'{number}. {row[3]}. {row[1]} - {get_year(row[6])}'
        print(line)
        output.write(line + '\n')
        number += 1
    output.close()
    print('Список сохранён в result.txt')
    input('Нажмите Enter')


#Список CharCode, но только для валют с Nominal=10 или Nominal=100
def parse_xml():
    try:
        xml_file = open('currency.xml', 'r', encoding='cp1251')
    except FileNotFoundError:
        print('Файл не найден!')
        return 0
    xml_data = xml_file.read()

    dom = minidom.parseString(xml_data)
    dom.normalize()

    elements = dom.getElementsByTagName('Valute')
    codes = []

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'CharCode':
                        if child.firstChild.nodeType == 3:
                            char_code = child.firstChild.data
                if child.tagName == 'Nominal':
                    if child.firstChild.nodeType == 3:
                        nominal = int(child.firstChild.data)
        if nominal == 10 or nominal == 100:
            codes.append(char_code)


    print('Валюты с номиналом 10 или 100:')
    print(' '.join(codes))
    input('Нажмите Enter')

    xml_file.close()


#Перечень всех тегов без повторений
def unique_tags(table):
    tags = set()
    for row in table:
        for tag in row[12].split('#'):
            tag = tag.strip() #убираем пробелы в начале и конце строки
            if tag != '':
                tags.add(tag)
    for tag in sorted(tags):
        print(tag)
    print(f'Всего уникальных тегов: {len(tags)}')
    input('Нажмите Enter')


#Самые популярные 20 книг
def top_books(table):
    books = {}
    for row in table:
        key = (row[1], row[3]) #ключ- кортеж из названия и автора
        books[key] = books.get(key, 0) + int(row[8])
    result = []
    for key in books:
        result.append([books[key], key[0], key[1]])
    result.sort(reverse=True) #по убыванию
    number = 1
    for i in result[:20]:
        print(f'{number}. {i[2]}. {i[1]} - выдач: {i[0]}')
        number += 1
    input('Нажмите Enter')


while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    if open_table() == 0:
        break
    print('Меню:\n1 - Названия > 30 символов\n2 - Поиск по автору\n'
          '3 - Библиографические ссылки\n4 - Валюты Nominal 10 или 100\n'
          '5 - Теги без повторений\n6 - Топ 20 книг\n0 - Выход')
    menu = input('Выберите пункт меню: ')
    match menu:
        case '1':
            count_long(open_table())
        case '2':
            search(open_table())
        case '3':
            bib_links(open_table())
        case '4':
            parse_xml()
        case '5':
            unique_tags(open_table())
        case '6':
            top_books(open_table())
        case '0':
            break
        case _:
            print('Нет пункта меню, нажмите Enter')
            input()