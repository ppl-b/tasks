from scipy.integrate import quad
from scipy import linalg
import numpy as np
from math import sin, exp, cos
from prettytable import PrettyTable
import sys

ITER_MAX = 100
WEIGHT_MOMENT_ACCURACY = int(1e3)
RHO_X = "x^(1/2)"
F_X = "sin(x)"

def rho(x):
    # return 1
    return x**(1/2)


def f(x):
    return sin(x)


def get_monom_func(n: int):
    def wrapper(x):
        return x ** n
    return wrapper


def get_polynomial_func(coeffs: list):
    def wrapper(x):
        res = 0
        for i in range(len(coeffs)):
            res += coeffs[i] * x ** i
        return res
    return wrapper


def calc_qf_mean_square(a: float, b: float, n: int, func: callable):
    eps = (b-a) / n
    result = 0
    for i in range(n):
        value = eps * func((a + (i + 1/2) * eps))
        result += value
    return result


def calc_weight_moments(a, b, n, rho):
    weight_moments = []
    for i in range(n):
        # TODO изменить на qf_mean_square
        weight_moments.append(quad(lambda x: rho(x) * x ** i, a, b)[0])
    return weight_moments


def calc_iqf_coeffs(a, b, points, rho):  # Интерполяционная квадратурная формула
    n = len(points)
    weight_moments = calc_weight_moments(a, b, n, rho)

    # Находим коэффициенты
    a_matrix = np.zeros((n, n))
    b_vector = np.array(weight_moments)

    # Составляем матрицу коэффициентов
    for i in range(n):
        for j in range(n):
            a_matrix[i][j] = points[j] ** i

    # Решаем систему
    coeffs = linalg.solve(a_matrix, b_vector)
    table = PrettyTable()
    table.field_names = ["k", "Момент веса Mu", "Коэффициент A_k", "Узел x_k"]
    for i in range(n):
        table.add_row([i + 1, weight_moments[i], coeffs[i], points[i]])
    print(table)
    '''for i in range(n):
        print(f"Момент веса Mu_{i}:", weight_moments[i],
              f"Коэффициент A_{i + 1}:", coeffs[i],
              f"Узел X_{i + 1}:", points[i], sep="\t")'''
    return coeffs


def get_hada_polynom(a, b, n, rho):  # Получение ортогонального многочлена степени N=n
    # Получаем весовые моменты
    weight_moments = calc_weight_moments(a, b, 2 * n, rho)
    print("Моменты веса:", " ".join(map(str, weight_moments)), sep="\t")

    # Получаем матрицу коэффициентов
    a_matrix = np.zeros((n, n))
    b_vector = -np.array(weight_moments[n:])
    for i in range(n):
        for j in range(n):
            a_matrix[i][j] = weight_moments[i + j]

    # Решаем систему
    coeffs = linalg.solve(a_matrix, b_vector)
    return list(coeffs) + [1]  # Чтобы многочлен был унитарным


# Подсчёт интеграла с помощью КФ НАСТ
def calc_qf_hada_roots_coeffs(a, b, n, rho):
    coeffs = get_hada_polynom(a, b, n, rho)
    print("Коэффициенты полинома:", " ".join(map(str, coeffs)), sep="\t")
    roots = np.roots(coeffs[::-1])  # Ищем корни многочлена
    roots.sort()

    # # Тест на мономах
    # for i in range(n):
    #     print(quad(lambda x: rho(x) * get_monom_func(i)(x)
    #           * get_polynomial_func(coeffs)(x), a, b))
    # print(roots)

    a_matrix = np.zeros((n, n))
    b_vector = np.array(calc_weight_moments(a, b, n, rho))
    for i in range(n):
        for j in range(n):
            a_matrix[i][j] = roots[j] ** i
    # Решаем систему
    coeffs = linalg.solve(a_matrix, b_vector)
    return roots, coeffs


def calc_qf(points, coeffs, func):
    if len(points) != len(coeffs):
        raise ValueError("Количество узлов и коэффициентов должно совпадать.")
    value = 0
    for i in range(len(points)):
        value += coeffs[i] * func(points[i])
    return value


def sep():
    print("-" * 120)


def space():
    print("\n" * 2)


if __name__ == "__main__":
    print("___Приближённое вычисление интегралов при помощи КФ НАСТ___")

    print("f(x)=" + F_X + "\nВесовая фукнция: " + RHO_X)

    for iter in range(ITER_MAX):
        print("\n\nВведите пределы интегрирования ([a, b])")
        a = int(input("a: "))
        b = int(input("b: "))

        test_func = f
        test_rho = rho

        n = int(input("Введите число узлов N: "))
        step = (b - a) / (n + 1)
        points = []
        for k in range(n):
            points.append(a + (k + 1) * step)

        '''print(f"Введите {n} узлов:")
        tmp_str = input()
        if tmp_str:
            points = list(map(float, tmp_str.split()))
        else:
            points = list(np.linspace(a, b, n))'''

        sep()
        # Результат scipy
        scipy_value = quad(lambda x: test_func(x) * test_rho(x), a, b)[0]
        print("Точное значение интеграла: ", scipy_value)

        sep()
        space()
        # ИКФ
        print("ИКФ")
        coeffs = calc_iqf_coeffs(a, b, points, test_rho)
        res = calc_qf(points, coeffs, test_func)
        print("Результат ИКФ:", res, "\nПогрешность: ",
              abs(scipy_value - res), sep="\t")

        sep()
        # Проверка ИКФ на одночлене x^(n - 1)
        for j in range(n, n + 1):
            func = get_monom_func(j - 1)
            res = calc_qf(points, coeffs, func)
            right_answer = quad(lambda x: func(x) * test_rho(x), a, b)[0]
            print(f"Проверка ИКФ на мономе x^{j - 1}:", res,
                  "\nПравильный ответ:", right_answer,
                  "\nПогрешность:", abs(right_answer - res), sep="\t")

        sep()
        space()
        # КФ НАСТ
        print("КФ НАСТ")
        sep()
        roots, coeffs = calc_qf_hada_roots_coeffs(a, b, n, test_rho)
        print("Узлы:", " ".join(map(str, roots)), sep="\t")
        print("Коэффициенты A_k:", " ".join(map(str, coeffs)), sep="\t")
        sep()
        value = calc_qf(roots, coeffs, test_func)
        print("Значение интеграла по КФ НАСТ:", value,
              "\nПогрешность:", abs(scipy_value - value), sep="\t")

        sep()
        # Проверка КФ НАСТ на одночлене x^(2n - 1)
        print(f"Проверка КФ НАСТ на одночлене x^(2 * {n} - 1) = x^({2 * n - 1}):")
        for j in range(2 * n, 2 * n + 1):
            func = get_monom_func(j - 1)
            value = calc_qf(roots, coeffs, func)
            right_answer = quad(lambda x: func(x) * test_rho(x), a, b)[0]
            print(f"Результат для x^{j - 1}:", value,
                  "\nПравильный ответ:", right_answer,
                  "\nПогрешность:", abs(right_answer - value), sep="\t")
        sep()

        resp = input('\nХотите продолжить? (Да/Нет): ')
        if resp == 'Нет' or resp == 'нет' or resp == 'No' or resp == 'no':
            sys.exit()
