import numpy as np
import matplotlib.pyplot as plt

# Определение ОДУ и их точных решений
def f1(x, y):
    return x + y

def y_exact1(x, x0, y0):
    C = (y0 - x0 - 1) * np.exp(-x0)
    return C * np.exp(x) + x + 1

def f2(x, y):
    return y * np.cos(x)

def y_exact2(x, x0, y0):
    return y0 * np.exp(np.sin(x) - np.sin(x0))

def f3(x, y):
    return x**2 - y

def y_exact3(x, x0, y0):
    return (y0 - x0**2 + 2*x0 - 2) * np.exp(-(x - x0)) + x**2 - 2*x + 2

# Методы решения
def euler(f, x0, y0, h, xn):
    x = np.arange(x0, xn + h, h)
    y = np.zeros(len(x))
    y[0] = y0
    for i in range(1, len(x)):
        y[i] = y[i-1] + h * f(x[i-1], y[i-1])
    return x, y

def improved_euler(f, x0, y0, h, xn):
    x = np.arange(x0, xn + h, h)
    y = np.zeros(len(x))
    y[0] = y0
    for i in range(1, len(x)):
        k1 = h * f(x[i-1], y[i-1])
        k2 = h * f(x[i-1] + h, y[i-1] + k1)
        y[i] = y[i-1] + (k1 + k2) / 2
    return x, y

def milne(f, x0, y0, h, xn, start_method):
    x = np.arange(x0, xn + h, h)
    n = len(x)
    y = np.zeros(n)
    # Используем стартовый метод для первых 4 точек
    x_start, y_start = start_method(f, x0, y0, h, x0 + 3*h)
    y[:4] = y_start[:4]
    for i in range(3, n-1):
        # Предиктор
        y_pred = y[i-3] + 4*h/3 * (2*f(x[i], y[i]) - f(x[i-1], y[i-1]) + 2*f(x[i-2], y[i-2]))
        # Корректор
        y[i+1] = y[i-1] + h/3 * (f(x[i+1], y_pred) + 4*f(x[i], y[i]) + f(x[i-1], y[i-1]))
    return x, y

if __name__ == "__main__":
    # Выбор ОДУ
    print("Выберите ОДУ:")
    print("1. y' = x + y")
    print("2. y' = y * cos(x)")
    print("3. y' = x^2 - y")
    choice = int(input("Введите номер ОДУ (1-3): "))

    if choice == 1:
        f = f1
        y_exact = lambda x: y_exact1(x, x0, y0)
    elif choice == 2:
        f = f2
        y_exact = lambda x: y_exact2(x, x0, y0)
    elif choice == 3:
        f = f3
        y_exact = lambda x: y_exact3(x, x0, y0)
    else:
        print("Некорректный выбор")
        exit()

    x0 = float(input("Введите x0: "))
    y0 = float(input("Введите y0: "))
    xn = float(input("Введите xn: "))
    h = float(input("Введите шаг h: "))
    epsilon = float(input("Введите точность ε: "))

    if xn <= x0:
        print("Некорректный интервал")
        exit()

    # Решение методами
    x_euler, y_euler = euler(f, x0, y0, h, xn)
    x_ie, y_ie = improved_euler(f, x0, y0, h, xn)
    x_milne, y_milne = milne(f, x0, y0, h, xn, improved_euler)

    # Точное решение
    x_exact = np.linspace(x0, xn, 100)
    y_exact_vals = y_exact(x_exact)

    # Оценка точности
    # Правило Рунге для метода Эйлера
    h2 = h / 2
    x_euler_h2, y_euler_h2 = euler(f, x0, y0, h2, xn)
    error_euler = np.abs(y_euler - y_euler_h2[::2][:len(y_euler)])

    # Ошибка для Милна через точное решение
    y_milne_exact = y_exact(x_milne)
    error_milne = np.abs(y_milne - y_milne_exact)

    # Вывод таблицы
    print("\nТаблица результатов:")
    print("x\tЭйлер\tУ.Эйлер\tМилна\tErr_Э\tErr_М")
    for i in range(len(x_euler)):
        print(f"{x_euler[i]:.2f}\t{y_euler[i]:.3f}\t{y_ie[i]:.3f}\t{y_milne[i]:.3f}\t{error_euler[i]:.4f}\t{error_milne[i]:.4f}")

    # Графики
    plt.figure(figsize=(10, 6))
    plt.plot(x_exact, y_exact_vals, label='Точное решение', color='black')
    plt.plot(x_euler, y_euler, 'o--', label='Метод Эйлера')
    plt.plot(x_ie, y_ie, 's--', label='У. Эйлер')
    plt.plot(x_milne, y_milne, 'd--', label='Милна')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.title('Сравнение методов решения ОДУ')
    plt.savefig("graph.png")