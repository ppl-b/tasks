import sys
import math
import os
from prettytable import PrettyTable

ITER_MAX = 100
F = "1-e^(-2x)"
POLY_0 = "5"
POLY_1 = "2x+3"
POLY_2 = "x^2-x+1"
POLY_3 = "2x^3-4x^2+x+7"
FUNCS = [POLY_0, POLY_1, POLY_2, POLY_3, F]


def f_poly_calculate(x, n):
    if n == 0:
        return 5
    elif n == 1:
        return 2 * x + 3
    elif n == 2:
        return math.pow(x, 2) - x + 1
    elif n == 3:
        return 2 * math.pow(x, 3) - 4 * math.pow(x, 2) + x + 7
    elif n == 4:
        return 1 - math.exp(-2 * x)
    return False


def f_poly_primitive(x, n):
    if n == 0:
        return 5 * x
    elif n == 1:
        return math.pow(x, 2) + 3 * x
    elif n == 2:
        return math.pow(x, 3) / 3 - math.pow(x, 2) / 2 + x
    elif n == 3:
        return math.pow(x, 4) / 2 - (4 / 3) * math.pow(x, 3) + math.pow(x, 2) / 2 + 7 * x
    elif n == 4:
        return x + math.exp(-2 * x) / 2
    return False


def f_poly_integral(a, b, n):
    return f_poly_primitive(b, n) - f_poly_primitive(a, n)


def f(x):
    return 1 - math.exp(-2 * x)


def f_derivative(x, n=1):
    if n == 0:
        return f(x)
    if n > 1:
        return 2 * math.pow(-2, n - 1) * math.exp(-2 * x)
    return 2 * math.exp(-2 * x)


def f_primitive(x):
    return x + math.exp(-2 * x) / 2


def f_integral(a, b):
    return f_primitive(b) - f_primitive(a)


def qf_left_square(a, b, acc_values):
    result = []
    for i in range(5):
        value = (b - a) * f_poly_calculate(a, i)
        error = abs(value - acc_values[i])
        result.append([value, error])
    return result


def qf_right_square(a, b, acc_values):
    result = []
    for i in range(5):
        value = (b - a) * f_poly_calculate(b, i)
        error = abs(value - acc_values[i])
        result.append([value, error])
    return result


def qf_mean_square(a, b, acc_values):
    result = []
    for i in range(5):
        value = (b - a) * f_poly_calculate((b + a) / 2, i)
        error = abs(value - acc_values[i])
        result.append([value, error])
    return result


def qf_trapez(a, b, acc_values):
    result = []
    for i in range(5):
        value = ((b - a) / 2) * (f_poly_calculate(a, i) + f_poly_calculate(b, i))
        error = abs(value - acc_values[i])
        result.append([value, error])
    return result


def qf_Simpson(a, b, acc_values):
    result = []
    for i in range(5):
        value = ((b - a) / 6) * (f_poly_calculate(a, i) +
                                 4 * f_poly_calculate((a + b) / 2, i) +
                                 f_poly_calculate(b, i))
        error = abs(value - acc_values[i])
        result.append([value, error])
    return result


def qf_three_eight(a, b, acc_values):
    result = []
    h = (b - a) / 3
    for i in range(5):
        value = (b - a) * (f_poly_calculate(a, i) / 8 +
                           f_poly_calculate(a + h, i) * 3 / 8 +
                           f_poly_calculate(a + 2 * h, i) * 3 / 8 +
                           f_poly_calculate(b, i) / 8)
        error = abs(value - acc_values[i])
        result.append([value, error])
    return result


def qf_print_table(table, results):
    for i in range(5):
        table.add_row([FUNCS[i], results[i][0], results[i][1]])
    print(table)


def qf_print_results_tables(a, b, acc_values):
    table = PrettyTable()
    table.field_names = ['Функция/полином', 'Значение интеграла', 'Фактическая погрешность']

    results = qf_left_square(a, b, acc_values)
    print("\nКвадратурная формула левого прямоугольника:")
    qf_print_table(table, results)
    table.clear_rows()

    results = qf_right_square(a, b, acc_values)
    print("\nКвадратурная формула правого прямоугольника:")
    qf_print_table(table, results)
    table.clear_rows()

    results = qf_mean_square(a, b, acc_values)
    print("\nКвадратурная формула среднего прямоугольника:")
    qf_print_table(table, results)
    table.clear_rows()

    results = qf_trapez(a, b, acc_values)
    print("\nКвадратурная формула трапеции:")
    qf_print_table(table, results)
    table.clear_rows()

    results = qf_Simpson(a, b, acc_values)
    print("\nКвадратурная формула Симпсона:")
    qf_print_table(table, results)
    table.clear_rows()

    results = qf_three_eight(a, b, acc_values)
    print("\nКвадратурная формула 3/8:")
    qf_print_table(table, results)
    table.clear_rows()


