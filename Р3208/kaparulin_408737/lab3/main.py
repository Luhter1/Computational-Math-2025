import warnings
warnings.simplefilter("error")

from numpy import sin, cos
import numpy as np 

from methods import TrapezoidRule, RectangleRule, SimpsonRule


funcs = [
    lambda x: 3*x**3 + 5*x**2 + 3*x - 6, 
    lambda x: sin(x) + cos(x), 
    lambda x: x**2 + 1, 
    lambda x: np.log(x), 
]

methods = [
    RectangleRule.left_rectangle_rule,
    RectangleRule.midpoint_rectangle_rule,
    RectangleRule.right_rectangle_rule,
    TrapezoidRule.trapezoid_rule,
    SimpsonRule.simpson_rule,
]

class Main:
    def __init__(self):
        eq_nmb = 0
        method_nmb = 0

        while(eq_nmb not in [1, 2, 3, 4]):
            print("[1] f(x) = 3*x**3 + 5*x**2 + 3*x - 6")
            print("[2] f(x) = sin(x) + cos(x)")
            print("[3] f(x) = x**2 + 1")
            print("[4] f(x) = ln(x)")
            print("Введите номер уравнения: ", end="")
            eq_nmb = self.__get_param("equation number", int, input)
            print()

        while(method_nmb not in [1, 2, 3, 4, 5]):
            print("[1] Метод левых прямоугольников")
            print("[2] Метод серединных прямоугольников")
            print("[3] Метод правых прямоугольников")
            print("[4] Метод трапеций ")
            print("[5] Метод Симпсона ")
            print("Введите номер метода решения уравнения: ", end="")
            method_nmb = self.__get_param("method name", int, input)
            print()
        
        print("Input a: ", end="")
        a = self.__get_param("a", float, input)
        print("Input b: ", end="")
        b = self.__get_param("b", float, input)
        print("Input e: ", end="")
        e = self.__get_param("e", float, input)
        print()

        if (eq_nmb == 4 and a<=0) and not (eq_nmb == 4 and a==0 and (method_nmb==2 or method_nmb==3)): 
            print("Error: Integrated function has discontinuity in current interval")
            exit()
        elif a>b:
            print("Error: incorrect interval")
            exit()
        elif a==b:
            Integ, n = 0, 0
        else:
            Integ, n = methods[method_nmb-1](funcs[eq_nmb-1], a, b, e=e)


        print("Integral value: ", Integ)

        print("Number of splits: ", n)



    # получение 1 параметра
    def __get_param(self, name, type, func):
        try:
            return type(func())
        except:
            print(f"Incorrect {name}")  
            exit()


if __name__ == "__main__":
    Main()