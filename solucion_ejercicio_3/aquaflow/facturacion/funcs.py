def calcular_costo_agua(consumo_m3: float, tarifa_m3: float = 850.0)-> float:
    if consumo_m3 < 0:
        raise ValueError("El consumo de metros cúbicos debe ser mayor a 0")
    
    return consumo_m3 * tarifa_m3