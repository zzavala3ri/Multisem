from django.shortcuts import render, redirect
from .forms import DiagnosticoForm
from django.core.mail import EmailMessage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.template.loader import render_to_string
from weasyprint import HTML
import os


def crear_diagnostico(request):
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, request.FILES)

        print("📥 FORM RECIBIDO")

        if form.is_valid():
            print("✅ FORMULARIO VÁLIDO")

            diagnostico = form.save()

            try:
                ruta_pdf = generar_pdf(diagnostico)

                print("📄 PDF GENERADO:", ruta_pdf)

                email = EmailMessage(
                    subject="Reporte de Diagnóstico",
                    body="Adjunto el reporte del generador.",
                    from_email="multisem2006@yahoo.com",
                    to=["multisem2006@yahoo.com"],
                )

                email.attach_file(ruta_pdf)

                if diagnostico.foto:
                    print("📸 ADJUNTANDO FOTO")
                    email.attach_file(diagnostico.foto.path)

                print("📤 ENVIANDO CORREO...")
                email.send(fail_silently=False)

                print("✅ CORREO ENVIADO")

            except Exception as e:
                print("❌ ERROR AL ENVIAR CORREO:", e)

            return redirect('/')

        else:
            print("❌ FORM INVALIDO:", form.errors)

    else:
        form = DiagnosticoForm()

    return render(request, 'formulario.html', {'form': form})
def calcular_score(d):
    total = 10
    puntos = 0
    fallas = []

    campos = [
        ('placas', d.placas),
        ('nivel_aceite', d.nivel_aceite),
        ('estructura', d.estructura),
        ('cableado', d.cableado),
        ('tablero', d.tablero),
        ('aceite', d.aceite),
        ('filtro_aceite', d.filtro_aceite),
        ('filtro_aire', d.filtro_aire),
        ('filtro_combustible', d.filtro_combustible),
        ('escape', d.escape),
        ('bateria', d.bateria),
        ('arranca', d.arranca),
    ]

    for nombre, valor in campos:
        valor = str(valor).lower()

        if valor in ['bueno', 'si']:
            puntos += 1
        elif valor in ['malo', 'no']:
            fallas.append(nombre)

    porcentaje = int((puntos / total) * 100)

    return puntos, porcentaje, fallas






from django.conf import settings

def generar_pdf(diagnostico):

    ruta_imagen = None

    if diagnostico.foto:
        ruta_imagen = 'file://' + diagnostico.foto.path

    puntos, porcentaje, fallas = calcular_score(diagnostico)

    html_string = render_to_string('reporte.html', {
        'diagnostico': diagnostico,
        'score': puntos,
        'porcentaje': porcentaje,
        'fallas': fallas,
        'imagen': ruta_imagen,
    })

    ruta_carpeta = os.path.join(settings.MEDIA_ROOT, 'reportes')
    os.makedirs(ruta_carpeta, exist_ok=True)

    archivo = os.path.join(ruta_carpeta, f"reporte_{diagnostico.id}.pdf")

    HTML(string=html_string, base_url=settings.MEDIA_ROOT).write_pdf(archivo)

    return archivo