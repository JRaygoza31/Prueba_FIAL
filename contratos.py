# contratos.py

from flask import (
    Blueprint,
    render_template_string,
    request,
    send_file
)

from models import Evento
from io import BytesIO
import requests
import os
from models import db, Evento
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from PyPDF2 import PdfReader, PdfWriter

import fitz
import unicodedata


ACCESS_TOKEN = "EAASe8E2iOG0BRl9q2f7ZAATGaqxpmpw0ZCA1QMEgi2uqHkULz85SY2ZBXIsFJ7q1xzafnPrw9XGKJ7plqN7pHqujKRV8xZBFAGtjKeSlD2zLG120aWIv5M0EyePFLcZCn6O3AMB4iCZCD9kDobOQZATKb0kPBSHfUnOKQ8nXu2khD1tCDoSJJuZAtwvQtT01gxq06QZDZD"
PHONE_NUMBER_ID = "1146952391836103"
BASE_URL = "https://prueba-fial-4.onrender.com"
ADMIN_WHATSAPP = "528119061808"


# =========================================================
# BLUEPRINT
# =========================================================

generar_contrato_bp = Blueprint(
    "generar_contrato",
    __name__
)

# =========================================================
# MESES EN ESPAÑOL
# =========================================================

MESES_ES = {

    "January": "ENERO",
    "February": "FEBRERO",
    "March": "MARZO",
    "April": "ABRIL",
    "May": "MAYO",
    "June": "JUNIO",
    "July": "JULIO",
    "August": "AGOSTO",
    "September": "SEPTIEMBRE",
    "October": "OCTUBRE",
    "November": "NOVIEMBRE",
    "December": "DICIEMBRE"

}

# =========================================================
# QUITAR ACENTOS
# =========================================================

def quitar_acentos(texto):

    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# =========================================================
# GENERAR CONTRATO PDF
# =========================================================

def generar_pdf(evento):

    packet = BytesIO()

    can = canvas.Canvas(
        packet,
        pagesize=letter
    )

    # =====================================================
    # TODO EL TEXTO EN NEGRO
    # =====================================================

    can.setFillColor(colors.black)

    # =====================================================
    # FOLIO
    # =====================================================

    can.setFont(
        "Helvetica-Bold",
        16
    )

    can.drawString(
        520,   # mover derecha
        690,   # subir un poco
        str(evento.folio_cliente or "")
    )

    # =====================================================
    # FECHA
    # =====================================================

    mes = MESES_ES[
        evento.fecha_evento.strftime("%B")
    ]

    fecha_larga = (
        f"{evento.fecha_evento.day} DE "
        f"{mes} DE "
        f"{evento.fecha_evento.year}"
    )

    can.setFont(
        "Helvetica-Bold",
        12
    )

    can.drawString(
        100,
        645,
        fecha_larga
    )

# =====================================================
# FECHA DEL CONTRATO
# =====================================================

    hoy = datetime.now()

    MESES = {
        1:"ENE",
        2:"FEB",
        3:"MAR",
        4:"ABR",
        5:"MAY",
        6:"JUN",
        7:"JUL",
        8:"AGO",
        9:"SEP",
        10:"OCT",
        11:"NOV",
        12:"DIC"
    }

    hoy = datetime.now()

    fecha_contrato = (
        f" {hoy.day:02d} "
        f"      {MESES[hoy.month]} "
        f"     {hoy.year}"
    )

    can.setFont(
    "Helvetica-Bold",
    16)

    can.drawString(
        422,   # Cambia por la coordenada X
        744,   # Cambia por la coordenada Y
        fecha_contrato
    )



    # =====================================================
    # CLIENTE
    # =====================================================

    can.setFont("Helvetica-Bold",12)

    can.drawString(
        100,
        615,
        str(evento.nombre or "").upper()
    )
    

    # =====================================================
