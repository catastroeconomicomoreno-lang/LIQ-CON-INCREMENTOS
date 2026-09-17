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

# Estilos CSS con tarjetas súper comprimidas y tipografía optimizada para A4
st.markdown(
    """
    <style>
        .stApp, html, body, [data-testid="stAppViewContainer"],
        label, p, span, div, [data-testid="stWidgetLabel"] p, .stMarkdown p {
            font-family: Arial, sans-serif !important;
            color: #1e293b !important;
            font-size: 12px !important;
        }
        
        div[data-testid="stMarkdownContainer"] p, .stRadio label {
            font-family: Arial, sans-serif !important;
            color: #1e293b !important;
            font-size: 12px !important;
        }
        
        [data-testid="stWidgetLabel"] {
            margin-bottom: 1px !important;
            padding-bottom: 0px !important;
        }
        
        div.row-widget.stRadio > div {
            flex-direction: row !important;
            gap: 8px !important;
        }
        
        /* Tarjetas de resultados ultracompactas */
        .resultado-box-mini {
            background-color: #ffffff !important;
            padding: 3px 6px;
            border-radius: 3px;
            border: 1px solid #cbd5e1 !important;
            margin-bottom: 2px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 1px rgba(0,0,0,0.02);
        }
        
        .resultado-label-mini {
            font-family: Arial, sans-serif !important;
            color: #475569 !important;
            font-weight: bold;
            font-size: 11px !important;
        }
        
        .resultado-valor-mini {
            font-family: Arial, sans-serif !important;
            color: #0f172a !important;
            font-weight: bold;
            font-size: 11px !important;
        }
        
        .stButton>button {
            background-color: #0284c7 !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 4px !important;
            border: none !important;
            padding: 6px 12px !important;
            width: 100% !important;
            font-size: 12px !important;
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
            .resultado-box-mini {
                border: 1px solid #cbd5e1 !important;
                page-break-inside: avoid !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

col_p1, col_p2, col_p3 = st.columns(3)
with col_p2:
  entry_partida = st.text_input("PARTIDA MUNICIPAL N°:")

st.markdown("---")

col_f1_1, col_f1_2, col_f1_3, col_f1_4 = st.columns(4)
with col_f1_1:
  var_estado = st.radio("Estado:", ["EDIFICADO", "BALDIO"])
with col_f1_2:
  var_uso = st.radio("Uso:", ["RESIDENCIAL", "COMERCIAL", "INDUSTRIAL"])
with col_f1_3:
  var_acceso = st.radio("Acceso Principal:", ["NO", "SI"])
with col_f1_4:
  var_zonif = st.selectbox("Zonificación:", ["A/B", "F", "OTRA"])

st.markdown("---")

st.markdown(
    "<p style='font-weight: bold; margin-bottom: 2px;'>DESCUENTOS:</p>",
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

st.markdown("---")

col_tope1, col_tope2, col_tope3 = st.columns(3)
with col_tope1:
  var_tope = st.radio("Liberar Tope:", ["NO", "SI"])

st.markdown("---")

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

  st.markdown("---")
  st.markdown(
      "<p style='font-family: Arial, sans-serif; font-size: 12px; font-weight:"
      " bold; text-transform: uppercase; margin-bottom: 4px;'>BASE IMPONIBLE Y"
      " COEFICIENTES</p>",
      unsafe_allow_html=True,
  )

  # Layout ultracomprimido en 4 columnas para ocupar mucho menos espacio vertical
  c1, c2, c3, c4 = st.columns(4)


  def caja_mini(descripcion, valor_texto, columna):
    with columna:
      st.markdown(
          f"""
                <div class="resultado-box-mini">
                    <span class="resultado-label-mini">{descripcion}</span>
                    <span class="resultado-valor-mini">{valor_texto}</span>
                </div>
                """,
          unsafe_allow_html=True,
      )


  # Columna 1: Coeficientes base
  caja_mini("BI:", bi_str, c1)
  caja_mini("CA:", str(ca), c1)
  caja_mini("CU:", str(cu), c1)

  # Columna 2: Coeficientes y Alícuota
  caja_mini("CB:", str(cb), c2)
  caja_mini("CAP:", str(cap), c2)
  caja_mini("Alícuota:", alic_str, c2)

  # Columna 3: Montos base y Tasas adicionales
  caja_mini("Límite inf:", lim_str, c3)
  caja_mini("CFA:", cfa_str, c3)
  caja_mini("TSG Anual:", tasa_anual_str, c3)

  # Columna 4: Mensual, Salud, Protección y Descuentos agrupados
  caja_mini("TSG Mens:", tasa_mensual_str, c4)
  caja_mini("Salud:", tasa_salud_str, c4)
  caja_mini("Protección:", tasa_prot_str, c4)

  # Fila inferior compacta para Descuentos / Edenor y el Total general destacado
  d1, d2, d3, d4, d5 = st.columns(5)
  caja_mini("BC:", bc_str, d1)
  caja_mini("DA:", da_str, d2)
  caja_mini("BE:", be_str, d3)
  caja_mini("Edenor:", edenor_str, d4)
  caja_mini("TSG Total:", tasa_total_str, d5)

  # Cuadro Totalizador principal resaltado pero compacto
  st.markdown(
      f"""
        <div class="resultado-box-mini" style="border: 2px solid #0284c7 !important; margin-top: 4px; padding: 6px 10px; background-color: #f0f9ff !important;">
            <span class="resultado-label-mini" style="font-size: 13px; font-weight: bold; color: #0369a1;">MONTO FINAL TSG TOTAL:</span>
            <span class="resultado-valor-mini" style="font-size: 13px; font-weight: bold; color: #0369a1;">{tasa_total_str}</span>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # --- TABLA DE CUOTAS COMPRIMIDA (Con Pandas DataFrame) ---
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown(
      "<p style='font-family: Arial, sans-serif; font-size: 12px; font-weight:"
      " bold; text-align: center; text-transform: uppercase; margin-bottom:"
      " 2px;'>2026 - Aplicación Art. 15° Ord. Fiscal 7437/2024 TO 2025</p>",
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
  # -----------------------------------------------------------------------------------------

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("🖨️ IMPRIMIR REPORTE EN HOJA A4"):
    st.markdown("""<script>window.print();</script>""", unsafe_allow_html=True)
    st.success("Abriendo ventana de impresión...")

  ruta_pie = os.path.join(ruta_base, "pie_pagina.png")
  if os.path.exists(ruta_pie):
    st.markdown("<br>", unsafe_allow_html=True)
    st.image(ruta_pie, use_container_width=True)

except ValueError:
  st.error("Revise que los campos numéricos sean válidos.")