def task4_1():
    print("___Приближенное вычисление интеграла по квадратурным формулам___")
    print("\nФункция: f(x)=" + F + "\nВесовая функция: ro(x)=1")
    print("\nПолином нулевой степени: " + POLY_0)
    print("\nПолином первой степени: " + POLY_1)
    print("\nПолином второй степени: " + POLY_2)
    print("\nПолином третьей степени: " + POLY_3)
    for i in range(ITER_MAX):
        a = float(input("\nПравая граница отрезка [a, b]: a="))
        b = float(input("\nЛевая граница отрезка [a, b]: b="))
        acc_values = []
        for j in range(5):
            acc_values.append(f_poly_integral(a, b, j))
        print("\nТочное значение интеграла f(x) по [" + str(a) + ", " + str(b) + "]: J=" + str(acc_values[-1]))
        qf_print_results_tables(a, b, acc_values)
        resp = input('\nХотите продолжить? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет' or resp == 'No' or resp == 'no':
            sys.exit()


def get_max_deriv(a, b, m, h, n):
    result = 0
    for i in range(m + 1):
        value = abs(f_derivative(a + i * h, n))
        if result < value:
            result = value
    return result


def cqf_left_square(a, b, m, h, acc_values):
    result = []
    for i in range(5):
        value = 0
        for j in range(m):
            value += f_poly_calculate(a + j * h, i)
        value *= h
        fact_error = abs(value - acc_values[i])
        theo_error = "none"
        if i == 4:
            theo_error = get_max_deriv(a, b, m, h, 1) * (b - a) * math.pow(h, 1) / 2
        result.append([value, fact_error, theo_error])
    return result


def cqf_right_square(a, b, m, h, acc_values):
    result = []
    for i in range(5):
        value = 0
        for j in range(m):
            value += f_poly_calculate(a + (j + 1) * h, i)
        value *= h
        fact_error = abs(value - acc_values[i])
        theo_error = "none"
        if i == 4:
            theo_error = get_max_deriv(a, b, m, h, 1) * (b - a) * math.pow(h, 1) / 2
        result.append([value, fact_error, theo_error])
    return result


def cqf_mean_square(a, b, m, h, acc_values):
    result = []
    for i in range(5):
        value = 0
        for j in range(m):
            value += f_poly_calculate(a + (j + 0.5) * h, i)
        value *= h
        fact_error = abs(value - acc_values[i])
        theo_error = "none"
        if i == 4:
            theo_error = get_max_deriv(a, b, m, h, 2) * (b - a) * math.pow(h, 2) / 24
        result.append([value, fact_error, theo_error])
    return result


def cqf_trapez(a, b, m, h, acc_values):
    result = []
    for i in range(5):
        value = f_poly_calculate(a, i) + f_poly_calculate(b, i)
        for j in range(1, m):
            value += 2 * f_poly_calculate(a + j * h, i)
        value *= h / 2
        fact_error = abs(value - acc_values[i])
        theo_error = "none"
        if i == 4:
            theo_error = get_max_deriv(a, b, m, h, 2) * (b - a) * math.pow(h, 2) / 12
        result.append([value, fact_error, theo_error])
    return result


def cqf_Simpson(a, b, m, h, acc_values):
    result = []
    for i in range(5):
        value = f_poly_calculate(a, i) + f_poly_calculate(b, i)
        for j in range(1, m):
            value += 2 * f_poly_calculate(a + j * h, i)
        for j in range(m):
            value += 4 * f_poly_calculate(a + (j + 0.5) * h, i)
        value *= h / 6
        fact_error = abs(value - acc_values[i])
        theo_error = "none"
        if i == 4:
            theo_error = get_max_deriv(a, b, m, h, 4) * (b - a) * math.pow(h, 4) / 2880
        result.append([value, fact_error, theo_error])
    return result


def cqf_print_table(table, results):
    for i in range(5):
        table.add_row([FUNCS[i], results[i][0], results[i][1], results[i][2]])
    print(table)


def get_integral_values(values, results):
    temp = []
    for i in range(5):
        temp.append(results[i][0])
    values.append(temp)


def cqf_print_results_tables(a, b, m, h, acc_values):
    integral_values = []
    table = PrettyTable()
    table.field_names = ['Функция/полином', 'Значение интеграла',
                         'Фактическая погрешность', 'Теоретическая погрешность']

    results = cqf_left_square(a, b, m, h, acc_values)
    print("\nСоставная квадратурная формула левого прямоугольника:")
    cqf_print_table(table, results)
    table.clear_rows()
    get_integral_values(integral_values, results)
    integral_values[-1].append(0)  # АСТ

    results = cqf_right_square(a, b, m, h, acc_values)
    print("\nСоставная квадратурная формула правого прямоугольника:")
    cqf_print_table(table, results)
    table.clear_rows()
    get_integral_values(integral_values, results)
    integral_values[-1].append(0)

    results = cqf_mean_square(a, b, m, h, acc_values)
    print("\nСоставная квадратурная формула среднего прямоугольника:")
    cqf_print_table(table, results)
    table.clear_rows()
    get_integral_values(integral_values, results)
    integral_values[-1].append(1)

    results = cqf_trapez(a, b, m, h, acc_values)
    print("\nСоставная квадратурная формула трапеции:")
    cqf_print_table(table, results)
    table.clear_rows()
    get_integral_values(integral_values, results)
    integral_values[-1].append(1)

    results = cqf_Simpson(a, b, m, h, acc_values)
    print("\nСоставная квадратурная формула Симпсона:")
    cqf_print_table(table, results)
    table.clear_rows()
    get_integral_values(integral_values, results)
    integral_values[-1].append(3)

    return integral_values


def task4_2():
    print("___Приближенное вычисление интеграла по составным квадратурным формулам___")
    print("\nФункция: f(x)=" + F + "\nВесовая функция: ro(x)=1")
    print("\nПолином нулевой степени: " + POLY_0)
    print("\nПолином первой степени: " + POLY_1)
    print("\nПолином второй степени: " + POLY_2)
    print("\nПолином третьей степени: " + POLY_3)
    for i in range(ITER_MAX):
        a = float(input("\nПравая граница отрезка [A, B]: A="))
        b = float(input("\nЛевая граница отрезка [A, B]: B="))
        m = int(input("\nЧисло промежутков деления [A, B]: m="))
        h = (b - a) / m
        print("\nШаг: h=" + str(h))
        acc_values = []
        for j in range(5):
            acc_values.append(f_poly_integral(a, b, j))
        print("\nТочное значение интеграла f(x) по [" + str(a) + ", " + str(b) + "]: J=" + str(acc_values[-1]))
        cqf_print_results_tables(a, b, m, h, acc_values)
        resp = input('\nХотите продолжить? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет' or resp == 'No' or resp == 'no':
            sys.exit()


def runge_print_results_tables(integral_values_h, integral_values_hl, l, acc_values):
    print("\nУточнение по Рунге:")
    table = PrettyTable()
    table.field_names = ['Функция/полином', 'Уточненное значение интеграла', 'Фактическая погрешность']

    print("\nСоставная квадратурная формула левого прямоугольника:")
    for i in range(5):
        value = (math.pow(l, 1) * integral_values_hl[0][i] - integral_values_h[0][i]) / (math.pow(l, 1) - 1)
        error = abs(value - acc_values[i])
        table.add_row([FUNCS[i], value, error])
    print(table)
    table.clear_rows()

    print("\nСоставная квадратурная формула правого прямоугольника:")
    for i in range(5):
        value = (math.pow(l, 1) * integral_values_hl[1][i] - integral_values_h[1][i]) / (math.pow(l, 1) - 1)
        error = abs(value - acc_values[i])
        table.add_row([FUNCS[i], value, error])
    print(table)
    table.clear_rows()

    print("\nСоставная квадратурная формула среднего прямоугольника:")
    for i in range(5):
        value = (math.pow(l, 2) * integral_values_hl[2][i] - integral_values_h[2][i]) / (math.pow(l, 2) - 1)
        error = abs(value - acc_values[i])
        table.add_row([FUNCS[i], value, error])
    print(table)
    table.clear_rows()

    print("\nСоставная квадратурная формула трапеции:")
    for i in range(5):
        value = (math.pow(l, 2) * integral_values_hl[3][i] - integral_values_h[3][i]) / (math.pow(l, 2) - 1)
        error = abs(value - acc_values[i])
        table.add_row([FUNCS[i], value, error])
    print(table)
    table.clear_rows()

    print("\nСоставная квадратурная формула Симпсона:")
    for i in range(5):
        value = (math.pow(l, 4) * integral_values_hl[4][i] - integral_values_h[4][i]) / (math.pow(l, 4) - 1)
        error = abs(value - acc_values[i])
        table.add_row([FUNCS[i], value, error])
    print(table)


def task4_3():
    print("___Уточнение приближенных значений интегралов по принципу Рунге___")
    print("\nФункция: f(x)=" + F + "\nВесовая функция: ro(x)=1")
    print("\nПолином нулевой степени: " + POLY_0)
    print("\nПолином первой степени: " + POLY_1)
    print("\nПолином второй степени: " + POLY_2)
    print("\nПолином третьей степени: " + POLY_3)
    for i in range(ITER_MAX):
        a = float(input("\nПравая граница отрезка [A, B]: A="))
        b = float(input("\nЛевая граница отрезка [A, B]: B="))
        m = int(input("\nЧисло промежутков деления [A, B]: m="))
        h = (b - a) / m
        print("\nШаг: h=" + str(h))
        acc_values = []
        for j in range(5):
            acc_values.append(f_poly_integral(a, b, j))
        print("\nТочное значение интеграла f(x) по [" + str(a) + ", " + str(b) + "]: J=" + str(acc_values[-1]))
        integral_values_h = cqf_print_results_tables(a, b, m, h, acc_values)

        l = int(input("\nВо сколько раз умножить число промежутков: l="))
        hl = h / l
        print("\nНовый шаг: h/l=" + str(hl))
        integral_values_hl = cqf_print_results_tables(a, b, m * l, hl, acc_values)
        os.system('pause')
        runge_print_results_tables(integral_values_h, integral_values_hl, l, acc_values)

        resp = input('\nХотите продолжить? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет' or resp == 'No' or resp == 'no':
            sys.exit()

task4_3()
