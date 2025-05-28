from .Trapezoid import TrapezoidRule

class SimpsonRule:

    @classmethod
    def simpson_rule(self, func, a, b, n = 4, e = 1e-4):
        """Интегрирование методом парабол с заданной точностью.
            e - относительная точность,
            n - число отрезков начального разбиения"""
        """
        SS = (4*T(2n) - T(N))/3
        """
        old_trapez_sum, _ = TrapezoidRule.trapezoid_rule(func, a, b, n, e=float('inf'))
        new_trapez_sum, _ = TrapezoidRule.trapezoid_rule(func, a, b, 2*n, e=float('inf'))
        ans = (4 * new_trapez_sum - old_trapez_sum) / 3

        err_est = max(1, abs(ans))

        while (err_est > e):
            n*=2
            old_ans = ans
            old_trapez_sum = new_trapez_sum
            new_trapez_sum, _ = TrapezoidRule.trapezoid_rule(func, a, b, 2*n, e=float('inf'))

            ans = (4 * new_trapez_sum - old_trapez_sum) / 3
            err_est = abs(old_ans - ans)

        return ans, n