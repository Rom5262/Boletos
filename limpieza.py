
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from math import factorial
import numpy as np
from scipy import stats as st


def procesar_datos():
    """
    Carga, limpia y fusiona todos los DataFrames para el análisis.
    
    Retorna:
        DataFrame: El DataFrame final procesado y fusionado, o None si hay un error.
    """
    try:
        
        visitas = pd.read_csv('datos/visits_log_us.csv')
        pedidos = pd.read_csv('datos/orders_log_us.csv')
        gastos = pd.read_csv('datos/costs_us.csv')
        
    except FileNotFoundError as e:
        print(f"Error: Uno de los archivos CSV no fue encontrado. Por favor, verifica la ruta: {e}")
        return None
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return None

    
    visitas = visitas.drop_duplicates().reset_index(drop=True)
    visitas['Start Ts'] = pd.to_datetime(visitas['Start Ts'], errors='coerce')
    visitas['End Ts'] = pd.to_datetime(visitas['End Ts'], errors='coerce')
    visitas.dropna(subset=['Start Ts', 'End Ts'], inplace=True)
    visitas['mes_inicio'] = visitas['Start Ts'].dt.to_period('M')

    pedidos = pedidos.drop_duplicates().reset_index(drop=True)
    pedidos['Buy Ts'] = pd.to_datetime(pedidos['Buy Ts'], errors='coerce')
    pedidos.dropna(subset=['Buy Ts'], inplace=True)
    pedidos['mes_orden'] = pedidos['Buy Ts'].dt.to_period('M')

    gastos = gastos.drop_duplicates().reset_index(drop=True)
    gastos['dt'] = pd.to_datetime(gastos['dt'], errors='coerce')
    gastos.dropna(subset=['dt'], inplace=True)
    gastos['mes_gasto'] = gastos['dt'].dt.to_period('M')

    primera_compra = pedidos.groupby('Uid')['Buy Ts'].min().to_frame(name='primera_compra_ts').reset_index()
    primera_compra['mes_cohorte'] = primera_compra['primera_compra_ts'].dt.to_period('M')
    
    pedidos = pd.merge(pedidos, primera_compra, on='Uid', how='left')
    
    return visitas, pedidos, gastos

