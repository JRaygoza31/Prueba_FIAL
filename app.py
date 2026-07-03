# app.py
from flask import Flask, render_template_string
from models import db
from models import db, Evento
from formularios import formularios_bp
import calendar
from datetime import datetime, date
from calendario import calendario_bp
from clientes import clientes_bp
from flask import session, request, redirect
from functools import wraps
from contratos import generar_contrato_bp





app = Flask(__name__)
# ---------------------------
# BASE DE DATOS
# ---------------------------

app.secret_key = "juanjose31"




app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql+psycopg2://fial_user:"
    "OeO9PGCdGgPD5Y7jKcVn8uBjqVmSM5EZ@"
    "dpg-d7vn8k5ckfvc73eptgog-a.oregon-postgres.render.com:5432/"
    "fial"
    "?sslmode=require"
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(formularios_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(calendario_bp)
#print(app.url_map)
app.register_blueprint(generar_contrato_bp)


HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fiestas Increíbles</title>

    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

    <style>
        *{margin:0;padding:0;box-sizing:border-box;}

        body{
            background:#f7f7fb;
            font-family:'Poppins', sans-serif;
            overflow-x:hidden;
        }

        .sidebar{
            width:260px;
            height:100vh;
            position:fixed;
            left:0;
            top:0;
            background:white;
            padding:25px 20px;
            border-right:1px solid #eee;
        }

        .logo{
            display:flex;
            justify-content:center;
            align-items:center;
            margin-bottom:10px;
        }

        .logo a{
            display:flex;
            justify-content:center;
            align-items:center;
        }

        .logo img{
            width:180px;
            height:auto;
            object-fit:contain;
            transition:.25s;
            cursor:pointer;
        }

        .logo img:hover{
            transform:scale(1.05);
        }

        .subtitle{
            color:#777;
            font-size:14px;
        }

        .menu{
            margin-top:40px;
        }

        .menu a{
            display:flex;
            align-items:center;
            gap:14px;
            text-decoration:none;
            color:#3b3b55;
            padding:14px 18px;
            border-radius:18px;
            margin-bottom:10px;
            font-weight:500;
            transition:0.3s;
        }

        .menu a:hover{
            background:#ffe5ef;
            color:#ff4f8b;
        }

        .menu a.active{
            background:linear-gradient(135deg,#ff4f8b,#ff6ea8);
            color:white;
            box-shadow:0 10px 20px rgba(255,79,139,0.3);
        }

        .main{
            margin-left:260px;
            padding:30px;
        }

        .topbar{
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:30px;
        }

        .search-box{
            background:white;
            border-radius:18px;
            padding:12px 18px;
            width:350px;
            border:1px solid #eee;
        }

        .search-box input{
            border:none;
            outline:none;
            width:100%;
        }

        .new-btn{
            background:linear-gradient(135deg,#ff4f8b,#ff6ea8);
            border:none;
            color:white;
            padding:14px 22px;
            border-radius:18px;
            font-weight:600;
            box-shadow:0 10px 20px rgba(255,79,139,0.3);
        }

        .welcome h1{
            font-size:34px;
            font-weight:700;
            color:#1d275f;
        }

        .welcome p{
            color:#777;
        }

        .cards{
            display:grid;
            grid-template-columns:repeat(4,1fr);
            gap:20px;
            margin-top:25px;
        }

        .stat-card{
            background:white;
            border-radius:25px;
            padding:25px;
            box-shadow:0 5px 20px rgba(0,0,0,0.04);
        }

        .icon-box{
            width:70px;
            height:70px;
            border-radius:20px;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:30px;
            color:white;
            margin-bottom:18px;
        }

        .pink{background:linear-gradient(135deg,#ff4f8b,#ff79a9);}
        .yellow{background:linear-gradient(135deg,#ffb100,#ffd166);}
        .green{background:linear-gradient(135deg,#22c55e,#54e39f);}
        .purple{background:linear-gradient(135deg,#7c3aed,#9b6bff);}

        .stat-card h2{
            font-size:34px;
            font-weight:700;
            color:#1d275f;
        }

        .stat-card p{
            color:#777;
            margin-bottom:0;
        }

        .content-grid{
            display:grid;
            grid-template-columns:2fr 1fr;
            gap:25px;
            margin-top:25px;
        }

        .calendar-card,
        .side-card{
            background:white;
            border-radius:28px;
            padding:25px;
            box-shadow:0 5px 20px rgba(0,0,0,0.04);
        }

        .calendar-grid{
            display:grid;
            grid-template-columns:repeat(7,1fr);
            gap:10px;
            margin-top:20px;
        }

        .day{
            background:#fafafa;
            height:90px;
            border-radius:16px;
            padding:10px;
            font-size:14px;
            color:#444;
            position:relative;
        }

        .event{
            position:absolute;
            bottom:8px;
            left:8px;
            right:8px;
            padding:5px;
            border-radius:10px;
            font-size:11px;
            font-weight:600;
        }

        .event.pink{
            background:#ffd4e5;
            color:#ff4f8b;
        }

        .events-list{
            margin-top:20px;
        }

        .event-item{
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:14px 0;
            border-bottom:1px solid #f1f1f1;
        }

        .event-left{
            display:flex;
            align-items:center;
            gap:12px;
        }

        .avatar{
            width:52px;
            height:52px;
            border-radius:50%;
            background:linear-gradient(135deg,#ff4f8b,#ffd166);
        }

        .badge-custom{
            padding:8px 14px;
            border-radius:20px;
            font-size:12px;
            font-weight:600;
        }

        .confirmado{
            background:#d8ffe7;
            color:#1ea85f;
        }

        .tasks{
            margin-top:18px;
        }

        .task{
            display:flex;
            align-items:center;
            gap:12px;
            padding:12px 0;
            border-bottom:1px solid #f2f2f2;
        }

        @media(max-width:1200px){
            .cards{grid-template-columns:repeat(2,1fr);}
            .content-grid{grid-template-columns:1fr;}
        }

        @media(max-width:768px){
            body{min-width:1200px;}
            .sidebar{display:block;width:260px;}
            .main{margin-left:260px;}
        }
    </style>
</head>

<body>

<div class="sidebar">

    <div class="logo">
        <a href="https://vercatalogo.com/fial_shows/products/by-all/all" target="_blank">
            <img src="{{ url_for('static', filename='fial_logo.png') }}" alt="Logo">
        </a>
    </div>

    <div class="subtitle">
        Eventos Infantiles
    </div>

    <div class="menu">

        <a href="#" class="active">
            <i class="bi bi-house-fill"></i>
            Inicio
        </a>

        <a href="/calendario2">
            <i class="bi bi-calendar3"></i>
            Calendario
        </a>

        <a href="/clientes">
            <i class="bi bi-people"></i>
            Clientes
        </a>

        <a href="/nuevo_evento">
            <i class="bi bi-file-earmark-text"></i>
            Formularios
        </a>

        <a href="/generar_contrato">
            <i class="bi bi-file-earmark-richtext"></i>
            Contratos
        </a>

        <a href="#">
            <i class="bi bi-bar-chart"></i>
            Estadísticas
        </a>

        <a href="#">
            <i class="bi bi-gear"></i>
            Configuración
        </a>

    </div>

</div>

<div class="main">

    <div class="topbar">

        <div class="welcome">
            <h1>
                ¡Hola, {{nombre_usuario}}! 👋
            </h1>
            <p>Aquí tienes el resumen de tu día.</p>
        </div>

        <div class="d-flex align-items-center gap-3">

            <div class="search-box d-flex align-items-center gap-2">
                <i class="bi bi-search"></i>
                <input type="text" placeholder="Buscar...">
            </div>

            <button class="new-btn">
                + Nueva Reserva
            </button>

        </div>

    </div>

    <!-- CARDS -->

        <div class="cards">

        <div class="stat-card">
            <div class="icon-box pink">
                <i class="bi bi-calendar-event"></i>
            </div>

            <h2>{{ eventos_totales }}</h2>
            <p>Eventos Totales</p>
        </div>

        <div class="stat-card">
            <div class="icon-box green">
                <i class="bi bi-calendar-check"></i>
            </div>

            <h2>{{ eventos_mes }}</h2>
            <p>Eventos del Mes</p>
        </div>

        <div class="stat-card">
            <div class="icon-box yellow">
                <i class="bi bi-calendar-heart"></i>
            </div>

            <h2>{{ cantidad_eventos_hoy }}</h2>
            <p>Eventos para Hoy</p>
        </div>

        <div class="stat-card">
            <div class="icon-box purple">
                <i class="bi bi-file-earmark-richtext"></i>
            </div>

            <h2>{{ contratos_pendientes }}</h2>
            <p>Contratos por Generar</p>
        </div>

    </div>

    <!-- CONTENT -->

    <div class="content-grid">

        <div class="calendar-card">

            <div class="d-flex justify-content-between align-items-center">
                <h3 class="fw-bold">
                    Calendario de Eventos
                </h3>

                <button class="btn btn-light rounded-pill">
                    {{ mes }} {{ anio }}
                </button>
            </div>

            <div class="calendar-grid">

                {% for dia in dias %}

                    <div class="day">

                        {{ dia.numero }}

                        {% for evento in dia.eventos %}

                            <div class="event pink">
                                {{ evento.nombre_festejado }}
                            </div>

                        {% endfor %}

                    </div>

                {% endfor %}

            </div>

        </div>

        <div class="d-flex flex-column gap-4">

            <div class="side-card">

                <h4 class="fw-bold mb-4">
                    Eventos de hoy
                </h4>

                <div class="events-list">

                    {% if eventos_hoy %}

                        {% for evento in eventos_hoy %}

                            <div class="event-item">

                                <div class="event-left">

                                    <div class="avatar"></div>

                                    <div>
                                        <strong>{{ evento.nombre_festejado }}</strong><br>
                                        <small>
                                            {{ evento.horario_show }} · {{ evento.tematica or evento.tipo_fiesta }}
                                        </small>
                                    </div>

                                </div>

                                <span class="badge-custom confirmado">
                                    Hoy
                                </span>

                            </div>

                        {% endfor %}

                    {% else %}

                        <p style="color:#777;">
                            No hay eventos registrados para hoy.
                        </p>

                    {% endif %}

                </div>

            </div>

            <div class="side-card">

                <h4 class="fw-bold mb-3">
                    Tareas Pendientes
                </h4>

                <div class="tasks">

                    {% if tareas_pendientes %}

                        {% for tarea in tareas_pendientes %}

                            <div class="task">
                                <input type="checkbox">
                                <span>{{ tarea }}</span>
                            </div>

                        {% endfor %}

                    {% else %}

                        <div class="task">
                            <span>Todo en orden por ahora ✅</span>
                        </div>

                    {% endif %}

                </div>

            </div>

        </div>

    </div>

</div>

</body>
</html>
"""

from flask import session, redirect


USUARIOS = {
    "jose": {
        "password": "1234",
        "nombre": "José"
    },
    "alex": {
        "password": "5678",
        "nombre": "Alex"
    }
}


##### LOGIN 

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"].lower()
        password = request.form["password"]

        if (
            usuario in USUARIOS
            and
            USUARIOS[usuario]["password"] == password
        ):
            session["logueado"] = True
            session["nombre"] = USUARIOS[usuario]["nombre"]
            return redirect("/")

        error = "Usuario o contraseña incorrectos"

    else:
        error = ""

    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Login FIAL</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    min-height:100vh;
    font-family:'Poppins',sans-serif;
    background:
        linear-gradient(
            rgba(29,39,95,.45),
            rgba(255,79,139,.35)
        ),
        url("{{ url_for('static', filename='fondo_login.jpg') }}");
    background-size:cover;
    background-position:center;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:30px;
}

.login-card{
    width:100%;
    max-width:430px;
    background:rgba(255,255,255,.92);
    backdrop-filter:blur(12px);
    border-radius:32px;
    padding:45px;
    box-shadow:0 20px 50px rgba(0,0,0,.18);
    text-align:center;
}

.logo{
    width:150px;
    margin-bottom:20px;
}

h1{
    color:#1d275f;
    font-size:34px;
    margin-bottom:8px;
}

p{
    color:#777;
    margin-bottom:30px;
}

.input-group{
    text-align:left;
    margin-bottom:18px;
}

label{
    display:block;
    font-weight:600;
    color:#444;
    margin-bottom:8px;
}

input{
    width:100%;
    padding:15px;
    border-radius:16px;
    border:1px solid #ddd;
    font-size:15px;
    outline:none;
}

input:focus{
    border-color:#ff4f8b;
    box-shadow:0 0 0 4px rgba(255,79,139,.15);
}

button{
    width:100%;
    border:none;
    margin-top:10px;
    padding:16px;
    border-radius:18px;
    background:linear-gradient(135deg,#ff4f8b,#ff7eb3);
    color:white;
    font-size:17px;
    font-weight:700;
    cursor:pointer;
    transition:.25s;
}

button:hover{
    transform:translateY(-3px);
    box-shadow:0 10px 25px rgba(255,79,139,.35);
}

.error{
    color:#dc2626;
    font-weight:600;
    margin-bottom:15px;
}

.footer{
    margin-top:25px;
    font-size:13px;
    color:#777;
}
</style>
</head>

<body>

<div class="login-card">

    <img
        src="{{ url_for('static', filename='fial_logo.png') }}"
        class="logo"
    >

    <h1>BIENVENIDO</h1>

    <p></p>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}

    <form method="POST">

        <div class="input-group">
            <label>Usuario</label>
            <input
                name="usuario"
                placeholder=""
                required
            >
        </div>

        <div class="input-group">
            <label>Contraseña</label>
            <input
                name="password"
                type="password"
                placeholder="Tu contraseña"
                required
            >
        </div>

        <button type="submit">
            Entrar
        </button>

    </form>

    <div class="footer">
        Sistema interno de eventos 🎉
    </div>

</div>

</body>
</html>
""", error=error)

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.before_request
def proteger_rutas():

    rutas_publicas = [

        "/login",

        "/nuevo_evento",

        "/formulario/cliente",

        "/formulario/convenio",

        "/terminos"

    ]

    if request.path.startswith("/static/"):
        return

    if request.path in rutas_publicas:
        return

    if not session.get("logueado"):
        return redirect("/login")


@app.route("/")
def home():

    nombre_usuario = session.get(
        "nombre",
        "Invitado"
    )

    hoy = datetime.now()

    anio = hoy.year
    mes = hoy.month

    # =====================================================
    # EVENTOS DEL MES
    # =====================================================

    eventos = Evento.query.filter(
        db.extract("month", Evento.fecha_evento) == mes,
        db.extract("year", Evento.fecha_evento) == anio
    ).all()

    # =====================================================
    # KPIs
    # =====================================================

    eventos_totales = Evento.query.count()

    eventos_mes = len(eventos)

    eventos_hoy = [
        e for e in eventos
        if e.fecha_evento == hoy.date()
    ]

    cantidad_eventos_hoy = len(
        eventos_hoy
    )

    contratos_pendientes = Evento.query.filter_by(
        contrato_generado=False
    ).count()

    # =====================================================
    # TAREAS PENDIENTES
    # =====================================================

    tareas_pendientes = []

    for e in eventos:

        if not e.folio_cliente:

            tareas_pendientes.append(
                f"Asignar folio a {e.nombre_festejado}"
            )

        if e.restante > 0:

            tareas_pendientes.append(
                f"Cobrar restante de {e.nombre_festejado}"
            )

        if not e.imagen_anticipo:

            tareas_pendientes.append(
                f"Subir comprobante de {e.nombre_festejado}"
            )

        if not e.contrato_generado:

            tareas_pendientes.append(
                f"Generar contrato de {e.nombre_festejado}"
            )

    tareas_pendientes = tareas_pendientes[:5]

    # =====================================================
    # CALENDARIO
    # =====================================================

    total_dias = calendar.monthrange(
        anio,
        mes
    )[1]

    dias = []

    for numero_dia in range(
        1,
        total_dias + 1
    ):

        eventos_del_dia = []

        for evento in eventos:

            if evento.fecha_evento.day == numero_dia:

                eventos_del_dia.append(
                    evento
                )

        dias.append({

            "numero": numero_dia,

            "eventos": eventos_del_dia

        })

    # =====================================================
    # RENDER
    # =====================================================

    return render_template_string(

        HTML,

        dias=dias,

        mes=hoy.strftime("%B"),

        anio=anio,

        nombre_usuario=nombre_usuario,

        eventos_totales=eventos_totales,

        eventos_mes=eventos_mes,

        eventos_hoy=eventos_hoy,

        cantidad_eventos_hoy=cantidad_eventos_hoy,

        contratos_pendientes=contratos_pendientes,

        tareas_pendientes=tareas_pendientes

    )

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)