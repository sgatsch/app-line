
import streamlit as st
import pandas as pd
from datetime import datetime

# Cargar archivo Excel
excel_path = "BBDD analisis line revisada.xlsx"

# Cargar hojas existentes
xls = pd.ExcelFile(excel_path)

# Función para agregar fila a una hoja
def append_to_excel(sheet_name, new_data):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    with pd.ExcelWriter(excel_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

st.title("Carga de Datos - Análisis de Lineouts")

# Paso 1: Info Gral
st.header("1. Información General")
line_id = st.text_input("ID del line")
fecha = st.date_input("Fecha", value=datetime.today())
rival = st.text_input("Rival")
zona = st.selectbox("Zona de cancha", ["Extrema defensa", "Gestación", "Ataque", "Extremo ataque"])
contexto = st.radio("¿Ataque o Defensa?", ["ataque", "defensa"])
score_propio = st.number_input("Score propio", min_value=0)
score_rival = st.number_input("Score rival", min_value=0)
minuto = st.number_input("Minuto", min_value=0, max_value=80)

if st.button("Guardar Info Gral"):
    info = {
        "line_id": line_id, "fecha": fecha, "rival": rival,
        "zona_cancha": zona, "ataque_defensa": contexto,
        "score_propio": score_propio, "score_rival": score_rival, "minuto": minuto
    }
    append_to_excel("Info Gral", info)
    st.success("Información general guardada.")

# Condición principal
if contexto == "ataque":
    st.header("2. Line Ataque")
    cantidad = st.number_input("Cantidad de jugadores", min_value=1)
    tipo = st.text_input("Tipo de ataque")
    presion = st.selectbox("Presión defensa", ["Buena", "Mala"])
    decision = st.text_input("Decisión")
    ejecucion = st.text_input("Ejecución")
    resultado = st.selectbox("Resultado", ["obtención limpia", "obtención sucia", "no obtención", "robada"])

    extra_data = {}
    if resultado == "obtención limpia":
        extra_data["posicion"] = st.text_input("Posición")
        lanzamiento = st.selectbox("Lanzamiento", ["norte", "sur", "pichón"])
        extra_data["lanzamiento_jcc"] = lanzamiento
        if lanzamiento == "norte":
            st.subheader("3. Maul Ataque")
            maul_id = st.text_input("ID del maul")
            armado = st.selectbox("Maul armado", ["si", "no"])
            catcher = st.text_input("Golpe catcher")
            cuñas = st.text_input("Cuñas")
            levantadores = st.text_input("Levantadores")
            resultado_maul = st.selectbox("Resultado del maul", ["maul avanza ok", "derribado", "trabado", "penal favor"])
            metros = st.number_input("Metros", min_value=0)

            maul_data = {
                "line_id": line_id, "maul_id": maul_id, "maul_armado": armado,
                "golpe_catcher": catcher, "cuñas": cuñas, "levantadores": levantadores,
                "resultado_maul": resultado_maul, "metros": metros if resultado_maul == "maul avanza ok" else None
            }
            append_to_excel("Maul Ataque", maul_data)

    elif resultado != "obtención limpia":
        extra_data["error"] = st.text_input("Error (no obtención limpia)")

    ataque_data = {
        "line_id": line_id, "cantidad": cantidad, "tipo_ataque_jcc": tipo,
        "presión_defensa": presion, "decision": decision, "ejecucion": ejecucion,
        "resultado_line": resultado, **extra_data
    }
    if st.button("Guardar Line Ataque"):
        append_to_excel("Line Ataque", ataque_data)
        st.success("Datos de ataque guardados.")

elif contexto == "defensa":
    st.header("2. Line Defensa")
    cantidad = st.number_input("Cantidad de jugadores", min_value=1)
    presion = st.text_input("Presión")
    resultado = st.selectbox("Resultado line", ["obtención limpia", "obtención rival manipulada", "no obtención", "robada"])

    extra_data = {}
    if resultado in ["obtención limpia", "obtención rival manipulada"]:
        extra_data["posicion"] = st.text_input("Posición")
        lanzamiento = st.selectbox("Lanzamiento", ["maul", "pichón", "otro"])
        extra_data["lanzamiento"] = lanzamiento
        if lanzamiento == "maul":
            st.subheader("3. Maul Defensa")
            maul_id = st.text_input("ID del maul")
            tipo = st.text_input("Tipo de defensa maul")
            efectivo = st.selectbox("¿Fue efectivo?", ["si", "no"])
            resultado_ok = st.text_input("Resultado OK") if efectivo == "si" else None
            resultado_nok = st.text_input("Resultado NO OK") if efectivo == "no" else None
            metros = st.number_input("Metros", min_value=0) if resultado_nok == "maul avanza" else None

            maul_data = {
                "line_id": line_id, "maul_id": maul_id, "tipo_defensa_maul": tipo,
                "efectivo": efectivo, "resultado_ok": resultado_ok,
                "resultado_nok": resultado_nok, "metros": metros
            }
            append_to_excel("Maul Defensa", maul_data)

    elif resultado in ["no obtención", "robada"]:
        extra_data["pos_recupera"] = st.text_input("Posición recuperación")

    defensa_data = {
        "line_id": line_id, "cantidad": cantidad, "presion": presion,
        "resultado_line": resultado, **extra_data
    }
    if st.button("Guardar Line Defensa"):
        append_to_excel("Line Defensa", defensa_data)
        st.success("Datos de defensa guardados.")
