def _rectangle_rule(func, a, b, n, frac):
    """Обобщённое правило прямоугольников."""
    dx = 1.0 * (b - a) / n
    sum = 0.0
    xstart = a + frac * dx # 0 <= frac <= 1 задаёт долю смещения точки, 
                           # в которой вычисляется функция,
                           # от левого края отрезка dx
    for i in range(n):
        sum += func(xstart + i * dx)

    return sum * dx

def midpoint_rectangle_rule(func, a, b, n):
    """Правило прямоугольников со средней точкой"""
    return _rectangle_rule(func, a, b, n, 0.5)

class TrapezoidRule:
    @classmethod
    def trapezoid_rule(self, func, a, b, n = 4, e = 1e-4):
        """Правило трапеций
        e - желаемая относительная точность вычислений
        n0 - начальное число отрезков разбиения"""
        old_ans = 0.0
        dx = (b - a) / n
        ans = 0.5 * (func(a) + func(b))

        for i in range(1, n):
            ans += func(a + i * dx)

        ans *= dx
        err_est = max(1, abs(ans))
        while (err_est > e):
            old_ans = ans
            ans = 0.5 * (ans + midpoint_rectangle_rule(func, a, b, n)) # новые точки для уточнения интеграла
                                                                        # добавляются ровно в середины предыдущих отрезков
            n *= 2
            err_est = abs(ans - old_ans)

        return ans, n
    