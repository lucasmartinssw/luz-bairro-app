"""Calculo de fatura de energia (simplificado) - Portal Luz do Bairro.

Continuidade do Modulo 8: aqui a regra da bandeira tarifaria e aplicada POR kWh
(o defeito proposital do repositorio do Modulo 8 ja esta corrigido).
"""

TARIFA_KWH = 0.95
# Adicional por kWh conforme a bandeira tarifaria
BANDEIRAS = {"verde": 0.0, "amarela": 0.02, "vermelha": 0.05}


def calcular_fatura(kwh, bandeira="verde"):
    if kwh < 0:
        raise ValueError("consumo nao pode ser negativo")
    if bandeira not in BANDEIRAS:
        raise ValueError("bandeira invalida: " + bandeira)
    return round(kwh * (TARIFA_KWH + BANDEIRAS[bandeira]), 2)
