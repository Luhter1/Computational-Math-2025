def _rectangle_rule(func, a, b, n, frac):
    """Обобщённое правило прямоугольников."""
    dx = (b - a) / n
    ans = 0.0
    xstart = a + frac * dx  # 0 <= frac <= 1 задаёт долю смещения точки, 
                            # в которой вычисляется функция,
                            # от левого края отрезка dx
    for i in range(n):
        ans += func(xstart + i * dx)

    return ans*dx

def _rectangle_rule_with_e(func, a, b, n, e, frac):
    ans = _rectangle_rule(func, a, b, n, frac)
    err_est = max(1, abs(ans))

    while (err_est > e):
        old_ans = ans
        ans = _rectangle_rule(func, a, b, 2*n, frac)

        n *= 2
        err_est = abs(ans - old_ans)

    return ans, n

class RectangleRule:

    @classmethod
    def left_rectangle_rule(self, func, a, b, n = 4, e = 1e-4):
        """Правило левых прямоугольников"""
        return _rectangle_rule_with_e(func, a, b, n, e, 0.0)

    @classmethod
    def right_rectangle_rule(self, func, a, b, n = 4, e = 1e-4):
        """Правило правых прямоугольников"""
        return _rectangle_rule_with_e(func, a, b, n, e, 1.0)

    @classmethod
    def midpoint_rectangle_rule(self, func, a, b, n = 4, e = 1e-4):
        """Правило прямоугольников со средней точкой"""
        return _rectangle_rule_with_e(func, a, b, n, e, 0.5)
    