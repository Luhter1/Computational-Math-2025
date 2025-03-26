import numpy as np
import matplotlib.pyplot as plt
from sympy import Matrix

sys = [
    
    [
        [lambda x, y: x + y, lambda x, y: -3*x + 5*y],
        [
            [lambda x, y: 1, lambda x, y: 1], 
            [lambda x, y: -3, lambda x, y: 5]
        ]
    ],

    [
        [lambda x, y: x**2 + y**2 - 4, lambda x, y: -3*x**2 + y],
        [
            [lambda x, y: 2*x, lambda x, y: 2*y], 
            [lambda x, y: -6*x, lambda x, y: 1]
        ]
    ],

]

class Newton:
    def __init__(self, system):

        self.__plot(system[0])
        self.__input_params()
        self.__solution(system)

    def __solution(self, system):
        f = system[0][0]
        g = system[0][1]
        dfdx = system[1][0][0]
        dfdy = system[1][0][1]
        dgdx = system[1][1][0]
        dgdy = system[1][1][1]

        def matrix(x, y):
            return Matrix([
                [dfdx(x, y), dfdy(x, y)], 
                [dgdx(x, y), dgdy(x, y)]
            ]), Matrix([g(x,y), f(x,y)])

        
        

        diff = float('inf')
        cnt = 0
        x = self.x0
        y = self.y0 

        while(diff > self.e):
            cnt += 1
            M, ans = matrix(x, y)

            res = M.solve_least_squares(ans)
            dx = res[0]
            dy = res[1]

            x = x + dx
            y = y + dy

            diff = min(abs(dx), abs(dy))
            
        print("x1, x2: ", x, y)
        print("Number of Iteration: ", cnt)
        print("|x_k - x_k+1|: ", diff)
        
        
    def __plot(self, eqs):
        # Определяем диапазон значений для x и y
        x = np.linspace(-10, 10, 400)
        y = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x, y)

        # Определяем функцию
        Z1 = eqs[0](X,Y)
        Z2 = eqs[1](X,Y)

        # Строим график
        plt.contour(X, Y, Z1, levels=[0], colors='blue')
        plt.contour(X, Y, Z2, levels=[0], colors='red')
        plt.title('График системы нелинейных уравнений')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.savefig("System_graph.png")


    #  ввод всех параметров
    def __input_params(self):
        
        print("Input x0: ", end="")
        self.x0 = self.__get_param("x0", float, input)

        print("Input y0: ", end="")
        self.y0 = self.__get_param("y0", float, input)

        print("Input e: ", end="")
        self.e = self.__get_param("e", float, input)
        
        print()   



    # получение 1 параметра
    def __get_param(self, name, type, func):
        try:
            return type(func())
        except:
            print(f"Incorrect {name}")  
            exit()

if __name__ == "__main__":
    Newton(sys[0])