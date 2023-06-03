import math
from prettytable import PrettyTable

K_MAX = 100000000


def f(x):
    return 2 ** (-x) - math.sin(x)
    # return 2 ^ (-x) - math.sin(x)


def f_derivative(x):
    return -math.log(2) * 2 ** (-x) - math.cos(x)
    # return -log(2) / 2^x - cos(x)


def splitting_roots(A, B, N=100):
    value_h = (B - A) / N
    iter = 0
    counter = 0
    value_x1 = A
    value_x2 = value_x1 + value_h
    value_f1 = f(value_x1)
    sections = []
    table = PrettyTable()
    table.field_names = ['', 'Отрезки']
    print('\nОтделение корней:')
    while counter < K_MAX:
        if value_x2 <= B:
            value_f2 = f(value_x2)
            if value_f1 * value_f2 <= 0:
                sections.append([value_x1, value_x2])
                iter += 1
                table.add_row([iter, sections[-1]])
            value_x1 = value_x2
            value_x2 = value_x1 + value_h
            value_f1 = value_f2
        else:
            print(table)
            print('Число отрезков: ' + str(len(sections)))
            return sections
        counter += 1
    print(table)
    print('Число отрезков: ' + str(len(sections)))
    return sections


def bisection_method(sections, epsilon):
    roots = []
    iter = 0
    table = PrettyTable()
    table.field_names = ['', 'x', 'delta', '|f(x)-0|', 'кол-во шагов']
    print('\nМетод бисекции:')
    for section in sections:
        iter += 1
        counter = 0
        a = section[0]
        b = section[1]
        while ((b - a) / 2 > epsilon) and (counter < K_MAX):
            c = (a + b) / 2
            if f(a) * f(c) <= 0:
                b = c
            else:
                a = c
            counter += 1
        x = (a + b) / 2
        delta = (b - a) / 2
        table.add_row([iter, x, delta, abs(f(x) - 0), counter])
        roots.append(x)
    print(table)
    return roots


def Newton_method(sections, epsilon):
    roots = []
    iter = 0
    table = PrettyTable()
    table.field_names = ['', 'x', '|f(x)-0|', 'кол-во шагов']
    print('\nМетод Ньютона:')
    for section in sections:
        iter += 1
        x_0 = section[0] + abs(section[1] - section[0]) / 2
        x_1 = x_0 - f(x_0) / f_derivative(x_0)
        counter = 0
        while counter < K_MAX:
            if abs(x_1 - x_0) < epsilon:
                break
            x_k = x_1 - f(x_1) / f_derivative(x_1)
            x_0 = x_1
            x_1 = x_k
            counter += 1
        table.add_row([iter, x_1, abs(f(x_1) - 0), counter])
        roots.append(x_1)
    print(table)
    return roots


def modified_Newton_method(sections, epsilon):
    roots = []
    iter = 0
    table = PrettyTable()
    table.field_names = ['', 'x', '|f(x)-0|', 'кол-во шагов']
    print('\nМодифицированный метод Ньютона:')
    for section in sections:
        iter += 1
        x_0 = section[0] + abs(section[1] - section[0]) / 2
        x_prev = x_0
        x_next = x_prev - f(x_prev) / f_derivative(x_0)
        counter = 0
        while counter < K_MAX:
            if abs(x_next - x_prev) < epsilon:
                break
            x_k = x_next - f(x_next) / f_derivative(x_0)
            x_prev = x_next
            x_next = x_k
            counter += 1
        table.add_row([iter, x_next, abs(f(x_next) - 0), counter])
        roots.append(x_next)
    print(table)
    return roots


def secants_method(sections, epsilon):
    roots = []
    iter = 0
    table = PrettyTable()
    table.field_names = ['', 'x', '|f(x)-0|', 'кол-во шагов']
    print('\nМетод секущих:')
    for section in sections:
        iter += 1
        #x_0 = section[0] + abs(section[1] - section[0]) / 2
        #x_1 = x_0 - f(x_0) / f_derivative(x_0)
        x_0 = section[0]
        x_1 = section[1]
        counter = 0
        while counter < K_MAX:
            if abs(x_1 - x_0) < epsilon:
                break
            x_k = x_1 - (f(x_1) / (f(x_1) - f(x_0))) * (x_1 - x_0)
            x_0 = x_1
            x_1 = x_k
            counter += 1
        table.add_row([iter, x_1, abs(f(x_1) - 0), counter])
        roots.append(x_1)
    print(table)
    return roots


def task1():
    print('___Численные методы решения нелинейных уравнений___\nВариант 2')
    A = int(input('A: '))
    B = int(input('B: '))
    epsilon = float(input('epsilon: '))
    print('Начальные данные:   f(x) = 2^(-x)-sin(x),   '
          '[A,B]=[' + str(A) + ',' + str(B) + '],   epsilon=' + str(epsilon))
    array = splitting_roots(A, B)
    bisection_method(array, epsilon)
    Newton_method(array, epsilon)
    modified_Newton_method(array, epsilon)
    secants_method(array, epsilon)

task1()
