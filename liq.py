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
        
        /* Cajas de resultados y celdas con texto fino/normal */
        .resultado-box {
            background-color: #ffffff !important;
            padding: 5px 10px !important;
            border-radius: 4px !important;
            border: 1px solid #cbd5e1 !important;
            margin-bottom: 3px !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
            text-align: center !important;
            min-height: 28px !important;
        }
        
        /* Caja específica para la tabla alineada a la izquierda */
        .resultado-box-tabla {
            background-color: #ffffff !important;
            padding: 5px 8px !important;
            border-radius: 4px !important;
            border: 1px solid #cbd5e1 !important;
            margin-bottom: 3px !important;
            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
            text-align: left !important;
            min-height: 28px !important;
        }
        
        .tabla-header {
            background-color: #ffffff !important;
            color: #1e293b !important;
            font-weight: normal;
            text-align: left;
            padding: 5px 8px !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 4px !important;
            font-size: 11px !important;
            text-transform: uppercase;
            min-height: 28px !important;
            display: flex;
            align-items: center;
            justify-content: flex-start;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }
        
        .titulo-seccion-tabla {
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            padding: 6px 10px;
            font-weight: normal;
            text-align: center;
            margin-bottom: 4px;
            border-radius: 4px;
            font-size: 12px !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }
        
        .resultado-label {
            font-family: Arial, sans-serif !important;
            color: #1e293b !important;
            font-weight: normal !important;
            font-size: 12px !important;
        }
        
        .resultado-valor {
            font-family: Arial, sans-serif !important;
            color: #1e293b !important;
            font-weight: normal !important;
            font-size: 12px !important;
        }
        
        .stButton>button {
            background-color: #0284c7 !important;
            color: white !important;
            font-weight: normal !important;
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
            .resultado-box, .resultado-box-tabla, .tabla-header, .titulo-seccion-tabla {
                border: 1px solid #cbd5e1 !important;
                page-break-inside: avoid !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    "<p style='font-weight: normal; margin-bottom: 2px;'>DESCUENTOS:</p>",
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

# Ubicación de Liberar Tope y Valuación Prototípica al lado
col_tope1, col_tope2, col_tope3 = st.columns(3)
with col_tope1:
  var_tope = st.radio("Liberar Tope:", ["NO", "SI"])
with col_tope2:
  var_prototipico = st.radio("Valuación Prototípica:", ["NO", "SI"])

st.markdown("---")

col_sup1, col_sup2, col_val1, col_val2 = st.columns(4)
with col_sup1:
  entry_sup_terreno = st.text_input("Superficie de Terreno (m²):", "300,00")
with col_sup2:
  entry_sup_edificada = st.text_input("Superficie Edificada (m²):", "0,00")

# Cálculo preliminar de superficies para aplicar la fórmula prototípica
try:
  sup_terreno_pre = (
      float(entry_sup_terreno.replace(".", "").replace(",", "."))
      if entry_sup_terreno
      else 0.0
  )
  sup_edificada_pre = (
      float(entry_sup_edificada.replace(".", "").replace(",", "."))
      if entry_sup_edificada
      else 0.0
  )
except ValueError:
  sup_terreno_pre = 0.0
  sup_edificada_pre = 0.0

if sup_terreno_pre <= 10000:
  val_terreno_proto = sup_terreno_pre * 5 * 1261.39
else:
  val_terreno_proto = sup_terreno_pre * 10 * 1261.39

val_edificado_proto = sup_edificada_pre * 50 * 1261.39
valuacion_prototipica_calc = round(val_terreno_proto + val_edificado_proto, 2)

valuacion_calc_str = f"{valuacion_prototipica_calc:,.2f}".replace(
    ",", "X"
).replace(".", ",").replace("X", ".")

# Si es prototípico SÍ, inyectamos el valor calculado sin deshabilitar el input para conservar el color normal
if var_prototipico == "SI":
  default_val_valuacion = valuacion_calc_str
else:
  default_val_valuacion = "300000,00"

with col_val1:
  entry_va = st.text_input("Valuación ($):", value=default_val_valuacion)

with col_val2:
  var_anio = st.selectbox(
      "Valuación año:", ["2023 o anterior", "2024", "2025", "2026"]
  )

try:
  sup_terreno = sup_terreno_pre
  sup_edificada = sup_edificada_pre

  if var_prototipico == "SI":
    va = valuacion_prototipica_calc
  else:
    va = (
        float(entry_va.replace(".", "").replace(",", ".")) if entry_va else 0.0
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
      " normal; text-transform: uppercase; margin-bottom: 4px;'>BASE IMPONIBLE"
      " Y COEFICIENTES</p>",
      unsafe_allow_html=True,
  )

  c_bi, c_ca, c_cu, c_cb, c_cap = st.columns(5)
  with c_bi:
    st.markdown(
        f'<div class="resultado-box"><span'
        f' class="resultado-label">BI:</span><span'
        f' class="resultado-valor">{bi_str}</span></div>',
        unsafe_allow_html=True,
    )
  with c_ca:
    st.markdown(
        f'<div class="resultado-box"><span'
        f' class="resultado-label">CA:</span><span'
        f' class="resultado-valor">{ca}</span></div>',
        unsafe_allow_html=True,
    )
  with c_cu:
    st.markdown(
        f'<div class="resultado-box"><span'
        f' class="resultado-label">CU:</span><span'
        f' class="resultado-valor">{cu}</span></div>',
        unsafe_allow_html=True,
    )
  with c_cb:
    st.markdown(
        f'<div class="resultado-box"><span'
        f' class="resultado-label">CB:</span><span'
        f' class="resultado-valor">{cb}</span></div>',
        unsafe_allow_html=True,
    )
  with c_cap:
    st.markdown(
        f'<div class="resultado-box"><span'
        f' class="resultado-label">CAP:</span><span'
        f' class="resultado-valor">{cap}</span></div>',
        unsafe_allow_html=True,
    )


  def caja_horizontal(descripcion, valor_texto, columna_destino):
    with columna_destino:
      st.markdown(
          f"""
                <div class="resultado-box">
                    <span class="resultado-label">{descripcion}</span>
                    <span class="resultado-valor">{valor_texto}</span>
                </div>
                """,
          unsafe_allow_html=True,
      )


  f1_c1, f1_c2, f1_c3 = st.columns(3)
  caja_horizontal("Límite inferior:", lim_str, f1_c1)
  caja_horizontal("Alícuota:", alic_str, f1_c2)
  caja_horizontal("CFA:", cfa_str, f1_c3)

  f2_c1, f2_c2, f2_c3 = st.columns(3)
  caja_horizontal("TSG Anual:", tasa_anual_str, f2_c1)
  caja_horizontal("TSG Mensual:", tasa_mensual_str, f2_c2)

  f3_c1, f3_c2, f3_c3 = st.columns(3)
  caja_horizontal("Tasa de Salud:", tasa_salud_str, f3_c1)
  caja_horizontal("Tasa de Protección:", tasa_prot_str, f3_c2)
  caja_horizontal("EDENOR:", edenor_str, f3_c3)

  f4_c1, f4_c2, f4_c3 = st.columns(3)
  caja_horizontal("BC:", bc_str, f4_c1)
  caja_horizontal("DA:", da_str, f4_c2)
  caja_horizontal("BE:", be_str, f4_c3)

  st.markdown(
      f"""
        <div class="resultado-box" style="border: 2px solid #1e293b !important; margin-top: 4px; padding: 6px 10px;">
            <span class="resultado-label" style="font-size: 13px;">TSG Total:</span>
            <span class="resultado-valor" style="font-size: 13px;">{tasa_total_str}</span>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # --- TABLA DE CUOTAS ALINEADA A LA IZQUIERDA ---
  st.markdown("<br>", unsafe_allow_html=True)

  st.markdown(
      """
    <div class="titulo-seccion-tabla">
        Aplicación Art. 15° Ord. Fiscal 7437/2025 TO 2026
    </div>
    """,
      unsafe_allow_html=True,
  )

  col_t1, col_t2, col_t3, col_t4, col_t5, col_t6, col_t7 = st.columns(
      [1.3, 1, 1, 1, 1, 1, 1]
  )
  with col_t1:
    st.markdown('<div class="tabla-header">CUOTAS</div>', unsafe_allow_html=True)
  with col_t2:
    st.markdown(
        '<div class="tabla-header">Subtotal</div>', unsafe_allow_html=True
    )
  with col_t3:
    st.markdown(
        '<div class="tabla-header">Descuento BC</div>', unsafe_allow_html=True
    )
  with col_t4:
    st.markdown(
        '<div class="tabla-header">Descuento DA</div>', unsafe_allow_html=True
    )
  with col_t5:
    st.markdown(
        '<div class="tabla-header">Descuento BE</div>', unsafe_allow_html=True
    )
  with col_t6:
    st.markdown(
        '<div class="tabla-header">Descuento Edenor</div>',
        unsafe_allow_html=True,
    )
  with col_t7:
    st.markdown('<div class="tabla-header">TOTAL</div>', unsafe_allow_html=True)

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

  for i in range(1, 13):
    pct = porcentajes_aumento[i - 1]
    nombre_cuota = (
        f"CUOTA {i} ({pct}%)".replace(".0%", "%")
        if pct > 0
        else f"CUOTA {i} (0%)"
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

    r_c1, r_c2, r_c3, r_c4, r_c5, r_c6, r_c7 = st.columns(
        [1.3, 1, 1, 1, 1, 1, 1]
    )

    with r_c1:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-label">{nombre_cuota}</span></div>',
          unsafe_allow_html=True,
      )
    with r_c2:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">{fmt(sub_c)}</span></div>',
          unsafe_allow_html=True,
      )
    with r_c3:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">-</span><span'
          f' class="resultado-valor">{fmt(m_bc_c)}</span></div>'
          if m_bc_c > 0
          else '<div class="resultado-box-tabla"><span'
          ' class="resultado-valor">-</span></div>',
          unsafe_allow_html=True,
      )
    with r_c4:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">-</span><span'
          f' class="resultado-valor">{fmt(m_da_c)}</span></div>'
          if m_da_c > 0
          else '<div class="resultado-box-tabla"><span'
          ' class="resultado-valor">-</span></div>',
          unsafe_allow_html=True,
      )
    with r_c5:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">-</span><span'
          f' class="resultado-valor">{fmt(m_be_c)}</span></div>'
          if m_be_c > 0
          else '<div class="resultado-box-tabla"><span'
          ' class="resultado-valor">-</span></div>',
          unsafe_allow_html=True,
      )
    with r_c6:
      st.markdown(
          f'<div class="resultado-box-tabla"><span'
          f' class="resultado-valor">-</span><span'
          f' class="resultado-valor">{fmt(m_edenor_c)}</span></div>'
          if m_edenor_c > 0
          else '<div class="resultado-box-tabla"><span'
          ' class="resultado-valor">-</span></div>',
          unsafe_allow_html=True,
      )
    with r_c7:
      st.markdown(
          f'<div class="resultado-box-tabla"><span class="resultado-valor"'
          f' style="color:#0284c7;">{fmt(total_cuota)}</span></div>',
          unsafe_allow_html=True,
      )
  # -------------------------------------------------------------------------

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
