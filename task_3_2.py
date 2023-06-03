import sys
import math
from task_2 import print_table
from prettytable import PrettyTable


def f(x):
    return math.exp(4 * x)


def f_deriv(x):
    return 4 * math.exp(4 * x)


def f_second_deriv(x):
    return 4 * 4 * math.exp(4 * x)


def get_diff_table(m, a, h):
    nodes = []
    for k in range(0, m + 1):
        x_k = a + k * h
        nodes.append([x_k, f(x_k)])
    print('\nТаблица значений:')
    print_table(nodes)
    return nodes


def print_derivatives_table(nodes, first_derivatives, second_derivatives):
    table = PrettyTable()
    table.field_names = ['x_i', 'f`(x_i)', 'Невязка f`', 'f``(x_i)', 'Невязка f``']
    for i in range(0, len(nodes)):
        table.add_row([nodes[i][0], first_derivatives[i][0], first_derivatives[i][1],
                       second_derivatives[i][0], second_derivatives[i][1]])
    print(table)


def print_right_difference(nodes, h):
    print("\nПравая разностная производная")
    first_derivatives = []
    second_derivatives = []
    nodes_modified = nodes.copy()
    for i in range(2):
        nodes_modified.append([nodes_modified[-1][0] + h, f(nodes_modified[-1][0] + h)])
    for j in range(len(nodes_modified) - 1):
        f_j = (nodes_modified[j + 1][1] - nodes_modified[j][1]) / h
        first_derivatives.append([f_j, abs(f_j - f_deriv(nodes_modified[j][0]))])
    for k in range(len(first_derivatives) - 1):
        f_kk = (first_derivatives[k + 1][0] - first_derivatives[k][0]) / h
        second_derivatives.append([f_kk, abs(f_kk - f_second_deriv(nodes[k][0]))])
    print_derivatives_table(nodes, first_derivatives[:len(nodes)], second_derivatives)


def print_left_difference(nodes, h):
    print("\nЛевая разностная производная")
    first_derivatives = []
    second_derivatives = []
    nodes_modified = nodes.copy()
    for i in range(2):
        nodes_modified.insert(0, [nodes_modified[0][0] - h, f(nodes_modified[0][0] - h)])
    for j in range(1, len(nodes_modified)):
        f_j = (nodes_modified[j][1] - nodes_modified[j - 1][1]) / h
        first_derivatives.append([f_j, abs(f_j - f_deriv(nodes_modified[j][0]))])
    for k in range(1, len(first_derivatives)):
        f_kk = (first_derivatives[k][0] - first_derivatives[k - 1][0]) / h
        second_derivatives.append([f_kk, abs(f_kk - f_second_deriv(nodes[k - 1][0]))])
    print_derivatives_table(nodes, first_derivatives[1:], second_derivatives)


def print_central_difference(nodes, h):
    print("\nЦентральная разностная производная")
    first_derivatives = []
    second_derivatives = []
    nodes_modified = nodes.copy()
    for i in range(2):
        nodes_modified.insert(0, [nodes_modified[0][0] - h, f(nodes_modified[0][0] - h)])
        nodes_modified.append([nodes_modified[-1][0] + h, f(nodes_modified[-1][0] + h)])
    for j in range(1, len(nodes_modified) - 1):
        f_j = (nodes_modified[j + 1][1] - nodes_modified[j - 1][1]) / (2 * h)
        first_derivatives.append([f_j, abs(f_j - f_deriv(nodes_modified[j][0]))])
    for k in range(1, len(first_derivatives) - 1):
        f_kk = (first_derivatives[k + 1][0] - first_derivatives[k - 1][0]) / (2 * h)
        second_derivatives.append([f_kk, abs(f_kk - f_second_deriv(nodes[k - 1][0]))])
    print_derivatives_table(nodes, first_derivatives[1:(len(first_derivatives) - 1)], second_derivatives)


def print_beginning_dot(nodes, h):
    print("\nТочка в начале таблицы")
    first_derivatives = []
    second_derivatives = []
    nodes_modified = nodes.copy()
    for i in range(4):
        nodes_modified.append([nodes_modified[-1][0] + h, f(nodes_modified[-1][0] + h)])
    for j in range(len(nodes_modified) - 2):
        f_j = (-3 * nodes_modified[j][1]
               + 4 * nodes_modified[j + 1][1]
               - nodes_modified[j + 2][1]) / (2 * h)
        first_derivatives.append([f_j, abs(f_j - f_deriv(nodes_modified[j][0]))])
    for k in range(len(first_derivatives) - 2):
        f_kk = (-3 * first_derivatives[k][0]
                + 4 * first_derivatives[k + 1][0]
                - first_derivatives[k + 2][0]) / (2 * h)
        second_derivatives.append([f_kk, abs(f_kk - f_second_deriv(nodes[k][0]))])
    print_derivatives_table(nodes, first_derivatives[:len(nodes)], second_derivatives)


def print_ending_dot(nodes, h):
    print("\nТочка в конце таблицы")
    first_derivatives = []
    second_derivatives = []
    nodes_modified = nodes.copy()
    for i in range(4):
        nodes_modified.insert(0, [nodes_modified[0][0] - h, f(nodes_modified[0][0] - h)])
    for j in range(2, len(nodes_modified)):
        f_j = (3 * nodes_modified[j][1]
               - 4 * nodes_modified[j - 1][1]
               + nodes_modified[j - 2][1]) / (2 * h)
        first_derivatives.append([f_j, abs(f_j - f_deriv(nodes_modified[j][0]))])
    for k in range(2, len(first_derivatives)):
        f_kk = (3 * first_derivatives[k][0]
                - 4 * first_derivatives[k - 1][0]
                + first_derivatives[k - 2][0]) / (2 * h)
        second_derivatives.append([f_kk, abs(f_kk - f_second_deriv(nodes[k - 2][0]))])
    print_derivatives_table(nodes, first_derivatives[2:], second_derivatives)


def task3_2():
    print('___Нахождение производных таблично-заданной функции по формулам численного дифференцирования___')
    while True:
        m = int(input('\nЧисло значений в таблице (m+1): ')) - 1
        print('m = ' + str(m))
        a = float(input('Начальная точка a: '))
        h = float(input('Шаг в таблице h>0: '))
        table = get_diff_table(m, a, h)
        print_right_difference(table, h)
        print_left_difference(table, h)
        print_central_difference(table, h)
        print_beginning_dot(table, h)
        print_ending_dot(table, h)
        resp = input('\nХотите продолжить? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет' or resp == 'No' or resp == 'no':
            sys.exit()
task3_2()