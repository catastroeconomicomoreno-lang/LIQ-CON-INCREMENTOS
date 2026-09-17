# --- CUADRO DE AJUSTES MODERNIZADO (Art. 15 Ord. Fiscal 7437/2024 TO 2025) ---
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown(
      "<p style='font-family: Arial, sans-serif; font-size: 13px; font-weight:"
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

  # Iniciamos la tabla HTML completa en una sola variable
  tabla_html = """
    <table class="tabla-moderna-cuotas">
        <thead>
            <tr>
                <th style="text-align: left;">Cuota</th>
                <th>Subtotal</th>
                <th>Desc. BC</th>
                <th>Desc. DA</th>
                <th>Desc. BE</th>
                <th>Desc. Edenor</th>
                <th style="text-align: right;">Total Cuota</th>
            </tr>
        </thead>
        <tbody>
    """

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

    # Acumulamos cada fila
    tabla_html += f"""
        <tr>
            <td>{nombre_cuota}</td>
            <td>{fmt(sub_c)}</td>
            <td style="color: #64748b;">-{fmt(m_bc_c)}</td>
            <td style="color: #64748b;">-{fmt(m_da_c)}</td>
            <td style="color: #64748b;">-{fmt(m_be_c)}</td>
            <td style="color: #64748b;">-{fmt(m_edenor_c)}</td>
            <td class="td-total-cuota">{fmt(total_cuota)}</td>
        </tr>
        """

  # Cerramos la tabla
  tabla_html += """
        </tbody>
    </table>
    """

  # Renderizamos todo de una sola vez
  st.markdown(tabla_html, unsafe_allow_html=True)
