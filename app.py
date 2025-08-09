
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from limpieza import procesar_datos 

@st.cache_data
def load_data():
    """
    Carga los datos limpios y procesados.
    Ahora espera una tupla de tres DataFrames (visitas, pedidos, gastos) de procesar_datos().
    """
    return procesar_datos()

st.set_page_config(
    page_title="📱 Análisis de Negocio de la Venta de Entradas de SHOWZ ",
    layout="wide", 
    initial_sidebar_state="expanded" )

st.title("📱 Análisis de Negocio de la Venta de Entradas de SHOWZ")
st.header("Visualización Dashboard") 
st.markdown("### 📊 Visualización de las diferentes Dashboards del Proyecto")

with st.expander("Introducción", expanded=True):
    st.markdown("""
    Esta aplicación demuestra el Análisis en el Uso del Servicio por parte de los clientes para Optimizar los Gastos de Marketing.
    Aquí exploraremos:
    * El análisis para conocer el dispositivo más utilizado para ingresar a la página.
    * El Analisis de la Visualización de los Datos por Mes
    * 
    * ...
    """)

visitas = None
pedidos = None
gastos = None
data_loaded_successfully = False

try:
    visitas, pedidos, gastos = load_data() 
    
    if visitas is not None:
        data_loaded_successfully = True
    else:
        st.error("La función `procesar_datos()` no devolvió los DataFrames correctamente. Revisa `limpieza.py`.")
except Exception as e:
    st.error(f"Error al cargar los datos: {e}. Por favor, revisa tu script `limpieza.py` y las rutas de los archivos CSV.")
    st.info("Asegúrate de que `procesar_datos()` en `limpieza.py` devuelve una tupla de DataFrames (visitas, pedidos, gastos).")

if data_loaded_successfully:
    st.markdown("---")
    st.title('VISITAS') 
    st.markdown("---")

    with st.expander("Analisis conexión por Dispositivo", expanded=True):
        st.subheader("Conexiones por Tipo de Dispositivo") 
        
        if visitas is not None and 'Device' in visitas.columns: 
            tipo_dispositivo = visitas['Device'].value_counts()
            
            if not tipo_dispositivo.empty:
                fig, ax = plt.subplots(figsize=(10, 6)) 
                sns.barplot(x=tipo_dispositivo.index, y=tipo_dispositivo.values, palette='viridis', ax=ax) 
                ax.set_xlabel('Tipo de Dispositivo', fontsize=12)
                ax.set_ylabel('Número de Conexiones', fontsize=12)
                ax.set_title('Conexiones por Tipo de Dispositivo', fontsize=14, fontweight='bold')
                plt.xticks(rotation=45, ha='right') 
                plt.tight_layout() 
                st.pyplot(fig)
                plt.close(fig) 
            else:
                st.info("No hay datos para mostrar el gráfico de conexiones por dispositivo.")
        else:
            st.warning("La columna 'Device' no se encontró en el DataFrame de visitas o el DataFrame no se cargó correctamente. No se puede generar el gráfico de conexiones por dispositivo.")
            st.info("Asegúrate de que la columna 'Device' esté presente en el DataFrame `visitas` de `limpieza.py`.")

if data_loaded_successfully:
    st.markdown("---")
    st.title('PEDIDOS') 
    st.markdown("---")            

    with st.expander("Visualización de los Datos por Mes", expanded=True):
        st.subheader("Histograma de Visualización")
        
        if pedidos is not None and 'Buy Ts' in pedidos.columns:
            fechas_compra = pedidos['Buy Ts'].astype("datetime64[ns]") 
            if not fechas_compra.empty:
                fig, ax = plt.subplots(figsize=(12, 6)) 
                sns.histplot(fechas_compra, bins=15, kde=False, ax=ax, color='lightcoral') 
                ax.set_xlabel('Fecha de Compra', fontsize=12)
                ax.set_ylabel('Número de Pedidos', fontsize=12)
                ax.set_title('Visualización de los Datos por Mes', fontsize=14, fontweight='bold')
                plt.xticks(rotation=45, ha='right') 
                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)    


    with st.expander("Análisis de Clientes que Realizaron Primera Compra", expanded=True):
        col1, col2 = st.columns(2) 

        with col1:
            st.subheader("Tabla Dinámica de Compras por Mes")
            st.markdown("##### Clientes que siguen realizando compras después de la primera")

            if pedidos is not None and 'Buy Ts' in pedidos.columns and 'Uid' in pedidos.columns:
                pedidos['Buy Ts'] = pd.to_datetime(pedidos['Buy Ts']) 
                pedidos['orden_mes'] = pedidos['Buy Ts'].dt.to_period('M') 

                primera_orden_usuario = pedidos.groupby('Uid')['Buy Ts'].min().dt.to_period('M').reset_index()
                primera_orden_usuario.columns = ['Uid', 'primera_orden_mes']

                pedidos_con_primera_orden = pd.merge(pedidos, primera_orden_usuario, on='Uid', how='left')

                if 'Uid' in pedidos_con_primera_orden.columns:
                    tabla_dinamica_pedidos = pedidos_con_primera_orden.pivot_table(
                        index='primera_orden_mes',
                        columns='orden_mes',
                        values='Uid', 
                        aggfunc='nunique' 
                    )
                    
                    if not tabla_dinamica_pedidos.empty:
                        st.dataframe(tabla_dinamica_pedidos) 
                    else:
                        st.info("La tabla dinámica de compras por mes está vacía.")
                else:
                    st.warning("La columna 'Uid' no se encontró en el DataFrame de pedidos. No se puede generar la tabla dinámica.")
            else:
                st.warning("Las columnas 'Buy Ts' o 'Uid' no se encontraron en el DataFrame de pedidos o el DataFrame no se cargó correctamente. No se puede generar la tabla dinámica.")
                st.info("Asegúrate de que las columnas 'Buy Ts' y 'Uid' estén presentes en el DataFrame `pedidos` de `limpieza.py`.")

        with col2:
            st.subheader("Tendencia Diaria de Pedidos")
            st.markdown("##### Número de pedidos realizados por día")

            if pedidos is not None and 'Buy Ts' in pedidos.columns:
                pedidos['Buy Ts'] = pd.to_datetime(pedidos['Buy Ts'])
                pedidos_diarios = pedidos.groupby(pedidos['Buy Ts'].dt.date).size().reset_index(name='Numero de Pedidos')
                pedidos_diarios.columns = ['Fecha', 'Numero de Pedidos']
                pedidos_diarios['Fecha'] = pd.to_datetime(pedidos_diarios['Fecha']) 

                if not pedidos_diarios.empty:
                    fig_line, ax_line = plt.subplots(figsize=(10, 6))
                    sns.lineplot(x='Fecha', y='Numero de Pedidos', data=pedidos_diarios, ax=ax_line, color='darkblue')
                    ax_line.set_xlabel('Fecha', fontsize=12)
                    ax_line.set_ylabel('Número de Pedidos', fontsize=12)
                    ax_line.set_title('Tendencia Diaria de Pedidos', fontsize=14, fontweight='bold')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig_line)
                    plt.close(fig_line)
                else:
                    st.info("No hay datos para mostrar la tendencia diaria de pedidos.")
            else:
                st.warning("La columna 'Buy Ts' no se encontró en el DataFrame de pedidos o el DataFrame no se cargó correctamente. No se puede generar la tendencia diaria de pedidos.")
                st.info("Asegúrate de que la columna 'Buy Ts' esté presente en el DataFrame `pedidos` de `limpieza.py`.")



