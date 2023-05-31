"""Тестовая модель расчета теплоотводящей пластины.
    Первая версия. Пробуем написать модель радиатора.
"""
# 1. Задаётся мощность, рассеиваемая полупроводниковым прибором, P, Вт.


class Radiator():
    r_pk: float = 2  # тепловое контактное сопротивление между переходом и корпусом, Rпк, 2°С / Вт;
    r_kr: float = 0.5  # тепловое контактное сопротивление корпус – теплоотвод Rкр, 0.5С / Вт
    d_rib_thickness: float  # толщина ребра d
    sigma_plate: float  # толщина плиты теплоотвода δ
    b_edge_distanse: float  # расстояние между рёбрами b
    h_rib_height: float  # высота ребра h
    L_rib_length: float  # протяжённость ребра L
    n_number_of_edges: int  # число ребер радиатора
    l_radiator_length: float  # длина плиты радиатора
    S_square_non_ribbed: float  # площадь гладкой (неоребренной) поверхности радиатора, Sгл, м2

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

    def init_plate_and_rib_parameters(self, d, sigma, b, h, L):
        """Задаем параметры плиты и ребра нашего радиатора."""
        self.d_rib_thickness = d
        self.sigma_plate = sigma
        self.b_edge_distanse = b
        self.h_rib_height = h
        self.L_rib_length = L

    def number_of_adges_determine(self) -> int:
        """Определяем число рёбер, n, шт.
        n=(L+b)/(b+d)"""
        result = (
            (self.L_rib_length + self.b_edge_distanse) /
            (self.b_edge_distanse + self.d_rib_thickness) + 1
        )
        self.n_number_of_edges = result

    def length_of_radiator_plate_determine(self):
        """Определяем длина плиты радиатора, l, м.

        l=b · (n‑1)+2*d (5)"""
        result = (
            self.b_edge_distanse * (self.n_number_of_edges - 1) +
            2 * self.d_rib_thickness)
        self.l_radiator_length = result

    def square_of_non_ribbed_surface(self):
        """Определяем площадь гладкой (неоребренной) поверхности радиатора, Sгл, м2.

        Sгл=L ·l """
        result = self.L_rib_length * self.l_radiator_length
        self.square_of_non_ribbed_surface = result
