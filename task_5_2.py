from math import cos, log, exp
import numpy as np
from scipy.integrate import quad
from functools import cache
from task_5_1 import get_polynomial_func, sep, space, get_monom_func, calc_qf
from prettytable import PrettyTable
import sys


ITER_MAX = 100
F_GAUSS = "1/((1+x^2)*(4+3x^2))^(1/2)"
F_MOELLER = "exp(2x)"


@cache
# Возвращает полиномы Лежандра от 0 до n степени включительно
def calc_gauss_polynoms(n: int) -> list:
    if n == 0:
        return [[1]]
    if n == 1:
        return [[1], [0, 1]]

    polynoms = calc_gauss_polynoms(n - 1)
    # Рекуррентная формула для нахождения полиномов Лежандра
    polynom = np.zeros(n + 1)
    polynom[0] = (1 - n) / n * polynoms[n - 2][0]
    for j in range(n - 2):
        polynom[j + 1] += (2 * n - 1) / n * polynoms[n -
                                                     1][j] + (1 - n) / n * polynoms[n - 2][j + 1]
    for j in range(n - 1, n + 1):
        polynom[j] = (2 * n - 1) / n * polynoms[n - 1][j - 1]
    polynoms.append(list(polynom))
    return polynoms


@cache
def calc_gauss_roots_coeffs(n):
    polynoms = calc_gauss_polynoms(n)
    # Находим корни полиномов Лежандра на [-1, 1]
    # TODO искать корни методом секущих
    roots = list(sorted(np.roots(polynoms[n][::-1])))

    # Находим квадрат предпоследнего полинома
    power_2_polynom_coeffs = [0] * (len(polynoms[n - 1]) * 2 - 1)
    for i in range(len(polynoms[n-1])):
        for j in range(len(polynoms[n-1])):
            power_2_polynom_coeffs[i + j] += polynoms[-2][i] * polynoms[-2][j]
    power_2_polynom = get_polynomial_func(power_2_polynom_coeffs)

    # Находим коэффициенты формулы Гаусса
    coeffs = []
    for i in range(n):
        x = roots[i]
        coeff = 2 * (1 - x ** 2) / (n ** 2 * power_2_polynom(x))
        coeffs.append(coeff)
    return roots, coeffs


# Линейно распространяет корни и коэффициенты на произвольный отрезок
def calc_true_roots_coeffs(a, b, roots, coeffs):
    # Находим коэффициенты формулы Гаусса
    true_roots = []
    true_coeffs = []
    for i in range(len(roots)):
        x = (b - a) / 2 * roots[i] + (b + a) / 2
        coeff = (b - a) / 2 * coeffs[i]
        true_roots.append(x)
        true_coeffs.append(coeff)
    return true_roots, true_coeffs


@cache
def calc_moeller_roots_coeffs(n):
    roots = []
    coeffs = []
    for k in range(1, n + 1):
        roots.append(cos((2 * k - 1) / (2 * n) * np.pi))
        coeffs.append(np.pi / n)
    return roots, coeffs


def gaussian_f_5(x):
    return 1/((1+x**2)*(4+3*x**2))**(1/2)


def moeller_f_5(x):
    return exp(2*x)


if __name__ == "__main__":
    test_func = gaussian_f_5
    moeller_func = moeller_f_5

    print("Квадратурная формула Гаусса")
    sep()
    table = PrettyTable()
    table.field_names = ["Узлы", "Коэффициенты"]
    for n in range(1, 7 + 1):
        print(f"N={n}")
        roots, coeffs = calc_gauss_roots_coeffs(n)

        for i in range(len(roots)):
            table.add_row([roots[i], coeffs[i]])
        print(table)
        table.clear_rows()

        # print("Корни:", " ".join(map(str, roots)))
        # print("Коэффициенты:", " ".join(map(str, coeffs)))
        # print(
        #     f"Проверка КФ Гаусса на мономе x^(2 * {n} - 1) = x^({2 * n - 1}):")
        for j in range(2 * n, 2 * n + 1):
            func = get_monom_func(j - 1)
            value = calc_qf(roots, coeffs, func)
            right_value = quad(lambda x: func(x), -1, 1)[0]
            print(f"Результат на мономе x^{j - 1}:", value,
                  "\nПравильный ответ:", right_value,
                  "\nПогрешность:", abs(right_value - value), sep="\t")
        sep()

    space()

    for iter in range(ITER_MAX):
        print("Формула Гаусса для произвольного отрезка")
        print("Тестовая функция:", F_GAUSS)
        sep()
        print("Введите границы отрезка интегрирования ([a, b])")
        a = float(input("a: "))
        b = float(input("b: "))
        # a, b = map(float, input().split())
        sep()
        for n in range(3, 7):
            print(f"N={n}")
            roots, coeffs = calc_gauss_roots_coeffs(n)
            true_roots, true_coeffs = calc_true_roots_coeffs(a, b, roots, coeffs)
            for i in range(len(true_roots)):
                table.add_row([true_roots[i], true_coeffs[i]])
            print(table)
            table.clear_rows()
            # print("Корни:", " ".join(map(str, true_roots)))
            # print("Коэффициенты:", " ".join(map(str, true_coeffs)))
            # print(
            #     f"Проверка КФ Гаусса на мономе x^(2 * {n} - 1) = x^({2 * n - 1}):")
            func = test_func
            value = calc_qf(true_roots, true_coeffs, func)
            right_value = quad(lambda x: func(x), a, b)[0]
            print(f"Результат для тестовой функции:", value,
                  "\nТочное значение:", right_value,
                  "\nПогрешность:", abs(right_value - value), sep="\t")
            sep()

            func = get_monom_func(2 * n - 1)
            value_test = calc_qf(true_roots, true_coeffs, func)
            right_value_test = quad(lambda x: func(x), a, b)[0]
            print(f"Проверка на мономе x^(2 * {n} - 1) = x^({2 * n - 1}):")
            print("Погрешность:", abs(value_test - right_value_test), sep="\t")
            sep()

        space()
        print("Формула Мелера")
        print("Тестовая функция:", F_MOELLER)
        sep()
        print("Введите N1, N2, N3, N4:")
        ns = map(int, input().split())
        sep()
        for n in ns:
            print(f"N={n}")
            roots, coeffs = calc_moeller_roots_coeffs(n)
            for i in range(len(roots)):
                table.add_row([roots[i], coeffs[i]])
            print(table)
            table.clear_rows()
            # print("Корни:", " ".join(map(str, roots)))
            # print("Коэффициенты:", " ".join(map(str, coeffs)))
            value = calc_qf(roots, coeffs, moeller_func)
            print("Значение интеграла по КФ Мёллера:", value, sep="\t")
            right_value = quad(lambda x: 1 / (1 - x ** 2) **
                               (1/2) * moeller_func(x), -1, 1)[0]
            print("Точное значение интеграла:", right_value, sep="\t")
            print("Погрешность:", abs(right_value - value), sep="\t")

            sep()
            func = get_monom_func(2 * n - 1)
            value_test = calc_qf(roots, coeffs, func)
            right_value_test = quad(lambda x: 1 / (1 - x ** 2) **
                                    (1/2) * func(x), -1, 1)[0]
            print(f"Проверка на мономе x^(2 * {n} - 1) = x^({2 * n - 1}):")
            print("Погрешность:", abs(value_test - right_value_test), sep="\t")
            sep()

        resp = input('\nХотите продолжить? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет' or resp == 'No' or resp == 'no':
            sys.exit()
