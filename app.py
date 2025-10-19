import streamlit as st
import psycopg2
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Gestión de Personal Médico", page_icon="🏥", layout="wide")

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

# Función para insertar un nuevo médico
def insertar_medico(nombre, apellido, especialidad, telefono, email):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO personal_medico (nombre, apellido, especialidad, telefono, email)
                VALUES (%s, %s, %s, %s, %s);
            """, (nombre, apellido, especialidad, telefono, email))
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"✅ Médico {nombre} {apellido} registrado correctamente.")
        except Exception as e:
            st.error(f"Error al insertar el médico: {e}")
    else:
        st.error("No se pudo conectar a la base de datos.")

# Barra lateral de navegación
st.sidebar.title("🏥 Menú principal")
opcion = st.sidebar.radio("Selecciona una opción:", ["Consultar personal", "Registrar nuevo médico"])

# --------------------------------------------------------------------
# OPCIÓN 1: CONSULTAR PERSONAL MÉDICO
# --------------------------------------------------------------------
if opcion == "Consultar personal":
    st.title("🔍 Consulta de Personal Médico")
    st.sidebar.header("Filtros de búsqueda")

    opcion_busqueda = st.sidebar.selectbox("Buscar por:", ["Nombre", "Especialidad"])
    termino = st.sidebar.text_input("Ingrese el término de búsqueda:")

    conn = get_connection()
    if conn:
        try:
            query = "SELECT id, nombre, apellido, especialidad, telefono, email FROM personal_medico"

            if termino:
                if opcion_busqueda == "Nombre":
                    query += f" WHERE LOWER(nombre) LIKE LOWER('%{termino}%')"
                elif opcion_busqueda == "Especialidad":
                    query += f" WHERE LOWER(especialidad) LIKE LOWER('%{termino}%')"

            df = pd.read_sql(query, conn)

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

# --------------------------------------------------------------------
# OPCIÓN 2: REGISTRAR NUEVO MÉDICO
# --------------------------------------------------------------------
elif opcion == "Registrar nuevo médico":
    st.title("🩺 Registro de Nuevo Médico")

    with st.form("registro_medico"):
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        especialidad = st.text_input("Especialidad")
        telefono = st.text_input("Teléfono")
        email = st.text_input("Email")

        enviar = st.form_submit_button("Registrar")

        if enviar:
            if nombre and apellido and especialidad:
                insertar_medico(nombre, apellido, especialidad, telefono, email)
            else:
                st.warning("Por favor completa los campos obligatorios (nombre, apellido, especialidad).")

st.caption("Desarrollado por Alfredo Jefferson Ayquipa Quispe 🧑‍💻")
