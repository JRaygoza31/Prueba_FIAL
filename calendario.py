# calendario.py

from flask import Blueprint, render_template_string, request
from models import Evento, db

from datetime import datetime
import calendar

calendario_bp = Blueprint(
    "calendario2",
    __name__
)

HTML = """

<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Calendario</title>

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
    background:#f5f7fb;
    font-family:'Poppins',sans-serif;
    padding:20px;
}

/* ================================= */
/* CONTENEDOR */
/* ================================= */

.container{
    width:100%;
    max-width:1700px;
    margin:auto;
}

/* ================================= */
/* HEADER */
/* ================================= */

.topbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:25px;
    flex-wrap:wrap;
    gap:20px;
}

.title{
    display:flex;
    align-items:center;
    gap:15px;
}

.title h1{
    color:#1d275f;
    font-size:38px;
}

.title i{
    font-size:40px;
    color:#ff4f8b;
}

/* ================================= */
/* HOME + CONTROLES */
/* ================================= */

.top-actions{
    display:flex;
    align-items:center;
    gap:15px;
    flex-wrap:wrap;
}

.home-btn{
    width:55px;
    height:55px;
    border:none;
    border-radius:18px;
    background:white;
    font-size:22px;
    cursor:pointer;
    box-shadow:0 5px 20px rgba(0,0,0,.05);
    transition:.2s;
    display:flex;
    align-items:center;
    justify-content:center;
    text-decoration:none;
    color:#1d275f;
}

.home-btn:hover{
    transform:translateY(-3px);
    background:#1d275f;
    color:white;
}

.controls{
    display:flex;
    align-items:center;
    gap:12px;
    flex-wrap:wrap;
}

.nav-btn,
.today-btn{
    height:55px;
    border:none;
    border-radius:18px;
    background:white;
    font-size:18px;
    cursor:pointer;
    box-shadow:0 5px 20px rgba(0,0,0,.05);
    transition:.2s;
    padding:0 20px;
    font-weight:600;
    color:#1d275f;
}

.nav-btn{
    width:55px;
    padding:0;
}

.nav-btn:hover,
.today-btn:hover{
    transform:translateY(-3px);
    background:#ff4f8b;
    color:white;
}

.select{
    height:55px;
    border:none;
    border-radius:18px;
    padding:0 18px;
    background:white;
    font-size:16px;
    font-weight:600;
    box-shadow:0 5px 20px rgba(0,0,0,.05);
    outline:none;
    cursor:pointer;
}

/* ================================= */
/* DIAS SEMANA */
/* ================================= */

.weekdays{
    display:grid;
    grid-template-columns:repeat(7,1fr);
    gap:12px;
    margin-bottom:12px;
}

.weekday{
    text-align:center;
    font-weight:700;
    color:#777;
    font-size:15px;
}

/* ================================= */
/* GRID */
/* ================================= */

.calendar-grid{
    display:grid;
    grid-template-columns:repeat(7,1fr);
    gap:12px;
}

/* ================================= */
/* DIA */
/* ================================= */

.day{
    background:white;
    min-height:135px;
    border-radius:22px;
    padding:12px;
    position:relative;
    box-shadow:0 5px 20px rgba(0,0,0,.04);
    transition:.2s;
    overflow:visible;
}

.day:hover{
    transform:translateY(-3px);
}

.day-number{
    font-size:17px;
    font-weight:700;
    color:#1d275f;
    margin-bottom:10px;
}

/* ================================= */
/* EVENTO */
/* ================================= */

.event{
    padding:8px 10px;
    border-radius:14px;
    margin-bottom:8px;
    color:white;
    cursor:pointer;
    position:relative;
    transition:.2s;
}

.event:hover{
    transform:scale(1.02);
}

.pink{
    background:linear-gradient(135deg,#ff4f8b,#ff7eb3);
}

.blue{
    background:linear-gradient(135deg,#3498ff,#5dade2);
}

.green{
    background:linear-gradient(135deg,#22c55e,#54e39f);
}

.yellow{
    background:linear-gradient(135deg,#ffb100,#ffd166);
}

.event-title{
    font-size:13px;
    font-weight:600;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

/* ================================= */
/* TOOLTIP */
/* ================================= */

.tooltip{
    position:absolute;
    bottom:105%;
    left:0;
    width:260px;
    background:white;
    border-radius:18px;
    padding:15px;
    box-shadow:0 10px 35px rgba(0,0,0,.15);
    z-index:9999;
    display:none;
    color:#444;
}

.event:hover .tooltip{
    display:block;
}

.tooltip::after{
    content:"";
    position:absolute;
    bottom:-10px;
    left:25px;
    border-width:10px 10px 0 10px;
    border-style:solid;
    border-color:white transparent transparent transparent;
}

.tooltip h3{
    color:#1d275f;
    margin-bottom:10px;
    font-size:18px;
}

.tooltip p{
    font-size:13px;
    margin-bottom:6px;
}

/* ================================= */
/* VACIO */
/* ================================= */

.empty{
    background:transparent;
    box-shadow:none;
}

/* ================================= */
/* RESPONSIVE */
/* ================================= */

@media(max-width:1200px){

    .calendar-grid{
        grid-template-columns:repeat(4,1fr);
    }

    .weekdays{
        grid-template-columns:repeat(4,1fr);
    }

}

@media(max-width:850px){

    .calendar-grid{
        grid-template-columns:repeat(2,1fr);
    }

    .weekdays{
        display:none;
    }

}

@media(max-width:550px){

    .calendar-grid{
        grid-template-columns:1fr;
    }

    .day{
        min-height:auto;
    }

}

</style>

</head>

<body>

<div class="container">

    <!-- HEADER -->

    <div class="topbar">

        <div class="title">

            <i class="bi bi-calendar-event-fill"></i>

            <h1>
                Calendario
            </h1>

        </div>

        <!-- HOME + CONTROLES -->

        <div class="top-actions">

            <!-- HOME -->

            <a href="/" class="home-btn">

                <i class="bi bi-house-fill"></i>

            </a>

            <div class="controls">

                <!-- IZQUIERDA -->

                <button
                    class="nav-btn"
                    onclick="cambiarMes(-1)"
                >
                    <i class="bi bi-chevron-left"></i>
                </button>

                <!-- MES -->

                <select
                    id="mes"
                    class="select"
                    onchange="irFecha()"
                >

                    {% for numero, nombre in meses.items() %}

                        <option
                            value="{{ numero }}"
                            {% if numero == mes %}selected{% endif %}
                        >
                            {{ nombre }}
                        </option>

                    {% endfor %}

                </select>

                <!-- AÑO -->

                <select
                    id="anio"
                    class="select"
                    onchange="irFecha()"
                >

                    {% for a in range(anio-5, anio+6) %}

                        <option
                            value="{{ a }}"
                            {% if a == anio %}selected{% endif %}
                        >
                            {{ a }}
                        </option>

                    {% endfor %}

                </select>

                <!-- DERECHA -->

                <button
                    class="nav-btn"
                    onclick="cambiarMes(1)"
                >
                    <i class="bi bi-chevron-right"></i>
                </button>

                <!-- HOY -->

                <button
                    class="today-btn"
                    onclick="window.location='/calendario2'"
                >
                    Hoy
                </button>

            </div>

        </div>

    </div>

    <!-- DIAS -->

    <div class="weekdays">

        <div class="weekday">Lunes</div>
        <div class="weekday">Martes</div>
        <div class="weekday">Miércoles</div>
        <div class="weekday">Jueves</div>
        <div class="weekday">Viernes</div>
        <div class="weekday">Sábado</div>
        <div class="weekday">Domingo</div>

    </div>

    <!-- GRID -->

    <div class="calendar-grid">

        {% for celda in calendario %}

            {% if celda == None %}

                <div class="day empty"></div>

            {% else %}

                <div class="day">

                    <div class="day-number">

                        {{ celda.numero }}

                    </div>

                    {% for evento in celda.eventos %}

                        <div class="event

                            {% if evento.tipo_fiesta == 'Cumpleaños' %}
                                pink

                            {% elif evento.tipo_fiesta == 'Baby Shower' %}
                                yellow

                            {% elif evento.tipo_fiesta == 'Bautizo' %}
                                blue

                            {% else %}
                                green
                            {% endif %}
                        ">

                            <div class="event-title">

                                {{ evento.nombre_festejado }}

                            </div>

                            <!-- TOOLTIP -->

                            <div class="tooltip">

                                <h3>
                                    {{ evento.nombre_festejado }}
                                </h3>

                                <p>
                                    🎉 {{ evento.tipo_fiesta }}
                                </p>

                                <p>
                                    📍 {{ evento.salon }}
                                </p>

                                <p>
                                    📞 {{ evento.telefono }}
                                </p>

                                <p>
                                    🎭 {{ evento.paquete }}
                                </p>

                                <p>
                                    🕒 {{ evento.hora_inicio }}
                                </p>

                            </div>

                        </div>

                    {% endfor %}

                </div>

            {% endif %}

        {% endfor %}

    </div>

</div>

<script>

function irFecha(){

    let mes = document.getElementById("mes").value;
    let anio = document.getElementById("anio").value;

    window.location =
        "/calendario2?mes=" + mes + "&anio=" + anio;
}

function cambiarMes(direccion){

    let mes =
        parseInt(
            document.getElementById("mes").value
        );

    let anio =
        parseInt(
            document.getElementById("anio").value
        );

    mes += direccion;

    if(mes < 1){

        mes = 12;
        anio--;

    }

    if(mes > 12){

        mes = 1;
        anio++;

    }

    window.location =
        "/calendario2?mes=" + mes + "&anio=" + anio;
}

</script>

</body>
</html>

"""

