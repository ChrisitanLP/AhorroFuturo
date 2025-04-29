def calcular_amortizacion(monto, tasa_interes, plazo, metodo):
    """
    Calcula la tabla de amortización según el método elegido.
    
    Args:
        monto: Monto del préstamo
        tasa_interes: Tasa de interés anual en porcentaje
        plazo: Plazo en meses
        metodo: 'frances' o 'aleman'
        
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
    
        # Porcentaje de seguro (simulado)
        tasa_seguro_mensual = 0.041 / 100  # 0.041% mensual
        
        if metodo == 'frances':
            # Método francés: cuotas fijas
            if tasa_mensual > 0:
                cuota_capital_interes = monto * (tasa_mensual * (1 + tasa_mensual) ** plazo) / ((1 + tasa_mensual) ** plazo - 1)
            else:
                cuota_capital_interes = monto / plazo
                
            for periodo in range(1, plazo + 1):
                interes = saldo_capital * tasa_mensual
                seguro = saldo_capital * tasa_seguro_mensual
                
                capital = cuota_capital_interes - interes
                
                # Para el último período, ajustar capital para que saldo sea exactamente cero
                if periodo == plazo:
                    capital = saldo_capital
                
                saldo_capital = max(0, saldo_capital - capital)  # Asegurar que el saldo no sea negativo
                
                pago_total = capital + interes + seguro
                
                tabla.append({
                    'periodo': periodo,
                    'capital': round(capital, 2),
                    'interes': round(interes, 2),
                    'seguro': round(seguro, 2),
                    'pago_total': round(pago_total, 2),
                    'saldo': round(saldo_capital, 2)
                })
        
        elif metodo == 'aleman':
            # Método alemán: amortización constante
            capital_fijo = monto / plazo
            
            for periodo in range(1, plazo + 1):
                interes = saldo_capital * tasa_mensual
                seguro = saldo_capital * tasa_seguro_mensual
                
                # Para el último período, ajustar capital para que saldo sea exactamente cero
                if periodo == plazo:
                    capital_fijo = saldo_capital
                
                saldo_capital = max(0, saldo_capital - capital_fijo)  # Asegurar que el saldo no sea negativo
                    
                pago_total = capital_fijo + interes + seguro
                
                tabla.append({
                    'periodo': periodo,
                    'capital': round(capital_fijo, 2),
                    'interes': round(interes, 2),
                    'seguro': round(seguro, 2),
                    'pago_total': round(pago_total, 2),
                    'saldo': round(saldo_capital, 2)
                })
        else:
            raise ValueError(f"Método de pago no válido: {metodo}")
        
        return tabla
    except Exception as e:
        import traceback
        print(f"Error en calcular_amortizacion: {str(e)}")
        print(traceback.format_exc())
        raise