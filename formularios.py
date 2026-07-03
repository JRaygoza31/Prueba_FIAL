# formularios.py
from flask import make_response

from flask import (
    Blueprint,
    render_template,
    render_template_string,
    request,
    redirect
)

from models import db, Evento

from datetime import datetime

import random
import requests

# =========================================================
# BLUEPRINT
# =========================================================

formularios_bp = Blueprint(
    "formularios",
    __name__,
    template_folder="templates"
)

# =========================================================
# TERMINOS Y CONDICIONES
# =========================================================

@formularios_bp.route("/terminos")
def terminos():

    return redirect("/static/CLAUSULAS.pdf")
# =========================================================
# WHATSAPP META
# =========================================================

ACCESS_TOKEN = "EAASe8E2iOG0BRl9q2f7ZAATGaqxpmpw0ZCA1QMEgi2uqHkULz85SY2ZBXIsFJ7q1xzafnPrw9XGKJ7plqN7pHqujKRV8xZBFAGtjKeSlD2zLG120aWIv5M0EyePFLcZCn6O3AMB4iCZCD9kDobOQZATKb0kPBSHfUnOKQ8nXu2khD1tCDoSJJuZAtwvQtT01gxq06QZDZD"
PHONE_NUMBER_ID = "1146952391836103" 