# =========================================================
# RUTA
# =========================================================

@calendario_bp.route("/calendario2")
def calendario():

    hoy = datetime.now()

    mes = request.args.get(
        "mes",
        default=hoy.month,
        type=int
    )

    anio = request.args.get(
        "anio",
        default=hoy.year,
        type=int
    )

    # =====================================
    # EVENTOS
    # =====================================

    eventos = Evento.query.filter(
        db.extract('month', Evento.fecha_evento) == mes,
        db.extract('year', Evento.fecha_evento) == anio
    ).all()

    # =====================================
    # CALENDARIO
    # =====================================

    primer_dia_semana, total_dias = calendar.monthrange(
        anio,
        mes
    )

    calendario_dias = []

    # ESPACIOS VACIOS

    for _ in range(primer_dia_semana):

        calendario_dias.append(None)

    # DIAS

    for numero_dia in range(1, total_dias + 1):

        eventos_del_dia = []

        for evento in eventos:

            if evento.fecha_evento.day == numero_dia:

                eventos_del_dia.append(evento)

        calendario_dias.append({

            "numero": numero_dia,
            "eventos": eventos_del_dia

        })

    meses = {

        1:"Enero",
        2:"Febrero",
        3:"Marzo",
        4:"Abril",
        5:"Mayo",
        6:"Junio",
        7:"Julio",
        8:"Agosto",
        9:"Septiembre",
        10:"Octubre",
        11:"Noviembre",
        12:"Diciembre"

    }

    return render_template_string(

        HTML,

        calendario=calendario_dias,

        meses=meses,

        mes=mes,

        anio=anio

    )