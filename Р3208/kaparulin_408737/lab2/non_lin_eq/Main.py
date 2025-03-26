from .PolDel import PolDel
from .Secant import Secant
from .SimpleIter import SimpleIter

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt

f = [
    [
        lambda x: 2*x**3 + 3.41*x**2 - 23.74*x + 2.95, 
        lambda x: 6*x**2 + 6.82*x - 23.74, 
        lambda x: 12*x + 6.82
    ],

    [
        lambda x: sin(x) + cos(x), 
        lambda x: cos(x) - sin(x), 
        lambda x: -sin(x) - cos(x)
    ],

    [
        lambda x: x**2 + 1, 
        lambda x: 2*x, 
        lambda x: 2
    ],

    [
        lambda x: x + cos(x-1) - 0.7, 
        lambda x: 1 - sin(x-1), 
        lambda x: - cos(x-1)
    ],
]

method = [
    PolDel,
    Secant,
    SimpleIter
]

class Main:
    def __init__(self):
        eq_nmb = 0

        while(eq_nmb not in [1, 2, 3, 4]):
            print("[1] f(x) = 2*x**3 + 3.41*x**2 - 23.74*x + 2.95")
            print("[2] f(x) = sin(x) + cos(x)")
            print("[3] f(x) = x**2 + 1")
            print("[4] f(x) = x + cos(x-1) - 0.7")
            print("Введите номер уравнения: ", end="")
            eq_nmb = self.__get_param("equation number", int, input)
            print()

        print("Введите путь до данных(\"\" - ввод в терминале): ", end="")
        file = self.__get_param("file name", str, input)


        method_nmb = 0

        while(method_nmb not in [1, 2, 3]):
            print()
            print("[1] Метод половинного деления")
            print("[2] Метод секущих")
            print("[3] Метод простой итерации")
            print("Введите номер метода решения уравнения: ", end="")
            method_nmb = self.__get_param("method name", int, input)
        
        print()
        print("Результаты в файл?(\"\" - нет, file_path - да): ", end="")
        res_file = self.__get_param("result file name", str, input)
        print()

        x, f_x, iter_cnt, interval = method[method_nmb-1](f[eq_nmb-1], file).get_answer()

        if res_file == "":
            print("x: ", x)
            print("f(x): ", f_x)
            print("Number of iteration: ", iter_cnt)
        else:
            resf = open(res_file, 'w')
            
            print("x: ", x, file=resf)
            print("f(x): ", f_x, file=resf)
            print("Number of iteration: ", iter_cnt, file=resf)

            resf.close()

        x_plot = np.linspace(interval[0], interval[1], 500)
        y_plot = f[eq_nmb-1][0](x_plot)

        plt.title('График нелинейной функции')
        plt.plot(x_plot, y_plot)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(1)
        plt.savefig("Non_lin_equ.png")


    # получение 1 параметра
    def __get_param(self, name, type, func):
        try:
            return type(func())
        except:
            print(f"Incorrect {name}")  
            exit()


if __name__ == "__main__":
    Main()