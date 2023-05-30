"""Тестовая модель расчета теплоотводящей пластины.
    Первая версия. Пробуем написать модель радиатора.
"""
# 1. Задаётся мощность, рассеиваемая полупроводниковым прибором, P, Вт.


class Radiator():
    r_pk: float = 2  # тепловое контактное сопротивление между переходом и корпусом, Rпк, 2°С / Вт;
    r_kr: float = 0.5  # тепловое контактное сопротивление корпус – теплоотвод Rкр, 0.5С / Вт

    def __init__(self, p: float, t_outside: float, t_limit: float):
        self.p = p
        self.t_outside = t_outside
        self.t_limit = t_limit

    def p_max(self) -> float:
        """ Необходимо сопоставить максимальную мощность рассеяния транзистора при
        допустимой температуре р-п перехода Тп, температуре среды Тс и тепловом
        контактном сопротивлении Rпк с заданной мощностью транзистора"""
        p_max = (self.t_limit - self.t_outside)/self.r_pk
        if self.p > p_max:
            raise ValueError("заданная мощность Р превышает Рмах")
        else:
            return p_max

    def r_termal(self) -> float:
        """Рассчитываем тепловое сопротивление радиатора Rр исх, °С/Bт;"""

        q = 0.96
        try:
            result = q*(
                (self.t_limit-self.t_outside)
                - self.p * (self.r_pk - self.r_kr)
                )/self.p
            return result
        except (ZeroDivisionError, FloatingPointError) as e:
            print(e, "something went wrong")

    def t_average(self) -> float:
        """Определяем средняю поверхностную температуру радиатора Тр, °С:"""
        try:
            result = self.p * self.r_termal() + self.t_outside
            return result
        except Exception as e:
            print(e, "something went wrong")
