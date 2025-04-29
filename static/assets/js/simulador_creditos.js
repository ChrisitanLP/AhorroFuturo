$(document).ready(function() {
    // Formateo de números
    function formatMoney(value) {
        if (!value) return "$0.00";
        return "$" + parseFloat(value).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    }
    
    function unformatMoney(value) {
        return parseFloat(value.replace(/[$,]/g, '')) || 0;
    }
    
    // Llenar el selector de plazos según el tipo de crédito
    function actualizarPlazos() {
        const tipo = $("#tipo_credito option:selected");
        const minPlazo = parseInt(tipo.data('min-plazo')) || 12;
        const maxPlazo = parseInt(tipo.data('max-plazo')) || 300;
        
        const plazoSelect = $("#plazo");
        plazoSelect.empty();
        plazoSelect.append('<option value="" disabled selected>Selecciona tu plazo</option>');
        
        // Añadir opciones comunes: 1 año, 2 años, etc.
        const plazosComunes = [12, 24, 36, 48, 60, 120, 180, 240, 300];
        
        plazosComunes.forEach(meses => {
            if (meses >= minPlazo && meses <= maxPlazo) {
                const años = meses / 12;
                plazoSelect.append(`<option value="${meses}">${años} ${años === 1 ? 'año' : 'años'} (${meses} meses)</option>`);
            }
        });
    }
    
    // Evento al cambiar tipo de crédito
    document.getElementById("tipo_credito").addEventListener("change", function() {
        const tipoSeleccionado = this.value;
        const tipOption = this.options[this.selectedIndex];
        
        if (tipoSeleccionado) {
            const tasa = parseFloat(tipOption.dataset.tasa);
            const minMonto = parseFloat(tipOption.dataset.minMonto);
            const maxMonto = parseFloat(tipOption.dataset.maxMonto);
            
            // Actualizar valores mínimos
            document.getElementById("min_monto_vivienda").textContent = `Min: $${minMonto.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
            document.getElementById("min_monto_prestamo").textContent = `Min: $${minMonto.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
            
            // Mostrar formulario de simulación
            document.querySelector(".datos-simulacion").style.display = "block";
            
            // Actualizar plazos disponibles
            actualizarPlazos();
            
            // Actualizar tasa en el resumen
            document.querySelector(".info-tasa").textContent = `Con una tasa de interés referencial ${tasa}%`;
        } else {
            document.querySelector(".datos-simulacion").style.display = "none";
        }
    });
    
    // Selección de método de pago
    $(".metodo-card").click(function() {
        $(".metodo-card").removeClass("selected");
        $(this).addClass("selected");
        
        const metodoId = $(this).attr("id");
        $("#metodo_pago").val(metodoId === "metodo-frances" ? "frances" : "aleman");
    });
    
    // Formatear inputs de dinero
    $(".numero-formato").on("input", function() {
        const value = $(this).val().replace(/[^0-9]/g, '');
        
        if (value) {
            const formattedValue = formatMoney(value);
            $(this).val(formattedValue);
        }
    });
    
    // Calcular simulación
    $("#btn-simular").click(function() {
        const tipoCredito = $("#tipo_credito").val();
        const montoVivienda = unformatMoney($("#monto_vivienda").val());
        const montoPrestamo = unformatMoney($("#monto_prestamo").val());
        const plazo = $("#plazo").val();
        const metodoPago = $("#metodo_pago").val();
        
        // Validaciones
        if (!tipoCredito) {
            alert("Por favor selecciona un tipo de crédito");
            return;
        }
        
        if (!montoVivienda) {
            alert("Por favor ingresa el valor de la vivienda");
            return;
        }
        
        if (!montoPrestamo) {
            alert("Por favor ingresa el monto que necesitas que te prestemos");
            return;
        }
        
        if (!plazo) {
            alert("Por favor selecciona un plazo");
            return;
        }
        
        if (!metodoPago) {
            alert("Por favor selecciona un método de pago");
            return;
        }
        
        // Enviar datos para cálculo
        $.ajax({
            url: "{% url 'calcular' %}",
            type: "POST",
            data: {
                tipo_credito: tipoCredito,
                monto_vivienda: montoVivienda,
                monto_prestamo: montoPrestamo,
                plazo: plazo,
                metodo_pago: metodoPago,
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(response) {
                // Actualizar resumen
                const tabla = response.tabla;
                
                if (tabla && tabla.length > 0) {
                    const primeraCuota = tabla[0];
                    
                    // Actualizar valores en el resumen
                    $(".valor-pago").eq(0).text(formatMoney(primeraCuota.capital));
                    $(".valor-pago").eq(1).text(formatMoney(primeraCuota.interes));
                    $(".valor-pago").eq(2).text(formatMoney(primeraCuota.seguro));
                    
                    $(".total-mensual h2").text(formatMoney(primeraCuota.pago_total));
                    
                    const años = Math.floor(plazo / 12);
                    const mesesRestantes = plazo % 12;
                    let textoAños = "";
                    
                    if (años > 0) {
                        textoAños += `${años} ${años === 1 ? 'año' : 'años'}`;
                    }
                    
                    if (mesesRestantes > 0) {
                        if (textoAños) textoAños += " y ";
                        textoAños += `${mesesRestantes} ${mesesRestantes === 1 ? 'mes' : 'meses'}`;
                    }
                    
                    $(".info-plazo").text(`Durante ${plazo} meses (${textoAños})`);
                    
                    // Actualizar detalle del crédito
                    $(".detalle-credito .row").eq(0).find(".col-5").text(formatMoney(montoPrestamo));
                    $(".detalle-credito .row").eq(1).find(".col-5").text(formatMoney(response.total_interes));
                    $(".detalle-credito .row").eq(2).find(".col-5").text(formatMoney(response.total_seguro));
                    $(".detalle-credito .row").eq(3).find(".col-5").text(formatMoney(response.total_pago));
                    
                    // Guardar tabla para mostrarla después
                    window.tablaAmortizacion = tabla;
                }
            },
            error: function(xhr, status, error) {
                console.error("Error en la simulación", xhr.responseText);
                console.error("Status:", status);
                console.error("Error:", error);
                try {
                    const respuesta = JSON.parse(xhr.responseText);
                    alert("Error: " + (respuesta.error || "Ha ocurrido un error desconocido"));
                } catch(e) {
                    alert("Ha ocurrido un error al calcular la simulación. Por favor intenta nuevamente.");
                }
            }
        });
    });
    
    // Mostrar tabla de amortización
    $("#ver-tabla-amortizacion").click(function(e) {
        e.preventDefault();
        
        if (!window.tablaAmortizacion || window.tablaAmortizacion.length === 0) {
            alert("Primero debes realizar una simulación");
            return;
        }
        
        // Actualizar la información del modal
        $("#modal-tipo-credito").text($("#tipo_credito option:selected").text());
        $("#modal-monto-prestamo").text($("#monto_prestamo").val());
        $("#modal-plazo").text($("#plazo option:selected").text());
        $("#modal-tasa").text($("#tipo_credito option:selected").data('tasa') + "%");
        
        // Calcular totales para el resumen
        const totalCapital = unformatMoney($("#monto_prestamo").val());
        const totalInteres = window.tablaAmortizacion.reduce((sum, cuota) => sum + cuota.interes, 0);
        const totalSeguro = window.tablaAmortizacion.reduce((sum, cuota) => sum + cuota.seguro, 0);
        const totalPago = totalCapital + totalInteres + totalSeguro;
        
        // Actualizar resumen
        $("#modal-total-capital").text(formatMoney(totalCapital));
        $("#modal-total-interes").text(formatMoney(totalInteres));
        $("#modal-total-seguro").text(formatMoney(totalSeguro));
        $("#modal-total-pago").text(formatMoney(totalPago));
        
        // Limpiar tabla anterior
        $("#tabla-amortizacion tbody").empty();
        
        // Llenar tabla con datos
        window.tablaAmortizacion.forEach(function(cuota) {
            $("#tabla-amortizacion tbody").append(`
                <tr>
                    <td class="text-center">${cuota.periodo}</td>
                    <td class="text-end">${formatMoney(cuota.capital)}</td>
                    <td class="text-end">${formatMoney(cuota.interes)}</td>
                    <td class="text-end">${formatMoney(cuota.seguro)}</td>
                    <td class="text-end fw-bold">${formatMoney(cuota.pago_total)}</td>
                    <td class="text-end">${formatMoney(cuota.saldo)}</td>
                </tr>
            `);
        });
        
        // Mostrar modal
        const tablaModal = new bootstrap.Modal(document.getElementById('tablaAmortizacionModal'));
        tablaModal.show();
    });
    
    // Descargar tabla de amortización como PDF
    $("#btn-descargar-tabla").click(function() {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        
        // Configuración de colores y estilos
        const colorPrimario = [41, 128, 185]; // Azul Pichincha
        const colorSecundario = [220, 220, 220]; // Gris claro
        const colorTexto = [60, 60, 60]; // Gris oscuro
        
        // Agregar logo del banco (opcional - puedes agregar código para insertar el logo)
        // doc.addImage(logoBase64, 'PNG', 14, 10, 40, 15);
        
        // Título y subtítulo
        doc.setFillColor(colorPrimario[0], colorPrimario[1], colorPrimario[2]);
        doc.rect(0, 0, doc.internal.pageSize.getWidth(), 25, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(18);
        doc.setFont('helvetica', 'bold');
        doc.text("Tabla de Amortización", 14, 15);
        
        // Información del crédito - Título
        doc.setFillColor(240, 240, 240);
        doc.rect(0, 30, doc.internal.pageSize.getWidth(), 8, 'F');
        doc.setTextColor(colorPrimario[0], colorPrimario[1], colorPrimario[2]);
        doc.setFontSize(12);
        doc.text("Información del Crédito", 14, 36);
        
        // Información del crédito - Contenido
        doc.setTextColor(colorTexto[0], colorTexto[1], colorTexto[2]);
        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        
        const tipoCredito = $("#tipo_credito option:selected").text();
        const montoPrestamo = $("#monto_prestamo").val();
        const plazo = $("#plazo option:selected").text();
        const tasaInteres = $("#tipo_credito option:selected").data('tasa') + "%";
        const metodoPago = $("#metodo_pago").val() === 'frances' ? 'Francés (cuotas fijas)' : 'Alemán (cuotas variables)';
        
        doc.text(`Tipo de Crédito: ${tipoCredito}`, 14, 45);
        doc.text(`Monto del Préstamo: ${montoPrestamo}`, 14, 52);
        doc.text(`Plazo: ${plazo}`, 14, 59);
        doc.text(`Tasa de Interés: ${tasaInteres}`, 14, 66);
        doc.text(`Método de Pago: ${metodoPago}`, 14, 73);
        
        // Resumen del crédito - Título
        doc.setFillColor(240, 240, 240);
        doc.rect(0, 80, doc.internal.pageSize.getWidth(), 8, 'F');
        doc.setTextColor(colorPrimario[0], colorPrimario[1], colorPrimario[2]);
        doc.setFontSize(12);
        doc.text("Resumen del Crédito", 14, 86);
        
        // Resumen del crédito - Contenido
        doc.setTextColor(colorTexto[0], colorTexto[1], colorTexto[2]);
        doc.setFontSize(10);
        
        const totalCapital = unformatMoney($("#monto_prestamo").val());
        const totalInteres = window.tablaAmortizacion.reduce((sum, cuota) => sum + cuota.interes, 0);
        const totalSeguro = window.tablaAmortizacion.reduce((sum, cuota) => sum + cuota.seguro, 0);
        const totalPago = totalCapital + totalInteres + totalSeguro;
        
        doc.text(`Total Capital: ${formatMoney(totalCapital)}`, 14, 95);
        doc.text(`Total Interés: ${formatMoney(totalInteres)}`, 14, 102);
        doc.text(`Total Seguro: ${formatMoney(totalSeguro)}`, 14, 109);
        doc.setFont('helvetica', 'bold');
        doc.text(`Total a Pagar: ${formatMoney(totalPago)}`, 14, 116);
        
        // Tabla de amortización
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(10);
        doc.autoTable({
            head: [['Período', 'Capital', 'Interés', 'Seguro', 'Cuota Total', 'Saldo']],
            body: window.tablaAmortizacion.map(cuota => [
                cuota.periodo,
                formatMoney(cuota.capital),
                formatMoney(cuota.interes),
                formatMoney(cuota.seguro),
                formatMoney(cuota.pago_total),
                formatMoney(cuota.saldo),
            ]),
            startY: 125,
            theme: 'striped',
            headStyles: { 
                fillColor: colorPrimario, 
                textColor: 255,
                fontSize: 10,
                fontStyle: 'bold',
                halign: 'center'
            },
            columnStyles: {
                0: { halign: 'center' },
                1: { halign: 'right' },
                2: { halign: 'right' },
                3: { halign: 'right' },
                4: { halign: 'right' },
                5: { halign: 'right' }
            },
            styles: { 
                fontSize: 9,
                cellPadding: 3
            },
            alternateRowStyles: {
                fillColor: [248, 248, 248]
            }
        });
        
        // Agregar pie de página con disclaimer
        const finalY = doc.lastAutoTable.finalY + 10;
        
        doc.setFontSize(8);
        doc.setFont('helvetica', 'italic');
        doc.setTextColor(100, 100, 100);
        doc.text("* Valores referenciales, no son considerados como una oferta formal de préstamo.", 14, finalY);
        doc.text("La oferta definitiva está sujeta al cumplimiento de las condiciones y políticas referentes a capacidad de pago.", 14, finalY + 4);
        
        // Fecha de generación y pie de página institucional
        const fechaActual = new Date().toLocaleDateString();
        doc.setFontSize(8);
        doc.setFont('helvetica', 'normal');
        doc.text(`Documento generado el ${fechaActual}`, 14, doc.internal.pageSize.getHeight() - 10);
        doc.text("Banco Pichincha - Todos los derechos reservados", doc.internal.pageSize.getWidth() - 90, doc.internal.pageSize.getHeight() - 10);
        
        // Agregar numeración de páginas
        const pageCount = doc.internal.getNumberOfPages();
        for (let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            doc.setFontSize(8);
            doc.text(`Página ${i} de ${pageCount}`, doc.internal.pageSize.getWidth() - 30, doc.internal.pageSize.getHeight() - 10);
        }
        
        // Descargar documento
        doc.save(`Amortizacion-${tipoCredito}-${fechaActual}.pdf`);
    });
});