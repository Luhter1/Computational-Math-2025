import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

X = []
Y = []

# Функции для аппроксимации
def linear(x, a, b):
    return a * x + b

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def cubic(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def exponential(x, a, b):
    return a * np.exp(b * x)

def logarithmic(x, a, b):
    return a * np.log(x + 1e-9) + b  # +1e-9 для избежания log(0)

def power(x, a, b):
    return a * (x + 1e-9)**b  # +1e-9 для избежания 0^b

# Метод наименьших квадратов для всех моделей
models = {
    "Линейная": (linear, 2),
    "Квадратичная": (quadratic, 3),
    "Кубическая": (cubic, 4),
    "Экспоненциальная": (exponential, 2),
    "Логарифмическая": (logarithmic, 2),
    "Степенная": (power, 2),
}

class Main:
    def __init__(self):
        point_nmb = 0

        while(point_nmb not in [8, 9, 10, 11, 12]):
            print("Введите количество вводимых точек(8-12): ", end="")
            point_nmb = self.__get_param("equation number", int, input)
            print()

        print("Введите путь до данных(\"\" - ввод в терминале): ", end="")
        file = self.__get_param("file name", str, input)

        if file:
            with open(file) as f:
                for i in f.readlines():
                    xi, yi = map(float, i.split(" "))
                    X.append(xi)
                    Y.append(yi)
        else:
            for i in range(point_nmb):
                xi, yi = map(float, input().split(" "))
                X.append(xi)
                Y.append(yi)


        if len(X) != point_nmb:
            print("Error: invalid point's number")
            exit()

        x = np.array(X)
        y = np.array(Y)

        # решение
        results = {}
        for name, (func, params) in models.items():
            try:
                popt, pcov = curve_fit(func, x, y, maxfev=10000)
                y_pred = func(x, *popt)
                S = np.sum((y_pred - y)**2)
                n = len(x)
                mse = np.sqrt(S / n)
                results[name] = {
                    "coeffs": popt,
                    "S": S,
                    "mse": mse,
                    "y_pred": y_pred,
                }
            except Exception as e:
                print(f"Ошибка в модели {name}: {str(e)}")

        # Коэффициент корреляции Пирсона (для линейной)
        if "Линейная" in results:
            r = np.corrcoef(x, y)[0, 1]
            results["Линейная"]["r"] = r
            R2 = r**2
            results["Линейная"]["R2"] = R2

        # Вывод результатов
        print("Результаты аппроксимации:")
        for name, data in results.items():
            print(f"\n--- {name} ---")
            print(f"Коэффициенты: {np.round(data['coeffs'], 4)}")
            print(f"S = {data['S']:.4f}")
            print(f"СКО = {data['mse']:.4f}")
            if name == "Линейная":
                print(f"Коэф. корреляции Пирсона: {data['r']:.4f}")
                print(f"Коэф. детерминации R²: {data['R2']:.4f}")

        # Выбор наилучшей модели
        best_model = min(results.items(), key=lambda x: x[1]["mse"])
        print(f"\nНаилучшая модель: {best_model[0]} (СКО = {best_model[1]['mse']:.4f})")

        # Построение графиков
        plt.figure(figsize=(12, 8))
        plt.scatter(x, y, label="Исходные данные", color="black")

        x_plot = np.linspace(x.min() - 0.5, x.max() + 0.5, 100)
        for name, data in results.items():
            if name == "Линейная":
                y_plot = linear(x_plot, *data["coeffs"])
            elif name == "Квадратичная":
                y_plot = quadratic(x_plot, *data["coeffs"])
            elif name == "Кубическая":
                y_plot = cubic(x_plot, *data["coeffs"])
            elif name == "Экспоненциальная":
                y_plot = exponential(x_plot, *data["coeffs"])
            elif name == "Логарифмическая":
                y_plot = logarithmic(x_plot, *data["coeffs"])
            elif name == "Степенная":
                y_plot = power(x_plot, *data["coeffs"])
            plt.plot(x_plot, y_plot, label=name)

        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Аппроксимация функции")
        plt.legend()
        plt.grid(True)
        plt.savefig("graph.png")



    # получение 1 параметра
    def __get_param(self, name, type, func):
        try:
            return type(func())
        except:
            print(f"Incorrect {name}")  
            exit()


if __name__ == "__main__":
    Main()