import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
from math import sin, cos, exp, log

# Построение таблицы конечных разностей
def finite_diff(y):
    n = len(y)
    table = np.zeros((n, n))
    table[:,0] = y
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i+1][j-1] - table[i][j-1]
    return table

# 1. Интерполяция многочленом Лагранжа
def lagrange_interpolation(x, y, x_val):
    result = 0.0
    n = len(x)
    for i in range(n):
        term = y[i]
        for j in range(n):
            if j != i:
                term *= (x_val - x[j]) / (x[i] - x[j])
        result += term
    return result

# 2. Интерполяция Ньютона с разделенными разностями
def newton_divided_diff(x, y, x_val):
    n = len(x)
    coef = np.zeros([n, n])
    coef[:,0] = y
    
    for j in range(1, n):
        for i in range(n - j):
            coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x[i+j] - x[i])
    
    result = coef[0][0]
    for j in range(1, n):
        term = coef[0][j]
        for k in range(j):
            term *= (x_val - x[k])
        result += term
    return result

# 3. Интерполяция Ньютона с конечными разностями (1 и 2 формулы)
def newton_forward(x, y, x_val):
    h = x[1] - x[0]
    t = (x_val - x[0]) / h
    diff = finite_diff(y)
    result = y[0]
    for i in range(1, len(x)):
        term = 1.0
        for j in range(i):
            term *= (t - j)
        result += (term / factorial(i)) * diff[0, i]
    return result

def newton_backward(x, y, x_val):
    h = x[1] - x[0]
    t = (x_val - x[-1]) / h
    diff = finite_diff(y)
    result = y[-1]
    for i in range(1, len(x)):
        term = 1.0
        for j in range(i):
            term *= (t + j)
        result += (term / factorial(i)) * diff[-i-1, i]
    return result

# Функции для выбора в режиме (c)
def func_sin(x):
    return sin(x)

def func_cos(x):
    return cos(x)

def func_exp(x):
    return exp(x)

def func_log(x):
    return log(x) if x > 0 else float('nan')

def input_data():
    print("Выберите способ ввода данных:")
    print("a) Ввод с клавиатуры")
    print("b) Загрузка из файла")
    print("c) Генерация на основе функции")
    choice = input("Ваш выбор (a/b/c): ").strip().lower()
    
    if choice == 'a':
        # Режим (a): ввод с клавиатуры
        n = int(input("Введите количество точек: "))
        x = []
        y = []
        for i in range(n):
            xi = float(input(f"x[{i}]: "))
            yi = float(input(f"y[{i}]: "))
            x.append(xi)
            y.append(yi)
        return x, y
    
    elif choice == 'b':
        # Режим (b): загрузка из файла
        filename = input("Введите имя файла: ")
        with open(filename, 'r') as f:
            lines = f.readlines()
        x = []
        y = []
        for line in lines:
            xi, yi = map(float, line.strip().split())
            x.append(xi)
            y.append(yi)
        return x, y
    
    elif choice == 'c':
        # Режим (c): генерация на основе функции
        print("Доступные функции:")
        print("1. sin(x)")
        print("2. cos(x)")
        print("3. exp(x)")
        print("4. log(x)")
        func_choice = int(input("Выберите функцию (1-4): "))
        a = float(input("Начало интервала: "))
        b = float(input("Конец интервала: "))
        n = int(input("Количество точек: "))
        
        x = np.linspace(a, b, n)
        if func_choice == 1:
            y = [func_sin(xi) for xi in x]
        elif func_choice == 2:
            y = [func_cos(xi) for xi in x]
        elif func_choice == 3:
            y = [func_exp(xi) for xi in x]
        elif func_choice == 4:
            y = [func_log(xi) if xi > 0 else float('nan') for xi in x]
        else:
            raise ValueError("Неверный выбор функции")
        
        # Удаляем точки, где log(x) не определен
        if func_choice == 4:
            x = [xi for xi, yi in zip(x, y) if not np.isnan(yi)]
            y = [yi for yi in y if not np.isnan(yi)]
        
        return x, y
    
    else:
        raise ValueError("Неверный выбор способа ввода")

if __name__ == "__main__":
    try:
        x, y = input_data()
        print("\nВведенные данные:")
        for xi, yi in zip(x, y):
            print(f"x = {xi:.4f}, y = {yi:.4f}")

        # Запрос точки интерполяции
        x_val = float(input("\nВведите значение x для интерполяции: "))
        
        # Вычисление интерполяции
        print("\nРезультаты интерполяции:")
        print(f"Лагранж: y({x_val}) ≈ {lagrange_interpolation(x, y, x_val):.6f}")
        print(f"Ньютон (раздел. разности): y({x_val}) ≈ {newton_divided_diff(x, y, x_val):.6f}")
        
        if len(set(np.diff(x))) == 1:  # Проверка равномерности сетки
            print(f"Ньютон (вперед): y({x_val}) ≈ {newton_forward(x, y, x_val):.6f}")
            print(f"Ньютон (назад): y({x_val}) ≈ {newton_backward(x, y, x_val):.6f}")
            print()
            print("Таблица конечных разностей:\n")

            diff_table = finite_diff(y)

            for line in diff_table:
                for item in line:
                    print("%.3f\t" % (item), end="")
                print()
            print()
        else:
            print("Методы Ньютона с конечными разностями требуют равномерной сетки!")



        # Построение графиков
        x_new = np.linspace(min(x), max(x), 100)
        y_lagrange = [lagrange_interpolation(x, y, xi) for xi in x_new]
        y_newton_div = [newton_divided_diff(x, y, xi) for xi in x_new]
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, 'o', label='Узлы интерполяции')
        plt.plot(x_new, y_lagrange, label='Лагранж')
        plt.plot(x_new, y_newton_div, '--', label='Ньютон (раздел. разности)')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid()
        plt.title('Интерполяция функции')
        plt.savefig("graph.png")

    except Exception as e:
        print(f"Ошибка: {e}")