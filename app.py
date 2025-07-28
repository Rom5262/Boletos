
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from limpieza import procesar_datos

@st.cache_data
def load_data():
    """Carga los datos limpios y procesados."""
    return procesar_datos()

st.set_page_config(
    page_title="📱 Análisis de Negocio de la Venta de Entradas de SHOWZ ",
    layout="wide")

st.title("📱 Análisis de Negocio de la Venta de Entradas de SHOWZ")

st.title("Visualización Dashboard")
st.markdown("### 📊 Visualización de las diferentes Dashboard del Proyecto")

with st.expander("Introducción", expanded=True):
    st.markdown("""
    Esta aplicación demuestra el Análisis en el Uso del Servicio por parte de los clientes para Optimizar los Gastos de Marketing:
    * El Análisis para conocer el dispositivo más utilizado para ingresar a la Pagina
    * El 
    * El 
    * El
    * El 
    * El 
    * El 
    * El
    * El 
     """)

final_data = load_data()  
visitas, pedidos, gastos = final_data 

st.markdown("---")
st.title('VISITAS')    
st.markdown("---")

if final_data is not None:
    with st.expander("Analisis conexión por Dispositivo", expanded=True):
        st.title('')
        st.markdown("---")

    if 'Device' in final_data.columns: 
            tipo_dispositivo = final_data['Device'].value_counts()
    else:
            st.warning("La columna 'Device' no se encontró en los datos. No se puede generar el gráfico de conexiones por dispositivo.")
            tipo_dispositivo = pd.Series() 

    if not tipo_dispositivo.empty:

        
        fig, ax = plt.subplots(figsize=(8, 5))
        tipo_dispositivo.plot(kind='bar', color='skyblue', ax=ax) 
        ax.set_xlabel('Dispositivo')
        ax.set_ylabel('Conexión')
        ax.set_title('Conexiones por Tipo de Dispositivo')
        st.pyplot(fig)

        

    else:
            st.info("No hay datos para mostrar el gráfico de conexiones por dispositivo.")
else:
    st.error("No se pudieron cargar los datos. Por favor, revisa tu script `limpieza.py` y las rutas de los archivos CSV.")
    