import sys
from task_1 import K_MAX
from task_2 import f, Lagrange_polynom, sort_table, get_table
from prettytable import PrettyTable


def print_table_reversed(array):
    table = PrettyTable()
    table.field_names = ['', 'x_k', 'f^-1(x_k)']
    for i in range(0, len(array)):
        table.add_row([i + 1, array[i][0], array[i][1]])
    print(table)


def reverse_table(nodes):
    new_nodes = []
    for i in range(0, len(nodes)):
        new_nodes.append([nodes[i][1], nodes[i][0]])
    print('\nТаблица для обратной функции:')
    print_table_reversed(new_nodes)
    return new_nodes


def print_interpolation_polynom(nodes, x):
    result = Lagrange_polynom(nodes, x)
    print('\nQ_n(F) = ' + str(result)
          + '\n|f(x)-F| = ' + str(abs(f(result) - x)))
    return result


def interpolation_split_roots(nodes, F, a, b, n=100):
    h = (b - a) / n
    x1 = a
    x2 = x1 + h
    f1 = Lagrange_polynom(nodes, x1) - F
    sections = []
    counter = 0
    while counter < K_MAX:
        if x2 <= b:
            f2 = Lagrange_polynom(nodes, x2) - F
            if f1 * f2 <= 0:
                sections.append([x1, x2])
            x1 = x2
            x2 = x1 + h
            f1 = f2
        else:
            return sections
        counter += 1
    return sections


def interpolations_secants_method(nodes, F, sections, epsilon):
    roots = []
    for section in sections:
        x_0 = section[0]
        x_1 = section[1]
        counter = 0
        while counter < K_MAX:
            if abs(x_1 - x_0) < epsilon:
                break
            x_k = x_1 - ((Lagrange_polynom(nodes, x_1) - F) / ((Lagrange_polynom(nodes, x_1) - F) -
                                                               (Lagrange_polynom(nodes, x_0) - F))) * (x_1 - x_0)
            x_0 = x_1
            x_1 = x_k
            counter += 1
        roots.append(x_1)
    print('\nКорни уравнения P_n(x)=F: ')
    for i in range(0, len(roots)):
        print('x=' + str(roots[i]) + ', |f(x)-F| = ' + str(abs(f(roots[i]) - F)))
    return roots


def task3_1():
    print('___Задача обратного интерполирования___')
    m = int(input('\nЧисло значений в таблице (m+1): ')) - 1
    print('m = ' + str(m) + '\nОтрезок [a, b]:')
    a = float(input('a: '))
    b = float(input('b: '))
    table = get_table(m, [a, b])
    table_check = table.copy()
    table_check.sort(key=lambda x: x[1])
    table_check_1 = table.copy()
    table_check_1.sort(reverse=True, key=lambda x: x[1])
    first_method = False
    if table_check == table or table_check_1 == table:
        first_method = True
        print('\nФункция монотонна на промежутке, можем построить обратную функцию')
    else:
        print('\nФункция не монотонна на промежутке, не можем построить обратную фукнцию')
    while True:
        f_value = float(input('\nЗначение функции, для которого будем искать аргумент: '))

        if first_method:
            print('\nПервый способ: решаем задачу алгебраического интерполирования для f^-1')
            reversed_table = reverse_table(table)
            n = int(input('\nСтепень интерполяционного многочлена n (<= ' + str(m) + '): '))
            while n > m:
                n = int(input('Введите корректное значение (<= ' + str(m) + '): '))
            sorted_table = sort_table(reversed_table, f_value, [f_value - 1, f_value + 1])
            nodes = sorted_table[:(n + 1)]
            print_interpolation_polynom(nodes, f_value)

        print('\nВторой способ: строим интерполяционный многочлен и решаем ур-ние P_n(x)=F')
        epsilon = float(input('epsilon: '))
        sections = interpolation_split_roots(table, f_value, a, b)
        interpolations_secants_method(table, f_value, sections, epsilon)

        resp = input('\nХотите продолжить? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет' or resp == 'No' or resp == 'no':
            sys.exit()

task3_1()