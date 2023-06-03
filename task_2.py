import math
from prettytable import PrettyTable


def f(x):
    return math.log(1+x)


def print_table(array):
    table = PrettyTable()
    table.field_names = ['', 'x_k', 'f(x_k)']
    for i in range(0, len(array)):
        table.add_row([i + 1, array[i][0], array[i][1]])
    print(table)


def get_table(m, section):
    nodes = []
    a = section[0]
    b = section[1]
    for k in range(0, m + 1):
        x_k = a + (b - a) / m * k
        x_k = round(x_k, 5)
        nodes.append([x_k, f(x_k)])
    print('\nТаблица значений:')
    print_table(nodes)
    return nodes


def insert_node(array, element, x):
    abs_value = abs(element[0] - x)
    for i in range(0, len(array)):
        if abs_value < abs(array[i][0] - x):
            array.insert(i, element)
            return array
    array.append(element)
    return array


def sort_table(nodes, x, section):
    nodes_sorted = []
    a = section[0]
    b = section[1]
    if x <= a:
        nodes_sorted = nodes
    elif x >= b:
        nodes_sorted = nodes.copy()
        nodes_sorted.sort(reverse=True)
    else:
        nodes_sorted.append(nodes[0])
        for i in range(1, len(nodes)):
            nodes_sorted = insert_node(nodes_sorted, nodes[i], x)
    print('\nОтсортированная таблица')
    print_table(nodes_sorted)
    return nodes_sorted


def Lagrange_polynom(nodes, x):
    result = 0
    n = len(nodes)
    for k in range(0, n):
        multiplier = 1
        for j in range(0, n):
            if j == k:
                continue
            multiplier *= (x - nodes[j][0]) / (nodes[k][0] - nodes[j][0])
        multiplier *= nodes[k][1]
        result += multiplier
    return result


def print_Lagrange_polynom(nodes, x):
    result = Lagrange_polynom(nodes, x)
    print('\nПолином в форме Лагранжа:\nP_n(x) = ' + str(result)
          + '\n|f(x)-P_n(x)| = ' + str(abs(result - f(x))))
    return result


def div_diff(nodes, i, j=0):
    if i == j:
        return nodes[i][1]
    if (i - j) == 1:
        return (nodes[i][1] - nodes[j][1]) / (nodes[i][0] - nodes[j][0])
    return (div_diff(nodes, i, j + 1) - div_diff(nodes, i - 1, j)) / (nodes[i][0] - nodes[j][0])


def Newton_polynom(nodes, x):
    result = div_diff(nodes, 0)
    for k in range(1, len(nodes)):
        a_k = div_diff(nodes, k)
        for i in range(0, k):
            a_k *= (x - nodes[i][0])
        result += a_k
    return result


def print_Newton_polynom(nodes, x):
    result = Newton_polynom(nodes, x)
    print('\nПолином в форме Ньютона:\nP_n(x) = ' + str(result)
          + '\n|f(x)-P_n(x)| = ' + str(abs(result - f(x))))
    return result


def task2():
    print('___Задача алгебраического интерполирования___\nВариант 2\nf(x) = ln(1+x))')
    m = int(input('\nЧисло значений в таблице (m+1): ')) - 1
    print('m = ' + str(m) + '\nОтрезок [a, b]:')
    a = float(input('a: '))
    b = float(input('b: '))
    table = get_table(m, [a, b])
    repeat = True
    while repeat:
        x = float(input('\nТочка интерполирования: '))
        n = int(input('\nСтепень интерполяционного многочлена n (<= ' + str(m) + '): '))
        while n > m:
            n = int(input('Введите корректное значение (<= ' + str(m) + '): '))
        table_sorted = sort_table(table, x, [a, b])
        nodes = table_sorted[:(n + 1)]
        print_Lagrange_polynom(nodes, x)
        print_Newton_polynom(nodes, x)
        resp = input('\nХотите ввести новые значения x и n? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет':
            repeat = False

task2()