# DIRECCIÓN
# =====================================================

    direccion = (
        f"{evento.direccion}, "
        f"{evento.salon}, "
        f"{evento.municipio}"
    ).upper()

    can.drawString(
        100,
        585,
        direccion
    )

    # =====================================================
    # TELEFONO
    # =====================================================

    can.drawString(
        100,
        520,
        str(evento.telefono or "")
    )
    

    can.drawString(
        215,
        520,
        str(evento.telefono_secundario or "")
    )
    
    # =====================================================
    # HORARIO
    # =====================================================

    horario = (
        f"{evento.horario_show} "
    ).upper()

    can.drawString(
        100, 487,
        horario
    )

    can.drawString(
        450, 487,
        str(evento.horario_evento or "").upper()
    )
    # =====================================================
    # FESTEJADO
    # =====================================================

    can.drawString(
        100, 455,
        str(evento.nombre_festejado or "").upper()
    )

    # =====================================================
    # TEMATICA Y PAQUETE
    # =====================================================

    can.drawString(
        140, 410,
        str(evento.tematica or "").upper()
    )

    can.drawString(
        140, 338,
        str(evento.paquete or "").upper()
    )
    
    can.drawString(
        480, 410,
        str(evento.numero_personajes or "").upper()
    )
    
    can.drawString(
        140, 375,
        str(evento.personajes or "").upper()
    )
    
    can.drawString(
        480, 338,
        str(evento.total_horas or "").upper()
    )
    
    descripcion = (
    str(evento.descripcion_paquete or "")
    .replace("⭐", "")
    .replace("🎈", "")
    .replace("🔊", "")
    .replace("⏰", "")
)

    items = []

    for linea in descripcion.splitlines():

        texto = linea.strip()

        if (
            not texto
            or "MINUTO" in texto.upper()
            or "HORA" in texto.upper()
        ):
            continue

        items.append(texto.upper())

    mitad = (len(items) + 1) // 2

    can.setFont("Helvetica-Bold", 12)

    y_inicial = 290
    espacio = 12

    for i, texto in enumerate(items[:mitad]):
        can.drawString(
            40,
            y_inicial - i * espacio,
            "• " + texto
        )

    for i, texto in enumerate(items[mitad:]):
        can.drawString(
            300,
            y_inicial - i * espacio,
            "• " + texto
        )

    # =====================================================
    # COMENTARIOS / EXTRAS
    # =====================================================

    can.drawString(105, 215, str(evento.extras or "").upper())
    
    can.drawString(165, 196, str(evento.observaciones or "").upper())

    # =====================================================
    # COSTO, ANTICIPO Y RESTANTE
    # =====================================================

    can.drawString(435, 158, str(evento.costo_total or ""))
    
    can.drawString(435, 140, str(evento.anticipo or ""))
    
    can.drawString(445, 105, str(evento.restante or ""))


    # =====================================================
    # TERMINAR PDF
    # =====================================================

    can.save()

    packet.seek(0)

    overlay = PdfReader(packet)

    # =====================================================
    # LEER PLANTILLA
    # =====================================================

    plantilla = PdfReader(
        "plantilla_contrato.pdf"
    )

    salida = PdfWriter()

    pagina = plantilla.pages[0]

    pagina.merge_page(
        overlay.pages[0]
    )

    salida.add_page(pagina)

    output = BytesIO()

    salida.write(output)

    output.seek(0)

    return output

# =========================================================
# PDF A PNG
# =========================================================

def convertir_pdf_a_png(pdf_bytes):

    pdf_bytes.seek(0)

    documento = fitz.open(
        stream=pdf_bytes.read(),
        filetype="pdf"
    )

    pagina = documento.load_page(0)

    pix = pagina.get_pixmap(dpi=300)

    png_bytes = BytesIO(
        pix.tobytes("png")
    )

    png_bytes.seek(0)

    return png_bytes


def enviar_plantilla_contrato_fial(
    numero,
    url_pdf,
    nombre_pdf,
    nombre_cliente,
    telefono,
    nombre_festejado,
    fecha_evento,
    tipo_fiesta,
    paquete,
    municipio
):

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "template",
        "template": {
            "name": "envio_contrato_fial",
            "language": {
                "code": "es_MX"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "document",
                            "document": {
                                "link": url_pdf,
                                "filename": nombre_pdf
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "parameter_name": "nombre_cliente",
                            "text": nombre_cliente
                        },
                        {
                            "type": "text",
                            "parameter_name": "telefono",
                            "text": telefono
                        },
                        {
                            "type": "text",
                            "parameter_name": "nombre_festejado",
                            "text": nombre_festejado
                        },
                        {
                            "type": "text",
                            "parameter_name": "fecha_evento",
                            "text": fecha_evento.strftime("%d/%m/%Y")
                        },
                        {
                            "type": "text",
                            "parameter_name": "tipo_fiesta",
                            "text": tipo_fiesta
                        },
                        {
                            "type": "text",
                            "parameter_name": "paquete",
                            "text": paquete
                        },
                        {
                            "type": "text",
                            "parameter_name": "municipio",
                            "text": municipio
                        }
                    ]
                }
            ]
        }
    }

    respuesta = requests.post(
        url,
        headers=headers,
        json=data
    )

    print("================================")
    print("ENVIANDO CONTRATO FIAL A:", numero)
    print("STATUS:", respuesta.status_code)
    print("RESPUESTA:", respuesta.text)
    print("================================")

    return respuesta.status_code == 200






