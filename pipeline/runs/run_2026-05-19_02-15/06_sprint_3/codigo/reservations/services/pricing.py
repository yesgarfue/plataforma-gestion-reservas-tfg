from decimal import Decimal
from datetime import datetime


class PricingService:
    TASA_COMBUSTIBLE_DEFECTO = Decimal('50.00')
    TASA_COMBUSTIBLE_VELERO = Decimal('0.00')

    @staticmethod
    def calcular_dias(fecha_inicio, fecha_fin):
        """
        Calcula el número de días entre dos fechas.
        """
        delta = fecha_fin - fecha_inicio
        return delta.days

    @staticmethod
    def obtener_tasa_combustible(barco):
        """
        Obtiene la tasa de combustible según la categoría del barco.
        Para veleros es 0, para otros es 50 euros por día.
        """
        if barco.categoria.nombre.lower() == 'velero':
            return PricingService.TASA_COMBUSTIBLE_VELERO
        return PricingService.TASA_COMBUSTIBLE_DEFECTO

    @staticmethod
    def calcular_subtotal_linea(barco, cantidad, fecha_inicio, fecha_fin):
        """
        Calcula el subtotal de una línea de reserva.
        subtotal = (precio_dia + tasa_combustible) * cantidad * dias
        """
        dias = PricingService.calcular_dias(fecha_inicio, fecha_fin)
        tasa_combustible = PricingService.obtener_tasa_combustible(barco)
        precio_por_dia = barco.precio_dia + tasa_combustible
        subtotal = precio_por_dia * cantidad * dias
        return subtotal, dias, tasa_combustible

    @staticmethod
    def calcular_total_reserva(lineas_data):
        """
        Calcula el total de la reserva sumando todos los subtotales.
        lineas_data es una lista de diccionarios con 'subtotal'.
        """
        total = sum(Decimal(str(linea['subtotal'])) for linea in lineas_data)
        return total
