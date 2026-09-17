import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="LIQUIDADOR TASAS POR SERVICIOS GENERALES - MUNICIPIO DE MORENO",
    layout="wide",
)

ruta_base = os.path.dirname(__file__)
ruta_encabezado = os.path.join(ruta_base, "encabezado.png")

if os.path.exists(ruta_encabezado):
  st.image(ruta_encabezado, use_container_width=True)

# Estilos CSS optimizados para una vista ultra comprimida tipo planilla
st.markdown(
    """
    <style>
        .stApp, html, body, [data-testid="stAppViewContainer"],
        label, p, span, div, [data-testid="stWidgetLabel"] p, .stMarkdown p {
            font-family: Arial, sans-serif !important;
            color: #1e293b !important;
            font-size: 11px !important;
        }
        
        div[data-testid="stMarkdownContainer"] p, .stRadio label {
            font-family: Arial, sans-serif !important;
            color: #1e293b !important;
            font-size: 11px !important;
        }
        
        [data-testid="stWidgetLabel"] {
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
        }
        
        div.row-widget.stRadio > div {
            flex-direction: row !important;
            gap: 6px !important;
        }
        
        /* Tabla de resumen compacto estilo HTML */
        .tabla-resumen {
            width: 100%;
            border-collapse: collapse;
            margin-top: 4px;
            margin-bottom: 4px;
            font-family: Arial, sans-serif;
            background-color: #ffffff;
        }
        .tabla-resumen th {
            background-color: #f1f5f9;
            color: #334155;
            font-size: 11px;
            font-weight: bold;
            text-align: center;
            padding: 4px;
            border: 1px solid #cbd5e1;
        }
        .tabla-resumen td {
            font-size: 11px;
            padding: 4px 6px;
            border: 1px solid #cbd5e1;
            color: #0f172a;
        }
        .td-label {
            font-weight: bold;
            color: #475569;
            background-color: #f8fafc;
            width: 20%;
        }
        .td-val {
            text-align: right;
            width: 30%;
        }
        
        .stButton>button {
            background-color: #0284c7 !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 4px !important;
            border: none !important;
            padding: 4px 10px !important;
            width: 100% !important;
            font-size: 11px !important;
        }

        @media print {
            body, .stApp, [data-testid="stAppViewContainer"] {
                background-color: #ffffff !important;
                color: #000000 !important;
                font-size: 8pt !important;
            }
            header, [data-testid="stSidebar"], [data-testid="stHeader"], .stDeployButton, [data-testid="stDecoration"] {
                display: none !important;
            }
            .stButton {
                display: none !important;
            }
            [data-testid="stAppViewContainer"] {
                overflow: visible !important;
                position: static !important;
            }
            .block-container {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                max-width: 100% !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Filtros de entrada compactos en filas más juntas
col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
with col_p2:
  entry_partida = st.text_input("PARTIDA MUNICIPAL N°:")

col_f1_1, col_f1_2, col_f1_3, col_f1_4 = st.columns(4)
with col_f1_1:
  var_estado = st.radio("Estado:", ["EDIFICADO", "BALDIO"])
with col_f1_2:
  var_uso = st.radio("Uso:", ["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"])
with col_f1_3:
  var_acceso = st.radio("Acceso Principal:", ["NO", "SI"])
with col_f1_4:
  var_zonif = st.selectbox("Zonificación:", ["A/B", "F", "OTRA"])

st.markdown(
    "<p style='font-weight: bold; margin: 2px 0 0 0;'>DESCUENTOS:</p>",
    unsafe_allow_html=True,
)
col_desc1, col_desc2, col_desc3, col_desc4 = st.columns(4)
with col_desc1:
  var_bc = st.radio(
      "Buen Contribuyente (BC 10%):", ["NO", "SI"], horizontal=True
  )
with col_desc2:
  var_da = st.radio("Débito Automático (DA 10%):", ["NO", "SI"], horizontal=True)
with col_desc3:
  var_be = st.radio("Boleta Electrónica (BE 5%):", ["NO", "SI"], horizontal=True)
with col_desc4:
  entry_edenor = st.text_input("EDENOR ($):", "0,00")

col_tope1, col_tope2, col_tope3 = st.columns([1, 1, 2])
with col_tope1:
  var_tope = st.radio("Liberar Tope:", ["NO", "SI"])

col_sup1, col_sup2, col_val1, col_val2 = st.columns(4)
with col_sup1:
  entry_sup_terreno = st.text_input("Superficie de Terreno (m²):", "300,00")
with col_sup2:
  entry_sup_edificada = st.text_input("Superficie Edificada (m²):", "0,00")
with col_val1:
  entry_va = st.text_input("Valuación ($):", "300000,00")
with col_val2:
  var_anio = st.selectbox(
      "Valuación año:", ["2023 o anterior", "2024", "2025", "2026"]
  )

try:
  va = float(entry_va.replace(".", "").replace(",", ".")) if entry_va else 0.0
  sup_terreno = (
      float(entry_sup_terreno.replace(".", "").replace(",", "."))
      if entry_sup_terreno
      else 0.0
  )
  sup_edificada = (
      float(entry_sup_edificada.replace(".", "").replace(",", "."))
      if entry_sup_edificada
      else 0.0
  )

  estado_sel = var_estado
  uso_sel = var_uso
  anio_sel = var_anio

  if anio_sel == "2023 o anterior":
    ca = 19.10
  elif anio_sel == "2024":
    ca = 2.76
  elif anio_sel == "2025":
    ca = 1.36
  else:
    ca = 1.00

  if uso_sel == "RESIDENCIAL":
    cu = 1.0
  elif uso_sel == "COMERCIAL":
    cu = 1.1
  else:
    cu = 1.25

  if estado_sel == "EDIFICADO":
    cb = 1.0
  else:
    cb = 1.6 if sup_terreno <= 500 else 1.7 if sup_terreno <= 5000 else 2.0

  if var_acceso == "SI":
    if uso_sel == "RESIDENCIAL" and estado_sel == "EDIFICADO":
      cap = 1.2
    elif estado_sel == "BALDIO":
      cap = 1.6
    else:
      cap = 1.5
  else:
    cap = 1.0

  bi = round(va * ca * cu * cb * cap, 2)

  if bi <= 5730000:
    lim_inf, cfa_val, alic = 0.0, 107883.00, 0.0
  elif bi <= 6446250:
    lim_inf, cfa_val, alic = 5730000.0, 107883.00, 0.0150
  elif bi <= 7305750:
    lim_inf, cfa_val, alic = 6446250.0, 123095.84, 0.0152
  elif bi <= 8165250:
    lim_inf, cfa_val, alic = 7305750.0, 141843.90, 0.0154
  elif bi <= 12892500:
    lim_inf, cfa_val, alic = 8165250.0, 160838.66, 0.0156
  elif bi <= 21487500:
    lim_inf, cfa_val, alic = 12892500.0, 328337.79, 0.0160
  elif bi <= 30082500:
    lim_inf, cfa_val, alic = 21487500.0, 649028.37, 0.0164
  elif bi <= 38677500:
    lim_inf, cfa_val, alic = 30082500.0, 838975.84, 0.0169
  elif bi <= 47272500:
    lim_inf, cfa_val, alic = 38677500.0, 1096761.73, 0.0170
  elif bi <= 154447750:
    lim_inf, cfa_val, alic = 47272500.0, 1633008.75, 0.0171
  elif bi <= 1000000000:
    lim_inf, cfa_val, alic = 154447750.0, 4201777.78, 0.0173
  else:
    lim_inf, cfa_val, alic = 1000000000.0, 25380696.47, 0.0183

  excedente = max(0.0, bi - lim_inf)
  tasa_anual = round(((excedente * alic) + cfa_val), 2)
  tasa_mensual = round(tasa_anual / 12, 2)

  tasa_proteccion = round(tasa_mensual * 0.095, 2)
  tasa_salud = round(tasa_mensual * 0.105, 2)

  monto_bc = round(tasa_mensual * 0.10, 2) if var_bc == "SI" else 0.0
  base_da = tasa_mensual - monto_bc
  monto_da = round(base_da * 0.10, 2) if var_da == "SI" else 0.0
  base_be = base_da - monto_da
  monto_be = round(base_be * 0.05, 2) if var_be == "SI" else 0.0

  subtotal_con_desc = tasa_mensual - monto_bc - monto_da - monto_be

  monto_edenor = (
      float(entry_edenor.replace(".", "").replace(",", "."))
      if entry_edenor
      else 0.0
  )

  tasa_total = round(
      subtotal_con_desc + tasa_proteccion + tasa_salud - monto_edenor, 2
  )

  if var_tope == "NO" and tasa_total < 4500.0:
    tasa_total = 8900.0 if estado_sel == "BALDIO" else 4500.0


  def fmt(val):
    return (
        f"${val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )


  bi_str = fmt(bi)
  lim_str = fmt(lim_inf)
  cfa_str = fmt(cfa_val)
  tasa_anual_str = fmt(tasa_anual)
  alic_str = f"{alic * 100:.2f}%"
  tasa_mensual_str = fmt(tasa_mensual)
  bc_str = f"-{fmt(monto_bc)}" if monto_bc > 0 else f"-{fmt(0.0)}"
  da_str = f"-{fmt(monto_da)}" if monto_da > 0 else f"-{fmt(0.0)}"
  be_str = f"-{fmt(monto_be)}" if monto_be > 0 else f"-{fmt(0.0)}"
  edenor_str = f"-{fmt(monto_edenor)}" if monto_edenor > 0 else f"-{fmt(0.0)}"
  tasa_prot_str = fmt(tasa_proteccion)
  tasa_salud_str = fmt(tasa_salud)
  tasa_total_str = fmt(tasa_total)

  # --- PLANILLA RESUMEN COMPACTA (UNIFICADA) ---
  st.markdown(
      f"""
    <table class="tabla-resumen">
        <tr>
            <td class="td-label">Base Imponible (BI):</td>
            <td class="td-val">{bi_str}</td>
            <td class="td-label">Límite Inferior:</td>
            <td class="td-val">{lim_str}</td>
            <td class="td-label">TSG Mensual:</td>
            <td class="td-val">{tasa_mensual_str}</td>
        </tr>
        <tr>
            <td class="td-label">Coeficientes (CA / CU):</td>
            <td class="td-val">{ca} / {cu}</td>
            <td class="td-label">CFA:</td>
            <td class="td-val">{cfa_str}</td>
            <td class="td-label">Tasa Protección (9.5%):</td>
            <td class="td-val">{tasa_prot_str}</td>
        </tr>
        <tr>
            <td class="td-label">Coeficientes (CB / CAP):</td>
            <td class="td-val">{cb} / {cap}</td>
            <td class="td-label">Alícuota:</td>
            <td class="td-val">{alic_str}</td>
            <td class="td-label">Tasa Salud (10.5%):</td>
            <td class="td-val">{tasa_salud_str}</td>
        </tr>
        <tr>
            <td class="td-label">Descuentos (BC / DA / BE):</td>
            <td class="td-val" style="font-size:10px;">{bc_str} / {da_str} / {be_str}</td>
            <td class="td-label">Edenor:</td>
            <td class="td-val">{edenor_str}</td>
            <td class="td-label" style="background-color: #e0f2fe; color: #0369a1; font-weight: bold;">MONTO FINAL TSG:</td>
            <td class="td-val" style="background-color: #e0f2fe; color: #0369a1; font-weight: bold; font-size: 12px;">{tasa_total_str}</td>
        </tr>
    </table>
    """,
      unsafe_allow_html=True,
  )

  # --- TABLA DE CUOTAS COMPRIMIDA (Con Pandas DataFrame) ---
  st.markdown(
      "<p style='font-family: Arial, sans-serif; font-size: 11px; font-weight:"
      " bold; text-align: center; text-transform: uppercase; margin: 6px 0 2px"
      " 0;'>2026 - Aplicación Art. 15° Ord. Fiscal 7437/2024 TO 2025</p>",
      unsafe_allow_html=True,
  )

  porcentajes_aumento = [
      0.0,
      0.0,
      0.0,
      8.84,
      0.0,
      0.0,
      8.32,
      0.0,
      0.0,
      5.808,
      0.0,
      0.0,
  ]
  sub_c_acumulado = tasa_mensual
  filas_tabla = []

  for i in range(1, 13):
    pct = porcentajes_aumento[i - 1]
    nombre_cuota = (
        f"CUOTA {i}-2026 ({pct}%)".replace(".0%", "%")
        if pct > 0
        else f"CUOTA {i}-2026 (0%)"
    )

    if pct > 0:
      sub_c_acumulado = round(sub_c_acumulado * (1.0 + (pct / 100.0)), 2)

    sub_c = sub_c_acumulado

    m_bc_c = round(sub_c * 0.10, 2) if var_bc == "SI" else 0.0
    base_da_c = sub_c - m_bc_c
    m_da_c = round(base_da_c * 0.10, 2) if var_da == "SI" else 0.0
    base_be_c = base_da_c - m_da_c
    m_be_c = round(base_be_c * 0.05, 2) if var_be == "SI" else 0.0

    sub_desc_c = sub_c - m_bc_c - m_da_c - m_be_c

    prot_c = round(sub_c * 0.095, 2)
    salud_c = round(sub_c * 0.105, 2)

    m_edenor_c = monto_edenor

    total_cuota = round(sub_desc_c + prot_c + salud_c - m_edenor_c, 2)

    if var_tope == "NO" and total_cuota < 4500.0:
      total_cuota = 8900.0 if estado_sel == "BALDIO" else 4500.0

    filas_tabla.append({
        "Cuota": nombre_cuota,
        "Subtotal": fmt(sub_c),
        "BC": f"-{fmt(m_bc_c)}",
        "DA": f"-{fmt(m_da_c)}",
        "BE": f"-{fmt(m_be_c)}",
        "Edenor": f"-{fmt(m_edenor_c)}",
        "Total Cuota": fmt(total_cuota),
    })

  df_cuotas = pd.DataFrame(filas_tabla)

  st.dataframe(df_cuotas, use_container_width=True, hide_index=True)

  st.markdown("<br>", unsafe_allow_html=True)
  col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
  with col_btn2:
    if st.button("🖨️ IMPRIMIR REPORTE EN HOJA A4"):
      st.markdown("""<script>window.print();</script>""", unsafe_allow_html=True)
      st.success("Abriendo ventana de impresión...")

  ruta_pie = os.path.join(ruta_base, "pie_pagina.png")
  if os.path.exists(ruta_pie):
    st.markdown("<br>", unsafe_allow_html=True)
    st.image(ruta_pie, use_container_width=True)

except ValueError:
  st.error("Revise que los campos numéricos sean válidos.")