# =========================================================
# FUNCION ENVIAR WHATSAPP
# =========================================================
def enviar_whatsapp_plantilla_confirmacion(
    numero,
    nombre_cliente,
    tipo_fiesta,
    fecha_evento,
    nombre_festejado
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
            "name": "confirmacion_formulario",
            "language": {
                "code": "es_MX"
            },
            "components": [
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
                            "parameter_name": "tipo_fiesta",
                            "text": tipo_fiesta
                        },
                        {
                            "type": "text",
                            "parameter_name": "fecha_evento",
                            "text": fecha_evento.strftime("%d/%m/%Y")
                        },
                        {
                            "type": "text",
                            "parameter_name": "nombre_festejado",
                            "text": nombre_festejado
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
    print("ENVIANDO PLANTILLA A:", numero)
    print("STATUS:", respuesta.status_code)
    print("RESPUESTA:", respuesta.text)
    print("================================")

    return respuesta.status_code == 200





@formularios_bp.route("/prueba_template")
def prueba_template():

    exito = enviar_whatsapp_plantilla_confirmacion(

        "5213113963847",

        "José",

        "Cumpleaños",

        datetime(2026, 7, 20),

        "Pedrito"

    )

    if exito:
        return "✅ Plantilla enviada"

    return "❌ Error al enviar"









# =========================================================
# MENU FORMULARIOS

# =========================================================

@formularios_bp.route("/nuevo_evento")
def nuevo_evento():

    return render_template_string("""

<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Formularios</title>

<link
href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
rel="stylesheet"
>

<link
rel="stylesheet"
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
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
    max-width:760px;
    background:#fff;
    border-radius:35px;
    padding:60px;
    text-align:center;
    box-shadow:0 10px 35px rgba(0,0,0,.05);
}

h1{
    font-size:42px;
    color:#1d275f;
    display:flex;
    justify-content:center;
    align-items:center;
    gap:15px;
    margin-bottom:10px;
}

h1 i{
    color:#ff4f8b;
}

.subtitle{
    color:#777;
    margin-bottom:45px;
}

.buttons{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:25px;
}

.btn-card{
    text-decoration:none;
    color:white;
    padding:40px 25px;
    border-radius:28px;
    transition:.3s;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    gap:15px;
}

.btn-card:hover{
    transform:translateY(-5px);
}

.btn-card i{
    font-size:55px;
}

.cliente{
    background:linear-gradient(135deg,#ff4f8b,#ff7eb3);
}

.convenio{
    background:linear-gradient(135deg,#7c3aed,#9b6bff);
}

</style>

</head>

<body>

<div class="container">

    <h1>
        <i class="bi bi-file-earmark-text-fill"></i>
        Formularios
    </h1>

    <p class="subtitle">
        Selecciona el tipo de formulario 🎉
    </p>

    <div class="buttons">

        <a
            href="/formulario/cliente"
            class="btn-card cliente"
        >

            <i class="bi bi-people-fill"></i>

            <h2>Clientes</h2>

        </a>

        <a
            href="/formulario/convenio"
            class="btn-card convenio"
        >

            <i class="bi bi-file-earmark-richtext-fill"></i>

            <h2>Salones</h2>

        </a>

    </div>

</div>

</body>
</html>

""")

# =========================================================
# FORMULARIO
# =========================================================

@formularios_bp.route(
    "/formulario/<tipo>",
    methods=["GET", "POST"]
)
def formulario(tipo):

    # =====================================================
    # PAQUETES DINAMICOS
    # =====================================================

    if tipo == "cliente":

        paquetes = {

            "Animación": """
⭐ Presentación
⭐ Concurso
⭐ Momento pastel
⭐ Entrega de premios

⏰ 20 minutos

🔊 Audio sin producción
""",

            "Mini Show": """
⭐ Presentación
⭐ Musical
⭐ Concurso
⭐ Momento pastel
⭐ Baile
⭐ Entrega de premios

⏰ 30 minutos

🎈 Audio, humo, burbujas y globos
""",

            "Recepción": """
⭐ Personaje recibe invitados
⭐ Actividad básica

⏰ 40 minutos

🔊 Sin producción
""",

            "Show Completo": """
⭐ Presentación
⭐ Musical
⭐ Concurso
⭐ Carnaval
⭐ Interacciones
⭐ Baile
⭐ Entrega de premios

⏰ 40 minutos

🎈 Audio, humo, burbujas,
globos, telas y pelota gigante
""",

            "Espectáculo": """
⭐ Presentación
⭐ Cuento temático
⭐ Musical
⭐ Concurso
⭐ Carnaval
⭐ Interacciones
⭐ Baile
⭐ Entrega de premios

⏰ 50 minutos

🎈 Audio, humo, burbujas,
papelitos, globos,
telas y pelota gigante
"""
        }

    else:

        paquetes = {

        "Entrega de regalo": """
⭐ Personaje asiste al domicilio
⭐ Realiza entrega

⏰ 10-15 minutos

🔊 Sin producción
""",

        "Convivencia": """
⭐ Personaje acompañado de un dirigente
⭐ Momento del pastel
⭐ Interacción con festejado
⭐ Tiempo de fotos

⏰ 20 minutos

🎈 Mini audio (ambientación y mañanitas)
""",

        "Recepción": """
⭐ Personaje recibe invitados
⭐ Actividad básica

⏰ 40 minutos

🔊 Sin producción
""",

        "Mini Show": """
⭐ Presentación
⭐ Musical
⭐ Concurso
⭐ Momento pastel
⭐ Baile
⭐ Entrega de premios

⏰ 30 minutos

🎈 Audio, humo, burbujas y globos
""",

        "Animación Básica": """
⭐ Presentación
⭐ Musical
⭐ Concurso
⭐ Momento pastel
⭐ Interacciones
⭐ Baile
⭐ Entrega de premios

⏰ 30 minutos

🎈 Audio, humo, burbujas,
papelitos, globos,
telas y pelota gigante
""",

        "Show Completo con Animador": """
⭐ Presentación
⭐ Musical
⭐ Concurso
⭐ Carnaval
⭐ Momento pastel
⭐ Interacciones
⭐ Baile
⭐ Entrega de premios

⏰ 40 minutos

🎈 Audio, humo, burbujas,
papelitos, globos,
carnaval, telas
y pelota gigante
""",

        "Show Completo con Alex": """
⭐ Presentación
⭐ Musical
⭐ Concurso
⭐ Carnaval
⭐ Momento pastel
⭐ Interacciones
⭐ Baile
⭐ Entrega de premios

⏰ 40 minutos

🎈 Audio, humo, burbujas,
papelitos, globos,
zanquero, telas
y pelota gigante
""",

        "Espectáculo con Animador": """
⭐ Presentación
⭐ Cuento o temática
⭐ Musical
⭐ Concurso
⭐ Carnaval
⭐ Momento pastel
⭐ Interacciones
⭐ Baile
⭐ Entrega de premios

⏰ 50 minutos

🎈 Audio, humo, burbujas,
papelitos, globos,
carnaval, telas
y pelota gigante
""",

        "Espectáculo con Alex": """
⭐ Presentación
⭐ Cuento o temática
⭐ Musical
⭐ Concurso
⭐ Carnaval
⭐ Momento pastel
⭐ Interacciones
⭐ Baile
⭐ Entrega de premios

⏰ 50 minutos

🎈 Audio, humo, burbujas,
papelitos, globos,
zanquero, telas
y pelota gigante
"""
    }

    # =====================================================
    # GUARDAR FORMULARIO
    # =====================================================

    if request.method == "POST":

        nombre = request.form["nombre"]

        fecha_evento = datetime.strptime(
            request.form["fecha_evento"],
            "%Y-%m-%d"
        ).date()

        salon = request.form["salon"]

        municipio = request.form["municipio"]

        direccion = request.form["direccion"]

        telefono = request.form["telefono"]
        telefono_secundario = request.form["telefono_secundario"]

        horario_show = request.form["horario_show"]

        horario_evento = request.form["horario_evento"]

        nombre_festejado = request.form["nombre_festejado"]

        tipo_fiesta = request.form["tipo_fiesta"]
        tematica =request.form["tematica"]
        numero_personajes=request.form["numero_personajes"]
        personajes=request.form["personajes"]
        paquete = request.form["paquete"]
        descripcion_paquete = request.form["descripcion_paquete"]
        
        anticipo=float(request.form["anticipo"])
        fecha_anticipo=request.form["fecha_anticipo"]
        imagen_anticipo=request.files.get("imagen_anticipo")

        extras = request.form["extras"]

        anio = datetime.now().year

        ultimo_evento = Evento.query.order_by(
            Evento.id.desc()
        ).first()

        if ultimo_evento:
            consecutivo = ultimo_evento.id + 1
        else:
            consecutivo = 1

        prefijo = "C" if tipo == "cliente" else "S"

        folio_sistema = (
            f"{prefijo}{anio}{consecutivo:04d}"
        )
        
        import os

        ruta_imagen = None

        if imagen_anticipo and imagen_anticipo.filename:

            carpeta = "static/anticipos"
            os.makedirs(carpeta, exist_ok=True)

            nombre_archivo = f"{folio_sistema}_{imagen_anticipo.filename}"
            ruta_imagen = f"{carpeta}/{nombre_archivo}"

            imagen_anticipo.save(ruta_imagen)

        nuevo_evento = Evento(
            nombre=nombre,
            fecha_evento=fecha_evento,
            salon=salon,
            municipio=municipio,
            direccion=direccion,
            telefono=telefono,
            telefono_secundario=telefono_secundario,
            horario_show=horario_show,
            total_horas='',
            horario_evento=horario_evento,
            nombre_festejado=nombre_festejado,
            tipo_fiesta=tipo_fiesta,
            tematica=tematica,
            numero_personajes=numero_personajes,
            personajes=personajes,
            paquete=paquete,
            descripcion_paquete=descripcion_paquete,
            anticipo=anticipo,
            fecha_anticipo=fecha_anticipo if fecha_anticipo else None,
            imagen_anticipo=ruta_imagen,
            costo_total=0,
            restante=0,
            folio_sistema=folio_sistema,
            folio_cliente="",
            extras=extras,
            observaciones=""
        )
        
        db.session.add(nuevo_evento)
        db.session.commit()

        # =====================================================
        # MENSAJE CLIENTE
        # =====================================================

        mensaje_cliente = f'''
🎉 Hola {nombre}

Tu evento ha sido registrado correctamente.

📅 Fecha: {fecha_evento}

🎈 Festejado: {nombre_festejado}

🎭 Paquete: {paquete}

📍 Municipio: {municipio}

Gracias por confiar en nosotros.
'''

        enviar_whatsapp_plantilla_confirmacion(
            "52" + telefono,
            nombre,
            tipo_fiesta,
            fecha_evento,
            nombre_festejado
        )

        # =====================================================
        # MENSAJE ADMIN
        # =====================================================

        mensaje_admin = f'''
🚨 NUEVO EVENTO

👤 Cliente: {nombre}

📞 Teléfono: {telefono}

📅 Fecha: {fecha_evento}

🎉 Fiesta: {tipo_fiesta}

🎭 Paquete: {paquete}
'''

        ##enviar_whatsapp(
        #"528119061808",
        #mensaje_admin
    #)

        return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>

<meta charset="UTF-8">

<title>Evento Registrado</title>

<style>

body{
    font-family:Poppins,sans-serif;
    background:#f7f7fb;
    display:flex;
    justify-content:center;
    align-items:center;
    min-height:100vh;
    padding:30px;
}

.card{
    max-width:700px;
    width:100%;
    background:white;
    border-radius:30px;
    padding:40px;
    box-shadow:0 10px 30px rgba(0,0,0,.08);
}

h1{
    color:#16a34a;
    margin-bottom:20px;
}

.resumen{
    background:#f8fafc;
    padding:20px;
    border-radius:15px;
    line-height:1.9;
    margin-top:20px;
}

.timer{
    margin-top:25px;
    font-weight:bold;
    color:#dc2626;
}

</style>

<script>

let segundos = 10;

function iniciarCuenta(){

    const contador =
        document.getElementById("contador");

    setInterval(() => {

        segundos--;

        contador.innerText = segundos;

        if(segundos <= 0){
    window.location.replace("/nuevo_evento");
}

    },1000);

}

window.onload = iniciarCuenta;

</script>

</head>

<body>

<div class="card">

    <h1>
        ✅ Evento registrado correctamente
    </h1>

    <p>
        Hemos recibido tu información.
    </p>

    <div class="resumen">

        <b>Folio:</b> {{folio}}<br>

        <b>Cliente:</b> {{nombre}}<br>

        <b>Festejado:</b> {{festejado}}<br>

        <b>Fecha:</b> {{fecha}}<br>

        <b>Municipio:</b> {{municipio}}<br>

        <b>Paquete:</b> {{paquete}}<br>

        <b>Horario:</b> {{inicio}} - {{fin}}<br>


    </div>

    <div class="timer">

        Serás redireccionado al inicio en
        <span id="contador">10</span>
        segundos...

    </div>

</div>

</body>
</html>
""",
folio=folio_sistema,
nombre=nombre,
festejado=nombre_festejado,
fecha=fecha_evento,
municipio=municipio,
paquete=paquete,
horario_show=horario_show,
)

# =====================================================
# TITULO
# =====================================================

    titulo = (
        "Formulario Cliente"
        if tipo == "cliente"
        else "Formulario Convenio"
    )

# =====================================================
# MOSTRAR TEMPLATE DEL FORMULARIO
# =====================================================

    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{{ titulo }}</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    background:#f7f7fb;
    font-family:'Poppins',sans-serif;
    padding:30px;
}

.container{
    max-width:1000px;
    margin:auto;
    background:white;
    padding:40px;
    border-radius:30px;
    box-shadow:0 10px 30px rgba(0,0,0,.05);
}

h1{
    color:#1d275f;
    margin-bottom:30px;
    display:flex;
    align-items:center;
    gap:12px;
}

form{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
}

.full{
    grid-column:1/3;
}

.triple{
    display:grid;
    grid-template-columns:1fr 1fr 1fr;
    gap:20px;
    grid-column:1/3;
}

label{
    display:block;
    margin-bottom:8px;
    font-weight:600;
    color:#444;
}

input,
select,
textarea{
    width:100%;
    padding:14px;
    border-radius:14px;
    border:1px solid #ddd;
    font-family:'Poppins';
    font-size:15px;
    transition:.2s;
}

input:focus,
select:focus,
textarea:focus{
    outline:none;
    border-color:#ff7eb3;
    box-shadow:0 0 0 4px rgba(255,126,179,.15);
}

textarea{
    resize:none;
    height:120px;
}

.descripcion-paquete{
    grid-column:1/3;
    background:#fff4f8;
    border:2px dashed #ff7eb3;
    padding:20px;
    border-radius:18px;
    color:#444;
    line-height:1.8;
    white-space:pre-line;
}

button{
    grid-column:1/3;
    border:none;
    background:linear-gradient(135deg,#ff4f8b,#ff7eb3);
    color:white;
    padding:18px;
    border-radius:18px;
    font-size:18px;
    font-weight:600;
    cursor:pointer;
    transition:.3s;
}

button:hover{
    transform:translateY(-3px);
}

.terminos{
    grid-column:1/3;
    margin-top:10px;
}

.check-container{
    display:flex;
    align-items:center;
    gap:12px;
    font-size:14px;
    color:#555;
}

.check-container input{
    width:18px;
    height:18px;
    cursor:pointer;
}

.check-container a{
    color:#7c3aed;
    font-weight:600;
    text-decoration:none;
}

.check-container a:hover{
    text-decoration:underline;
}

@media(max-width:768px){

    form{
        grid-template-columns:1fr;
    }

    .full{
        grid-column:auto;
    }

    .triple{
        grid-template-columns:1fr;
        grid-column:auto;
    }

    button{
        grid-column:auto;
    }

}

</style>

</head>

<body>

<div class="container">

<h1>

    <i class="bi bi-file-earmark-text-fill"></i>

    {{ titulo }}

</h1>

<form method="POST" enctype="multipart/form-data">

    <!-- ================================= -->
    <!-- NOMBRE Y TELEFONO -->
    <!-- ================================= -->

    <div>

        <label>Nombre del cliente</label>

        <input
            type="text"
            name="nombre"
            placeholder=""
            required
        >

    </div>

    <div>

        <label>Teléfono</label>

        <input
            type="text"
            name="telefono"
            pattern="[0-9]{10}"
            maxlength="10"
            placeholder=""
            required
        >

    </div>
    
    <div>

            <label>
                Teléfono secundario
                (opcional)
            </label>

            <input
                type="text"
                name="telefono_secundario"
                pattern="[0-9]{10}"
                maxlength="10"
                placeholder="Ej: mamá o papá"
            >

        </div>
    
    
    

    <!-- ================================= -->
    <!-- SALON -->
    <!-- ================================= -->

    <div class="full">

        <label>
            Nombre del salón o ubicación
        </label>

        <input
            type="text"
            name="salon"
            placeholder="Ej: Salón Fantasía o Casa"
            required
        >

    </div>

    <!-- ================================= -->
    <!-- MUNICIPIO Y FECHA -->
    <!-- ================================= -->

    <div>

        <label>Municipio</label>

        <select
            name="municipio"
            required
        >

            <option value="">
                Selecciona
            </option>

            <option>Monterrey</option>
            <option>San Pedro</option>
            <option>Guadalupe</option>
            <option>San Nicolás</option>

        </select>

    </div>

    <div>

        <label>Fecha del evento</label>

        <input
            type="date"
            name="fecha_evento"
            required
        >

    </div>

    <!-- ================================= -->
    <!-- DIRECCION -->
    <!-- ================================= -->

    <div class="full">

        <label>Calle y número</label>

        <input
            type="text"
            name="direccion"
            placeholder="Ej: Margaritas 2080"
            required
        >

    </div>

<!-- ================================= -->
<!-- HORARIOS -->
<!-- ================================= -->

<div>

<label>
Horario del show
</label>

<input
type="text"
name="horario_show"
placeholder="Ej: 4:00 PM a 6:00 PM"
required
>

</div>

<!-- ================================= -->
<!-- HORA DEL EVENTO -->
<!-- ================================= -->

<div>

<label>
Hora del evento
</label>

<input
type="text"
name="horario_evento"
placeholder="Ej: 5:00 PM - 12:00"
required
>

</div>


    <!-- ================================= -->
    <!-- FESTEJADO -->
    <!-- ================================= -->

    <div>

        <label>Nombre del festejado</label>

        <input
            type="text"
            name="nombre_festejado"
            placeholder=""
            required
        >

    </div>

    <!-- ================================= -->
    <!-- TIPO DE FIESTA -->
    <!-- ================================= -->

    <div class="full">

        <label>Tipo de fiesta</label>

        <select
            name="tipo_fiesta"
            required
        >

            <option value="">
                Selecciona una opción
            </option>

            <option>Cumpleaños</option>
            <option>Bautizo</option>
            <option>Baby Shower</option>

        </select>

    </div>

<div class="full">

<label>
Temática
</label>

<input
type="text"
name="tematica"
placeholder="Ej: Frozen, Princesas, Sonic, Vaquero..."
>

</div>




<!-- NUMERO PERSONAJES -->

<div>

<label>
Número de personajes
</label>

<input
type="number"
name="numero_personajes"
min="1"
value="1"
required
>

</div>

<!-- PERSONAJES -->

<div>

<label>
Personajes
</label>

<input
type="text"
name="personajes"
placeholder="Ej: Elsa, Anna y Olaf"
required
>

</div>


    <!-- ================================= -->
    <!-- PAQUETE DINAMICO -->
    <!-- ================================= -->

    <div class="full">

        <label>Paquete</label>

        <select
            name="paquete"
            id="paquete"
            required
        >

            <option value="">
                Selecciona un paquete
            </option>

            {% for paquete in paquetes %}

            <option value="{{ paquete }}">
                {{ paquete }}
            </option>

            {% endfor %}

        </select>

    </div>
    <!-- ================================= -->
    <!-- DESCRIPCION PAQUETE -->
    <!-- ================================= -->

    <input
    type="hidden"
    name="descripcion_paquete"
    id="descripcion_paquete_input"
    >

    <div
    class="descripcion-paquete"
    id="descripcion_paquete"
    >
    Selecciona un paquete para ver la descripción 🎉
    </div>


    

    <!-- ================================= -->
    <!-- ANTICIPO -->
    <!-- ================================= -->


<div>

<label>
Anticipo
</label>

<input
type="number"
step="0.01"
name="anticipo"
placeholder="Ej: 1500"
required
>

</div>

<!-- FECHA ANTICIPO -->

<div>

<label>
Fecha del anticipo
</label>

<input
type="date"
name="fecha_anticipo"
>

</div>

<!-- IMAGEN ANTICIPO -->

<div class="full">

<label>
Comprobante de anticipo
</label>

<input
type="file"
name="imagen_anticipo"
accept=".jpg,.jpeg,.png,.pdf"
>

</div>
    
    

    <!-- ================================= -->
    <!-- COMENTARIOS -->
    <!-- ================================= -->

    <div class="full">

        <label>Comentarios</label>

        <textarea
            name="extras"
            placeholder="Información adicional del evento..."
        ></textarea>

    </div>

    <!-- ================================= -->
    <!-- TERMINOS -->
    <!-- ================================= -->

    <div class="full terminos">

        <label class="check-container">

            <input
                type="checkbox"
                name="terminos"
                required
            >

            <span>

                He leído y acepto los

                <a href="/terminos" target="_blank">
                    términos y condiciones
                </a>

            </span>

        </label>

    </div>

    <!-- ================================= -->
    <!-- BOTON -->
    <!-- ================================= -->

    <button type="submit">

        Guardar Evento

    </button>

</form>

</div>

<script>


// =====================================
// PAQUETES DINAMICOS
// =====================================

const paquete = document.getElementById(
    "paquete"
)

const descripcion = document.getElementById(
    "descripcion_paquete"
)

const descripcionInput = document.getElementById(
    "descripcion_paquete_input"
)

const paquetes = {{ paquetes | tojson | safe }};

paquete.addEventListener(
    "change",
    () => {

        descripcion.textContent = paquetes[paquete.value];

        descripcionInput.value = paquetes[paquete.value];

    }
)

</script>

</body>
</html>
""",
titulo=titulo,
paquetes=paquetes
)



