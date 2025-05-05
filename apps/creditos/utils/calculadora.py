def calcular_amortizacion(monto, tasa_interes, plazo, metodo, tipo_credito=None):
    """
    Calcula la tabla de amortización según el método elegido.
    
    Args:
        monto: Monto del préstamo
        tasa_interes: Tasa de interés anual en porcentaje
        plazo: Plazo en meses
        metodo: 'frances' o 'aleman'
        tipo_credito: Instancia del modelo TipoCredito (opcional)
    
    Returns:
        Lista de diccionarios con la tabla de amortización
    """
    try:
        # Convertir todos los valores a números
        monto = float(monto)
        tasa_interes = float(tasa_interes)
        plazo = int(plazo)
        
        # Validar datos de entrada
        if monto <= 0:
            raise ValueError("El monto debe ser mayor que cero")
        
        if plazo <= 0:
            raise ValueError("El plazo debe ser mayor que cero")
        
        # Convertir tasa anual a mensual
        tasa_mensual = tasa_interes / 100 / 12
        tabla = []
        saldo_capital = monto
        
        # Obtener tasas de seguro del tipo de crédito
        seguros = {}
        if tipo_credito:
            # Intentar obtener los seguros del campo JSON
            seguros = tipo_credito.get_seguros()
        
        # Preparar diccionario de tasas de seguro (convertir de porcentaje a decimal)
        tasas_seguro = {}
        for tipo_seguro, tasa in seguros.items():
            tasas_seguro[tipo_seguro] = float(tasa) / 100 / 12  # Convertir de % anual a decimal mensual
        
        if metodo == 'frances':
            # Método francés: cuotas fijas
            if tasa_mensual > 0:
                cuota_capital_interes = monto * (tasa_mensual * (1 + tasa_mensual)**plazo) / ((1 + tasa_mensual)**plazo - 1)
            else:
                cuota_capital_interes = monto / plazo
            
            for periodo in range(1, plazo + 1):
                interes = saldo_capital * tasa_mensual
                
                # Calcular cada tipo de seguro individual
                seguros_calculados = {}
                seguro_total = 0
                for tipo_seguro, tasa in tasas_seguro.items():
                    valor_seguro = saldo_capital * tasa
                    seguros_calculados[tipo_seguro] = round(valor_seguro, 2)
                    seguro_total += valor_seguro
                
                capital = cuota_capital_interes - interes
                
                # Para el último período, ajustar capital para que saldo sea exactamente cero
                if periodo == plazo:
                    capital = saldo_capital
                
                saldo_capital = max(0, saldo_capital - capital)  # Asegurar que el saldo no sea negativo
                
                pago_total = capital + interes + seguro_total
                
                cuota = {
                    'periodo': periodo,
                    'capital': round(capital, 2),
                    'interes': round(interes, 2),
                    'seguro': round(seguro_total, 2),
                    'pago_total': round(pago_total, 2),
                    'saldo': round(saldo_capital, 2)
                }
                
                # Agregar cada seguro individual al resultado
                for tipo_seguro, valor in seguros_calculados.items():
                    cuota[f'seguro_{tipo_seguro}'] = valor
                
                tabla.append(cuota)
        
        elif metodo == 'aleman':
            # Método alemán: amortización constante
            capital_fijo = monto / plazo
            
            for periodo in range(1, plazo + 1):
                interes = saldo_capital * tasa_mensual
                
                # Calcular cada tipo de seguro individual
                seguros_calculados = {}
                seguro_total = 0
                for tipo_seguro, tasa in tasas_seguro.items():
                    valor_seguro = saldo_capital * tasa
                    seguros_calculados[tipo_seguro] = round(valor_seguro, 2)
                    seguro_total += valor_seguro
                
                # Para el último período, ajustar capital para que saldo sea exactamente cero
                if periodo == plazo:
                    capital_fijo = saldo_capital
                
                saldo_capital = max(0, saldo_capital - capital_fijo)  # Asegurar que el saldo no sea negativo
                
                pago_total = capital_fijo + interes + seguro_total
                
                cuota = {
                    'periodo': periodo,
                    'capital': round(capital_fijo, 2),
                    'interes': round(interes, 2),
                    'seguro': round(seguro_total, 2),
                    'pago_total': round(pago_total, 2),
                    'saldo': round(saldo_capital, 2)
                }
                
                # Agregar cada seguro individual al resultado
                for tipo_seguro, valor in seguros_calculados.items():
                    cuota[f'seguro_{tipo_seguro}'] = valor
                
                tabla.append(cuota)
        else:
            raise ValueError(f"Método de pago no válido: {metodo}")
        
        return tabla
    except Exception as e:
        import traceback
        print(f"Error en calcular_amortizacion: {str(e)}")
        print(traceback.format_exc())
        raise

def calcular_tasa_interes(tipo_credito, monto, plazo):
    """
    Calcula la tasa de interés basada en el monto y plazo del préstamo,
    considerando los rangos mínimos y máximos del tipo de crédito.
    
    Args:
        tipo_credito: Instancia del modelo TipoCredito
        monto: Monto del préstamo
        plazo: Plazo en meses
    
    Returns:
        Tasa de interés calculada (porcentaje)
    """
    # Convertir valores a float para asegurar cálculos correctos
    monto = float(monto)
    plazo = float(plazo)
    monto_minimo = float(tipo_credito.monto_minimo)
    monto_maximo = float(tipo_credito.monto_maximo)
    plazo_minimo = float(tipo_credito.plazo_minimo)
    plazo_maximo = float(tipo_credito.plazo_maximo)
    tasa_min = float(tipo_credito.tasa_interes_minima)
    tasa_max = float(tipo_credito.tasa_interes_maxima)
    
    # Normalizar monto dentro del rango [0,1]
    f_monto = (monto - monto_minimo) / (monto_maximo - monto_minimo)
    f_monto = max(0, min(1, f_monto))  # Asegurar que esté en rango [0,1]
    
    # Normalizar plazo dentro del rango [0,1]
    f_plazo = (plazo - plazo_minimo) / (plazo_maximo - plazo_minimo)
    f_plazo = max(0, min(1, f_plazo))  # Asegurar que esté en rango [0,1]
    
    # El factor de riesgo aumenta con plazos largos y montos bajos
    # A mayor plazo y menor monto, más riesgo, por lo tanto tasa más alta
    riesgo = (1 - f_monto + f_plazo) / 2
    
    # Calcular tasa interpolando entre mínima y máxima según el riesgo
    tasa = tasa_min + riesgo * (tasa_max - tasa_min)
    
    return round(tasa, 2)