from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import TipoCredito, Credito
from .utils.calculadora import calcular_amortizacion, calcular_tasa_interes
from .forms import SimuladorForm
import json
import logging

# Configurar logger
logger = logging.getLogger(__name__)

def simulador_credito(request):
    """Vista para mostrar el simulador de crédito"""
    tipos_credito = TipoCredito.objects.all()
    return render(request, 'creditos/simulador_credito.html', {'tipos_credito': tipos_credito})

@csrf_exempt
@require_http_methods(["POST"])
def calcular_credito(request):
    """Vista para calcular la simulación de crédito basada en los parámetros del formulario"""
    try:
        # Obtener datos del formulario
        form = SimuladorForm(request.POST)
        
        # Si el formulario no es válido, retornar errores
        if not form.is_valid():
            logger.warning(f"Formulario inválido: {form.errors}")
            return JsonResponse({'error': json.dumps(form.errors)}, status=400)
        
        # Obtener datos limpios del formulario
        tipo_credito = form.cleaned_data['tipo_credito']
        monto_vivienda = float(form.cleaned_data['monto_vivienda'])
        monto_prestamo = float(form.cleaned_data['monto_prestamo'])
        plazo = int(form.cleaned_data['plazo'])
        metodo_pago = form.cleaned_data['metodo_pago']
        
        # Calcular la tasa de interés basada en el perfil de riesgo
        tasa_interes = calcular_tasa_interes(tipo_credito, monto_prestamo, plazo)
        
        # Calcular tabla de amortización
        try:
            tabla_amortizacion = calcular_amortizacion(
                monto_prestamo, 
                tasa_interes, 
                plazo, 
                metodo_pago,
                tipo_credito  # Pasar el objeto tipo_credito para acceder a las tasas de seguro
            )
        except Exception as e:
            logger.error(f"Error al calcular amortización: {str(e)}")
            return JsonResponse({
                'error': f'Error al calcular la tabla de amortización: {str(e)}'
            }, status=400)
        
        # Calcular totales
        total_interes = sum(cuota['interes'] for cuota in tabla_amortizacion)
        total_capital = sum(cuota['capital'] for cuota in tabla_amortizacion)
        total_seguro = sum(cuota['seguro'] for cuota in tabla_amortizacion)
        total_pago = total_capital + total_interes + total_seguro

        # Si el usuario está autenticado, guardar la simulación
        if request.user.is_authenticated:
            try:
                Credito.objects.create(
                    usuario=request.user,
                    tipo_credito=tipo_credito,
                    monto_vivienda=monto_vivienda,
                    monto_prestamo=monto_prestamo,
                    plazo=plazo,
                    metodo_pago=metodo_pago,
                    tasa_interes_aplicada=tasa_interes,
                    total_interes=total_interes,
                    total_capital=total_capital,
                    total_seguro=total_seguro,
                    total_pago=total_pago
                )
            except Exception as e:
                logger.warning(f"No se pudo guardar el crédito: {str(e)}")
        
        # Recopilar los tipos de seguros específicos que existen en la primera cuota
        primer_cuota = tabla_amortizacion[0] if tabla_amortizacion else {}
        tipos_seguro = {}
        for key, value in primer_cuota.items():
            if key.startswith('seguro_'):
                tipo = key.replace('seguro_', '')
                tipos_seguro[tipo] = 0  # Inicializar el total
        
        # Calcular totales para cada tipo de seguro
        totales_por_seguro = {}
        for tipo in tipos_seguro:
            totales_por_seguro[tipo] = sum(cuota.get(f'seguro_{tipo}', 0) for cuota in tabla_amortizacion)
        
        # Obtener tasas de seguro reales del tipo de crédito
        seguros_dict = tipo_credito.get_seguros()
        
        # Preparar tasas de seguro para enviar al frontend
        tasas_seguro = {
            'tasa_interes_aplicada': tasa_interes
        }
        
        # Agregar cada tasa de seguro al diccionario
        for tipo_seguro, tasa in seguros_dict.items():
            tasas_seguro[tipo_seguro] = float(tasa) / 100  # Convertir de porcentaje a decimal
        
        # Retornar respuesta JSON con los resultados
        return JsonResponse({
            'tabla': tabla_amortizacion,
            'total_interes': total_interes,
            'total_capital': total_capital,
            'total_seguro': total_seguro,
            'total_pago': total_pago,
            'totales_por_seguro': totales_por_seguro,
            'tipos_seguro': list(tipos_seguro.keys()),
            'tasas_seguro': tasas_seguro
        })
        
    except ValueError as e:
        logger.error(f"Error de valor: {str(e)}")
        return JsonResponse({'error': f'Error en formato de datos: {str(e)}'}, status=400)
    except TipoCredito.DoesNotExist:
        logger.error("Tipo de crédito no encontrado")
        return JsonResponse({'error': 'Tipo de crédito no encontrado'}, status=404)
    except Exception as e:
        import traceback
        logger.error(f"Error inesperado: {str(e)}")
        logger.error(traceback.format_exc())
        return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)