def enviar_plantilla_contrato_cliente(
    numero,
    url_pdf,
    nombre_pdf,
    nombre_cliente,
    fecha_evento,
    tipo_fiesta
):

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "template",
        "template": {
            "name": "envio_contrato_cliente",
            "language": {
                "code": "es_MX"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "document",
                            "document": {
                                "link": url_pdf,
                                "filename": nombre_pdf
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "parameter_name": "nombre_cliente",
                            "text": nombre_cliente
                        },
                        {
                            "type": "text",
                            "parameter_name": "fecha_evento",
                            "text": fecha_evento.strftime("%d/%m/%Y")
                        },
                        {
                            "type": "text",
                            "parameter_name": "tipo_fiesta",
                            "text": tipo_fiesta
                        }
                    ]
                }
            ]
        }
    }

    respuesta = requests.post(
        url,
        headers=headers,
        json=data
    )

    print("================================")
    print("ENVIANDO CONTRATO A:", numero)
    print("STATUS:", respuesta.status_code)
    print("RESPUESTA:", respuesta.text)
    print("================================")

    return respuesta.status_code == 200



# =========================================================
# HTML
# =========================================================

html = """

<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Generar Contrato</title>

<link
href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
rel="stylesheet"
>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    background:#f7f7fb;
    font-family:'Poppins',sans-serif;
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:30px;
}

.container{
    width:100%;
    max-width:500px;
    background:white;
    padding:40px;
    border-radius:30px;
    box-shadow:0 10px 30px rgba(0,0,0,.05);
}

h1{
    color:#1d275f;
    margin-bottom:30px;
}

label{
    display:block;
    margin-bottom:8px;
    font-weight:600;
    color:#444;
}

input,
select{
    width:100%;
    padding:14px;
    border-radius:14px;
    border:1px solid #ddd;
    margin-bottom:20px;
    font-family:'Poppins';
}

button{
    width:100%;
    border:none;
    background:linear-gradient(
        135deg,
        #ff4f8b,
        #ff7eb3
    );
    color:white;
    padding:18px;
    border-radius:18px;
    font-size:18px;
    font-weight:600;
    cursor:pointer;
}

button:hover{
    opacity:.9;
}

.mensaje{
    margin-top:20px;
    color:red;
    font-weight:600;
}

</style>

</head>

<body>

<div class="container">

<h1>
    Generar Contrato 📄
</h1>

<form method="POST">

    <label>Folio</label>

    <input
        type="text"
        name="folio_cliente"
        required
       
    >

    <label>Formato</label>

    <select
        name="formato"
        required
    >

        <option value="pdf">
            PDF
        </option>

        <option value="png">
            PNG
        </option>

    </select>



    <button type="submit">
    Generar y Enviar Contrato
</button>

    <a
        href="/"
        class="btn-inicio"
    >
        🏠 Volver al inicio
</a>

</form>

{% if mensaje %}

<div class="mensaje">
    {{ mensaje }}
</div>

{% endif %}

</div>

</body>
</html>

"""

# =========================================================
# RUTA
# =========================================================

