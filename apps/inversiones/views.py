from django.shortcuts import render
from django.http import JsonResponse
from .models import TipoInversion, PerfilRiesgo, Inversion
from .forms import SimuladorInversionForm
import json
import math

def simulador_inversion(request):
    """Vista para el simulador de inversiones"""
    tipos_inversion = TipoInversion.objects.filter(es_activo=True).order_by('nombre')
    form = SimuladorInversionForm()
    
    context = {
        'tipos_inversion': tipos_inversion,
        'form': form,
    }
    return render(request, 'inversiones/simulador_inversion.html', context)

def calcular_inversion(request):
    """API para calcular resultados de inversión basados en los parámetros proporcionados"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Obtener parámetros
            tipo_inversion_id = data.get('tipo_inversion')
            monto = float(data.get('monto_inversion', 0))
            plazo_meses = int(data.get('plazo', 0))
            reinversion = data.get('reinversion_intereses', False)
            
            # Validar datos básicos
            if not tipo_inversion_id or monto <= 0 or plazo_meses <= 0:
                return JsonResponse({'error': 'Datos incompletos o inválidos'}, status=400)
            
            # Obtener el tipo de inversión
            try:
                tipo = TipoInversion.objects.get(id=tipo_inversion_id)
            except TipoInversion.DoesNotExist:
                return JsonResponse({'error': 'Tipo de inversión no encontrado'}, status=400)
            
            # Validar rangos
            if monto < float(tipo.monto_minimo) or monto > float(tipo.monto_maximo):
                return JsonResponse({'error': f'El monto debe estar entre ${tipo.monto_minimo} y ${tipo.monto_maximo}'}, status=400)
            
            if plazo_meses < tipo.plazo_minimo or plazo_meses > tipo.plazo_maximo:
                return JsonResponse({'error': f'El plazo debe estar entre {tipo.plazo_minimo} y {tipo.plazo_maximo} meses'}, status=400)
            
            # Calcular rentabilidad (usamos un valor promedio entre mínimo y máximo para simplificar)
            tasa_anual = (float(tipo.rentabilidad_anual_minima) + float(tipo.rentabilidad_anual_maxima)) / 2
            tasa_mensual = tasa_anual / 12 / 100  # Convertir a decimal y mensualizar
            
            resultados = []
            monto_acumulado = monto
            interes_total = 0
            
            # Calcular mes a mes
            for mes in range(1, plazo_meses + 1):
                interes_mensual = monto_acumulado * tasa_mensual
                interes_total += interes_mensual
                
                resultados.append({
                    'mes': mes,
                    'capital_inicial': round(monto_acumulado, 2),
                    'interes': round(interes_mensual, 2),
                    'capital_final': round(monto_acumulado + interes_mensual, 2)
                })
                
                # Si hay reinversión, el interés se suma al capital
                if reinversion:
                    monto_acumulado += interes_mensual
            
            capital_final = monto_acumulado if reinversion else monto
            
            # Cálculo de rentabilidad efectiva anual
            if reinversion:
                # Con capitalización mensual
                rentabilidad_efectiva = ((1 + tasa_mensual) ** 12 - 1) * 100
            else:
                # Sin capitalización
                rentabilidad_efectiva = tasa_anual
                
            # Preparar resultado
            resumen = {
                'capital_inicial': round(monto, 2),
                'interes_total': round(interes_total, 2),
                'capital_final': round(capital_final + (0 if reinversion else interes_total), 2),
                'rentabilidad_anual': round(rentabilidad_efectiva, 2),
                'plazo_meses': plazo_meses,
                'plazo_anios': round(plazo_meses / 12, 1),
                'riesgo': tipo.riesgo,
                'resultados_mensuales': resultados
            }

            if request.user.is_authenticated:
                Inversion.objects.create(
                    usuario=request.user,
                    tipo_inversion=tipo,
                    monto_invertido=monto,
                    plazo=plazo_meses,
                    reinversion_intereses=reinversion,
                    interes_total=round(interes_total, 2),
                    capital_final=round(capital_final + (0 if reinversion else interes_total), 2),
                    rentabilidad_anual=round(rentabilidad_efectiva, 2)
                )
            
            return JsonResponse({'success': True, 'data': resumen})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error en el formato de datos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def obtener_datos_tipo_inversion(request, tipo_id):
    """API para obtener detalles de un tipo de inversión específico"""
    try:
        tipo = TipoInversion.objects.get(id=tipo_id)
        data = {
            'nombre': tipo.nombre,
            'descripcion': tipo.descripcion,
            'rentabilidad_minima': float(tipo.rentabilidad_anual_minima),
            'rentabilidad_maxima': float(tipo.rentabilidad_anual_maxima),
            'plazo_minimo': tipo.plazo_minimo,
            'plazo_maximo': tipo.plazo_maximo,
            'monto_minimo': float(tipo.monto_minimo),
            'monto_maximo': float(tipo.monto_maximo),
            'riesgo': tipo.riesgo
        }
        return JsonResponse({'success': True, 'data': data})
    except TipoInversion.DoesNotExist:
        return JsonResponse({'error': 'Tipo de inversión no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)