import numpy as np

class SimpleIter:
    interval = np.array([0,0], dtype=float)
    x0 = 0
    e = 0.01

    def __init__(self, funcs, file_name=''):

        if not file_name:
            self.__input_params()
        else:
            self.__read_params(file_name)

        self.__is_correct(self.interval, self.e)

        self.__root_check(funcs[0], funcs[1], self.interval)

        self.__find_x0_and_lambda(funcs[1], self.interval)

        self.__is_algorithm_convergence(funcs[1])
        
        self.__solution(funcs[0])


    def get_answer(self):
        return (self.solution, self.f_x, self.cnt, self.interval)


    def __solution(self, f):
        diff = float('inf')
        x = self.x0
        self.cnt = 0

        while(diff > self.e):
            x_n = self.__phi(f, x)
            self.cnt+=1
            diff = abs(x - x_n)
            x = x_n

        self.solution = x
        self.f_x = f(self.solution)


    def __phi(self, f, x):
        return x + self.Lambda * f(x)
    
    def __is_algorithm_convergence(self, fp):
        if 1 + self.Lambda * fp(self.x0) >= 1:
            print(f"Ошибка: условие сходимости не выполнено на данном интервале")
            exit()


    def __find_x0_and_lambda(self, fp, interval):
        if abs(fp(interval[0])) > abs(fp(interval[1])):
            self.Lambda = -1/abs(fp(interval[0])) if fp(interval[0]) > 0 else 1/abs(fp(interval[0]))
            self.x0 = interval[0]
        else:
            self.Lambda = -1/abs(fp(interval[1])) if fp(interval[1]) > 0 else 1/abs(fp(interval[1]))
            self.x0 = interval[1]


    def __root_check(self, f, fp, interval):
        if(f(interval[0]) * f(interval[1]) > 0):
            print(f"Ошибка: на данном интервале нет корней, либо их несколько")
            exit()
            
        else:
            linspace = np.linspace(interval[0], interval[1], num=500)
            fp_linspace = fp(linspace)
            
            if not (np.all(fp_linspace[:-1] <= fp_linspace[1:]) or np.all(fp_linspace[:-1] >= fp_linspace[1:])):
                print(f"Предупреждение: на данном интервале может быть несколько корней")


    def __is_correct(self, interval, e):
        if interval[0] >= interval[1]:
            print(f"Ошибка: некорректный интервал - {interval}")
            exit()

        if e >= 1 or e < 0:
            print(f"Ошибка: некорректное значение e - {e}")
            exit()


    #  ввод всех параметров
    def __input_params(self):
        
        print("Input a: ", end="")
        self.interval[0] = self.__get_param("a", float, input)

        print("Input b: ", end="")
        self.interval[1] = self.__get_param("b", float, input)

        print("Input e: ", end="")
        self.e = self.__get_param("e", float, input)
        
        print()   

    # чтение всех параметов из файла
    def __read_params(self, file_name):
        try:
            with open(file_name) as file:

                self.interval[0] = self.__get_param("a", float, file.readline)
                self.interval[1] = self.__get_param("b", float, file.readline)
                self.e = self.__get_param("e", float, file.readline)
        except:
            print(f"Incorrect file name: {file_name}")  
            exit()

    # получение 1 параметра
    def __get_param(self, name, type, func):
        try:
            return type(func())
        except:
            print(f"Incorrect {name}")  
            exit()