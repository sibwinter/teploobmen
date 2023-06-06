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

    def square_of_ribbed_surfase(self) -> float:
        """Определяем площадь оребренной поверхности радиатора.
        
        при креплении ППП с гладкой стороны, Sор1, м2;
        Sор1=S1+S2+S3, где
        S1=(n‑1) ·L ·b;
        S2=(δ+2 ·h) ·L ·n+2 ·l ·δ;
        S3=2 ·n ·δ ·h."""
        square_1 = (self.n_number_of_edges - 1) * self.L_rib_length * self.b_edge_distanse
        square_2 = (self.sigma_plate + 2 * self.h_rib_height) * self.L_rib_length * self.n_number_of_edges + 2 * self.l_radiator_length * self.sigma_plate
        square_3 = 2 * self.n_number_of_edges * self.sigma_plate * self.h_rib_height
        return square_1 + square_2 + square_3

    def alfa_convection_determine(self) -> float:
        """Определяем коэффициент теплоотдачи конвекцией для гладкой поверхности радиатора.

        aк.гл, Вт/м2*град;
        aк.гл=А1· [(Тр-Тс)/2]^(1/4)
        где А1 определяется по формуле:
        А1=1,424767–0,00251 ·Тм+0,000011 · (Тм)^2-0,0000000013 · (Тм)^3
        Тм=0,5 (Тр+Тс)"""

        Tm = 0.5 * (self.t_average() + self.t_outside)
        A1 = 1,424767 - 0.00251 * Tm + 0.000011 * Tm ^ 2 - 0.0000000013 * Tm ^ 3
        alfa_convection = A1 * ((self.t_average() - self.t_outside)/2) ^ (1/4)
        return alfa_convection

    def alfa_radiation_determine(self) -> float:
        """Определяем коэффициент теплоотдачи излучения для гладкой поверхности радиатора, л.гл, Вт/м2*град.

        Alfaл.гл=ε ·φ ·₣(Тр, Тс), (14)
        где ε – степень черноты тела (для Д‑16 ε=0,4);
        φ – коэффициент облучённости (для гладкой поверхности φ=1);
        ₣(Тр, Тс) – рассчитывается по формуле:
        ₣(Тр, Тс)=5,67 ·10-8 · [(Тр+267)4 – (Тс+267)4]/(Тр-Тс) (15)"""
        epsi = 0.4  # задаем степень черноты тела
        F = 5.67 * 10 ^ (-8) * ((self.t_average() + 267) ^ 4 - (self.t_outside + 267) ^ 4)/(self.t_average() - self.t_outside)
        alfa_radiation = epsi * 1 * F
        return alfa_radiation

    def alfa_summary_determine(self) -> float:
        """Определяем эффективный коэффициент теплоотдачи гладкой поверхности радиатора, гл, Вт/м2*град;.

        Alfaгл = Alfaк.гл + Alfaл.гл"""
        return self.alfa_convection_determine() + self.alfa_radiation_determine()

    def power_of_smooth_surface_define(self) -> float:
        """Определяем мощность, рассеиваемая гладкой поверхностью радиатора, Ргл, Вт.

        Ргл=гл·Sгл· (Тр-Тс)"""
        power_of_smooth_surface = self.alfa_summary_determine() * self.square_of_non_ribbed_surface() * (self.t_average() - self.t_outside)
        return power_of_smooth_surface

    def resistance_of_smooth_surface_define(self) -> float:
        """15) Определяем тепловое сопротивление гладкой поверхности радиатора, Rгл, град / Вт;.
        Rгл=1/(Alfaгл·Sгл) (18)"""
        resistance_of_smooth_surface = 1 / (self.alfa_summary_determine * self.square_of_non_ribbed_surface())
        return resistance_of_smooth_surface

    def koef_temp_pressure_define(self):
        """Определяем коэффициенты для нахождения относительного температурного напора.

        C=K/M.
        nu = A2(Tm)*b*C
        Здесь какая то откровенная магия. Оставляю эти коэффициенты как внешние данные.
        """
        self.nu = float(input())

    def H_temp_pressure_define(self) -> float:
        """Определяем относительный температурный напор Н.

        напор определяется по магическому графику исходя из коэффициента nu"""

        self.temp_pressure = float(input())
        return self.temp_pressure

    def ambient_temp_between_edges(self) -> float:
        """Определяем температуру окружающей среды между рёбрами, Тс1, °С;.

        Тс1=(Тр+Тс)/2
        """
        result = (self.t_average - self.t_outside) / 2
        return result

