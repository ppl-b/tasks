from math import sin
from scipy.integrate import quad
from task_5_2 import calc_gauss_roots_coeffs, calc_true_roots_coeffs
from task_5_1 import sep, calc_qf
import sys
from prettytable import PrettyTable


ITER_MAX = 100
F_X = "sin(x)"
RHO_X = "x^(1/4)"

# 2 вариант
def rho_4(x):
    return x ** (1/4)


def calc_true_complex_roots_coeffs(a, b, points, coeffs, m):
    if len(points) != len(coeffs):
        raise ValueError("Количество узлов и коэффициентов должно совпадать")

    eps = (b - a) / m
    true_points = []
    true_coeffs = []
    b_i = a
    for _ in range(m):
        a_i = b_i
        b_i = a_i + eps
        tmp_roots, tmp_coeffs = calc_true_roots_coeffs(
            a_i, b_i, points, coeffs)
        true_points.extend(tmp_roots)
        true_coeffs.extend(tmp_coeffs)
    return true_points, true_coeffs


if __name__ == "__main__":
    print("___Приближённое вычисление интеграла при помощи составной КФ Гаусса___")
    print("\nf(x)=" + F_X)
    print("Весовая функция:", RHO_X)

    test_f = sin
    test_rho = rho_4

    for iter in range(ITER_MAX):
        print("\nВведите a, b - границы отрезка интегрирования")
        a = float(input("a: "))
        b = float(input("b: "))
        # a, b = map(float, input().split())

        print("Введите N - количество узлов, m - число отрезков разбиения")
        n = int(input("N: "))
        m = int(input("m: "))
        # line = input()
        # n, m = map(int, line.split())
        roots, coeffs = calc_gauss_roots_coeffs(n)
        true_roots, true_coeffs = calc_true_complex_roots_coeffs(
            a, b, roots, coeffs, m)

        '''table = PrettyTable()
        table.field_names = ["Узлы", "Коэффициенты"]
        for i in range(len(true_roots)):
            table.add_row([true_roots[i], true_coeffs[i]])
        print(table)'''

        value = calc_qf(true_roots, true_coeffs,
                        lambda x: test_f(x) * test_rho(x))
        right_value = quad(lambda x: test_f(x) * test_rho(x), a, b)[0]
        print(f"Значение интеграла для {n} узлов и {m} разбиений", value,
              "\nПравильный ответ:", right_value,
              "\nПогрешность:", abs(right_value - value), sep="\t")
        sep()

        resp = input('\nХотите продолжить? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет' or resp == 'No' or resp == 'no':
            sys.exit()

