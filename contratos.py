# contratos.py

from flask import (
    Blueprint,
    render_template_string,
    request,
    send_file
)

from models import Evento

from io import BytesIO

from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from PyPDF2 import PdfReader, PdfWriter

import fitz
import unicodedata

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
        680,   # subir un poco
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
        11
    )

    can.drawString(
        100,
        635,
        fecha_larga
    )

    # =====================================================
    # CLIENTE
    # =====================================================

    can.drawString(
        100,
        605,
        str(evento.nombre or "").upper()
    )
    
    # =====================================================
    # DIRECCION
    # =====================================================

    can.drawString(
        100,
        575,
        str(evento.direccion or "").upper()
    )
    
     # =====================================================
    # UBICACION
    # =====================================================

    ubicacion = (
        f"{evento.salon} - "
        f"{evento.municipio}"
    ).upper()

    can.drawString(
        150,
        575,
        ubicacion
    )


    # =====================================================
    # TELEFONO
    # =====================================================

    can.drawString(
        100,
        510,
        str(evento.telefono or "")
    )
    
    # =====================================================
    # HORARIO
    # =====================================================

    horario = (
        f"{evento.horario_show} "
        f"({evento.total_horas})"
    ).upper()

    can.drawString(
        100, 480,
        horario
    )

    can.drawString(
        450, 480,
        str(evento.horario_evento or "").upper()
    )
    # =====================================================
    # FESTEJADO
    # =====================================================

    can.drawString(
        100, 445,
        str(evento.nombre_festejado or "").upper()
    )

    # =====================================================
    # PAQUETE
    # =====================================================

    can.drawString(
        130, 333,
        str(evento.paquete or "").upper()
    )

    # =====================================================
    # COMENTARIOS / EXTRAS
    # =====================================================

    can.drawString(105, 215, str(evento.extras or "").upper())
    
    can.drawString(165, 196, str(evento.observaciones or "").upper())

    # =====================================================
    # COSTO, ANTICIPO Y RESTANTE
    # =====================================================

    can.drawString(425, 158, str(evento.costo_total or ""))
    
    can.drawString(425, 140, str(evento.anticipo or ""))
    
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
        Generar Contrato
    </button>

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
                .replace(" ","_")
            )

            nombre_archivo = f"""
{folio_cliente}_{nombre_cliente}
""".strip()

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
    
    
  
  
