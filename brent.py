# Базовые функции брента
import random

def kukarek(file):  # брент говорить
    f = open(file, encoding='utf-8').read().splitlines()
    return random.choice(f)


def kukareku(file, num):  # брент давать пронумерованую строку
    f = open(file, encoding='utf-8').readlines()
    return f[num]


def kudah(file, text):  # Брент записывать
    f = open(file, 'a+', encoding='utf-8')
    f.write(text)
    f.close()


def pokpok(file, name):  # Брент вычеркивать
    f = open(file, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    f = open(file, 'w', encoding='utf-8')
    for line in lines:
        if line != name:
            f.write(line)
    f.close()


def is_number(num):  # проверка конвертируемости стрингов в числа
    try:
        int(num)
        return True
    except ValueError:
        return False


def file_len(fname):  # кол-во строчек в файле
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def check_in(mystr, mylist):
    for line in mylist:
        if mystr.find(line) != -1:
            return True
    return False


def file_to_list(file):
    try:
        f = open(file, encoding='utf-8').read().splitlines()
        return f
    except FileNotFoundError:
        return []