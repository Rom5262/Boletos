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
        
    except FileNotFoundError as e:
        print(f"Error: Uno de los archivos CSV no fue encontrado. Por favor, verifica la ruta: {e}")
        return None # Retorna None si no se pueden cargar los archivos
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None       

    if 'Start Ts' in visitas.columns and 'End Ts' in visitas.columns:
        visitas['Start Ts'] = pd.to_datetime(visitas['Start Ts'])
        visitas['End Ts'] = pd.to_datetime(visitas['End Ts'])
    else:
        print("Advertencia: Columnas 'Start Ts' o 'End Ts' no encontradas en 'visitas' para conversión a datetime.")

    visitas = visitas.drop_duplicates()
    visitas = visitas.reset_index(drop=True)

    if 'Buy Ts' in pedidos.columns:
        pedidos['Buy Ts'] = pd.to_datetime(pedidos['Buy Ts'])
    else:
        print("Advertencia: Columna 'Buy Ts' no encontrada en 'pedidos' para conversión a datetime.")
        
    pedidos = pedidos.drop_duplicates()
    pedidos = pedidos.reset_index(drop=True)

    if 'dt' in gastos.columns:
        gastos['dt'] = pd.to_datetime(gastos['dt'])
    else:
        print("Advertencia: Columna 'dt' no encontrada en 'gastos' para conversión a datetime.")
        
    gastos = gastos.drop_duplicates() 
    gastos = gastos.reset_index(drop=True)

    return final_data

