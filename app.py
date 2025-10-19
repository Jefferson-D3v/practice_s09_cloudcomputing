import streamlit as st
import psycopg2
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Consulta de Personal Médico", page_icon="🏥", layout="wide")

# Mostrar el contenido del archivo secrets (para depuración opcional)
# st.write(st.secrets)  # <- Puedes descomentar para verificar que se lea correctamente

# Leer credenciales desde secrets
db = st.secrets["postgres"]

# Función para conectar a la base de datos
def get_connection():
    try:
        conn = psycopg2.connect(
            user=db["USER"],
            password=db["PASSWORD"],
            host=db["HOST"],
            port=db["PORT"],
            dbname=db["DBNAME"]
        )
        return conn
    except Exception as e:
        st.error(f"Error de conexión a la base de datos: {e}")
        return None

# Sidebar
st.sidebar.header("🔍 Filtros de búsqueda")
opcion_busqueda = st.sidebar.selectbox("Buscar por:", ["Nombre", "Especialidad"])
termino = st.sidebar.text_input("Ingrese el término de búsqueda:")

# Título principal
st.title("🏥 Aplicativo de Consulta de Personal Médico")

# Conectar a la base de datos
conn = get_connection()
if conn:
    try:
        # Consulta base
        query = "SELECT id, nombre, apellido, especialidad, telefono, email FROM personal_medico"

        # Filtros
        if termino:
            if opcion_busqueda == "Nombre":
                query += f" WHERE LOWER(nombre) LIKE LOWER('%{termino}%')"
            elif opcion_busqueda == "Especialidad":
                query += f" WHERE LOWER(especialidad) LIKE LOWER('%{termino}%')"

        # Ejecutar consulta
        df = pd.read_sql(query, conn)

        # Mostrar resultados
        if df.empty:
            st.warning("No se encontraron resultados.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error al realizar la consulta: {e}")
    finally:
        conn.close()
else:
    st.stop()

st.caption("Desarrollado por Alfredo Jefferson Ayquipa Quispe 🧑‍💻")