@generar_contrato_bp.route(
    "/generar_contrato",
    methods=["GET","POST"]
)
@generar_contrato_bp.route(
    "/generar_contrato",
    methods=["GET", "POST"]
)
def generar_contrato():

    mensaje = None

    if request.method == "POST":

        folio_cliente = (
            request.form["folio_cliente"]
            .strip()
            .upper()
        )

        formato = request.form["formato"]

        evento = Evento.query.filter_by(
            folio_cliente=folio_cliente
        ).first()

        if not evento:

            mensaje = f"""
No existe el folio {folio_cliente}
"""

        else:

            pdf = generar_pdf(evento)

            nombre_cliente = quitar_acentos(
                evento.nombre.upper()
                .replace(" ", "_")
            )

            nombre_archivo_base = (
                f"{folio_cliente}_{nombre_cliente}"
            )

            # =============================================
            # GUARDAR PDF PARA WHATSAPP
            # =============================================

            carpeta = "static/contratos"

            os.makedirs(
                carpeta,
                exist_ok=True
            )

            nombre_pdf = f"{nombre_archivo_base}.pdf"

            ruta_pdf = f"{carpeta}/{nombre_pdf}"

            with open(ruta_pdf, "wb") as f:
                f.write(pdf.getbuffer())

            url_pdf = f"{BASE_URL}/{ruta_pdf}"
            print("URL PDF:", url_pdf)

            # =============================================
            # ENVIAR CONTRATO POR WHATSAPP
            # =============================================

            mensaje_cliente = (
                f"📄 Hola {evento.nombre}, "
                f"te compartimos tu contrato de evento.\n\n"
                f"🎉 Festejado: {evento.nombre_festejado}\n"
                f"📅 Fecha: {evento.fecha_evento}\n\n"
                f"Por favor revísalo y cualquier duda "
                f"estamos para ayudarte."
            )

            mensaje_admin = (
                f"📄 CONTRATO GENERADO\n\n"
                f"👤 Cliente: {evento.nombre}\n"
                f"📱 Teléfono: {evento.telefono}\n"
                f"🎉 Festejado: {evento.nombre_festejado}\n"
                f"📅 Fecha: {evento.fecha_evento}"
            )

            envio_cliente = enviar_plantilla_contrato_cliente(
                "521" + evento.telefono,
                url_pdf,
                nombre_pdf,
                evento.nombre,
                evento.fecha_evento,
                evento.tipo_fiesta
            )

            envio_admin = enviar_plantilla_contrato_fial(
                ADMIN_WHATSAPP,
                url_pdf,
                nombre_pdf,
                evento.nombre,
                evento.telefono,
                evento.nombre_festejado,
                evento.fecha_evento,
                evento.tipo_fiesta,
                evento.paquete,
                evento.municipio
            )

            # =============================================
            # MARCAR CONTRATO EN BASE DE DATOS
            # =============================================

            evento.contrato_generado = True

            evento.fecha_contrato = datetime.now()

            if envio_cliente and envio_admin:
                evento.contrato_enviado = True

            db.session.commit()

            pdf.seek(0)

            # =============================================
            # PDF
            # =============================================

            if formato == "pdf":

                return send_file(
                    pdf,
                    as_attachment=True,
                    download_name=nombre_pdf,
                    mimetype="application/pdf"
                )

            # =============================================
            # PNG
            # =============================================

            else:

                png = convertir_pdf_a_png(pdf)

                return send_file(
                    png,
                    as_attachment=True,
                    download_name=f"{nombre_archivo_base}.png",
                    mimetype="image/png"
                )

  # =============================================
            # PDF
            # =============================================
            if formato == "pdf":

                return send_file(

                    pdf,

                    as_attachment=True,

                    download_name=f"""
{nombre_archivo}.pdf
""".strip(),

                    mimetype="application/pdf"
                )

            # =============================================
            # PNG
            # =============================================

            else:

                png = convertir_pdf_a_png(pdf)

                return send_file(

                    png,

                    as_attachment=True,

                    download_name=f"""
{nombre_archivo}.png
""".strip(),

                    mimetype="image/png"
                )

    return render_template_string(
        html,
        mensaje=mensaje
    )
    


if __name__ == "__main__":

    from datetime import datetime

    class Demo:
        pass

    evento = Demo()

    evento.folio_sistema = "C20260001"
    evento.folio_cliente = "F-00025"

    evento.nombre = "JUAN PEREZ GARCIA"
    evento.telefono = "8111234567"
    evento.telefono_secundario = "8187654321"

    evento.fecha_evento = datetime(2026, 8, 15)

    evento.salon = "SALON FANTASIA"
    evento.municipio = "MONTERREY"
    evento.direccion = "AV. LINCOLN 1234"

    evento.horario_show = "4:00 PM A 6:00 PM"
    evento.total_horas = "2 HORAS"
    evento.horario_evento = "5:00 PM"

    evento.nombre_festejado = "SOFIA"
    evento.tipo_fiesta = "CUMPLEAÑOS"

    evento.tematica = "PRINCESAS"

    evento.numero_personajes = 2
    evento.personajes = "ELSA Y ANNA"

    evento.paquete = "ESPECTÁCULO CON ALEX"
    evento.descripcion_paquete = """
    ⭐ Presentación
    ⭐ Musical
    ⭐ Concurso
    ⭐ Momento pastel
    ⭐ Baile
    ⭐ Entrega de premios

    ⏰ 30 minutos

    🎈 Audio, humo, burbujas y globos
    """

    evento.costo_total = 6500
    evento.anticipo = 3000
    evento.restante = 3500

    evento.extras = "PIÑATA Y MAÑANITAS"
    evento.observaciones = "LLEGAR 30 MINUTOS ANTES"

    pdf = generar_pdf(evento)

    with open("Contrato_Demo.pdf", "wb") as f:
        f.write(pdf.getbuffer())

    print("Contrato generado correctamente.")
    







