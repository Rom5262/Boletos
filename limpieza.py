import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from math import factorial
import numpy as np
from scipy import stats as st


def procesar_datos():
    """
    Carga, limpia y fusiona todos los DataFrames para el análisis.
    Retorna el DataFrame final procesado.
    """
    try:
        
        visitas = pd.read_csv('datos/visits_log_us.csv')
        pedidos = pd.read_csv('datos/orders_log_us.csv')
        gastos = pd.read_csv('datos/costs_us.csv')
        