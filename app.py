# app.py
from flask import Flask, render_template_string
from models import db
from models import db, Evento
from formularios import formularios_bp
import calendar
from datetime import datetime
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

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

    <style>

        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
        }

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

        .logo img{
            width:180px;
            height:auto;
            object-fit:contain;
        }
        
        .logo a{
    display:flex;
    justify-content:center;
    align-items:center;
}

.logo img{
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

        .pink{
            background:linear-gradient(135deg,#ff4f8b,#ff79a9);
        }

        .yellow{
            background:linear-gradient(135deg,#ffb100,#ffd166);
        }

        .green{
            background:linear-gradient(135deg,#22c55e,#54e39f);
        }

        .purple{
            background:linear-gradient(135deg,#7c3aed,#9b6bff);
        }

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

        .event.blue{
            background:#d8ebff;
            color:#3498ff;
        }

        .event.green{
            background:#d6ffe8;
            color:#22c55e;
        }

        .event.yellow{
            background:#fff0c9;
            color:#ffb100;
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

        .pendiente{
            background:#fff0c9;
            color:#ff9900;
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

        .bottom-grid{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:25px;
            margin-top:25px;
        }

        .activity-item{
            display:flex;
            justify-content:space-between;
            padding:14px 0;
            border-bottom:1px solid #f2f2f2;
        }

        .chart-bars{
            display:flex;
            align-items:flex-end;
            gap:14px;
            height:220px;
            margin-top:25px;
        }

        .bar-group{
            display:flex;
            gap:6px;
            align-items:flex-end;
        }

        .bar{
            width:18px;
            border-radius:10px 10px 0 0;
        }

        .income{
            background:#22c55e;
        }

        .expense{
            background:#ff4f8b;
        }

        @media(max-width:1200px){

            .cards{
                grid-template-columns:repeat(2,1fr);
            }

            .content-grid{
                grid-template-columns:1fr;
            }

            .bottom-grid{
                grid-template-columns:1fr;
            }
        }

        @media(max-width:768px){

            .sidebar{
                display:none;
            }

            .main{
                margin-left:0;
            }

            .cards{
                grid-template-columns:1fr;
            }
        }

    </style>
</head>
<body>

    <!-- SIDEBAR -->

    <div class="sidebar">

        <div class="logo">

    <a 
        href="https://vercatalogo.com/fial_shows/products/by-all/all"
        target="_blank"
    >

        <img
            src="{{ url_for('static', filename='fial_logo.png') }}"
            alt="Logo"
        >

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

    <!-- MAIN -->

    <div class="main">

        <div class="topbar">

            <div class="welcome">
                <h1>
                    ¡Hola, {{nombre_usuario}}! 👋
                </h1>
                <p>Aquí tienes el resumen de tu negocio.</p>
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

                <h2>18</h2>
                <p>Eventos este mes</p>

            </div>

            <div class="stat-card">

                <div class="icon-box yellow">
                    <i class="bi bi-cash-coin"></i>
                </div>

                <h2>$85,400</h2>
                <p>Ingresos del mes</p>

            </div>

            <div class="stat-card">

                <div class="icon-box green">
                    <i class="bi bi-check-circle"></i>
                </div>

                <h2>32</h2>
                <p>Reservas confirmadas</p>

            </div>

            <div class="stat-card">

                <div class="icon-box purple">
                    <i class="bi bi-clipboard-check"></i>
                </div>

                <h2>6</h2>
                <p>Formularios pendientes</p>

            </div>

        </div>

        <!-- CONTENT -->

        <div class="content-grid">

            <!-- CALENDAR -->

            <div class="calendar-card">

                <div class="d-flex justify-content-between align-items-center">

                    <h3 class="fw-bold">
                        Calendario de Eventos
                    </h3>

                    <button class="btn btn-light rounded-pill">
                        Mayo 2026
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

            </div>

            <!-- SIDE -->

            <div class="d-flex flex-column gap-4">

                <!-- EVENTS -->

                <div class="side-card">

                    <h4 class="fw-bold mb-4">
                        Próximos Eventos
                    </h4>

                    <div class="events-list">

                        <div class="event-item">

                            <div class="event-left">

                                <div class="avatar"></div>

                                <div>
                                    <strong>Cumpleaños Sofía</strong><br>
                                    <small>Sábado 25 Mayo</small>
                                </div>

                            </div>

                            <span class="badge-custom confirmado">
                                Confirmado
                            </span>

                        </div>

                        <div class="event-item">

                            <div class="event-left">

                                <div class="avatar"></div>

                                <div>
                                    <strong>Fiesta Infantil</strong><br>
                                    <small>25 Mayo</small>
                                </div>

                            </div>

                            <span class="badge-custom pendiente">
                                Pendiente
                            </span>

                        </div>

                    </div>

                </div>

                <!-- TASKS -->

                <div class="side-card">

                    <h4 class="fw-bold mb-3">
                        Tareas Pendientes
                    </h4>

                    <div class="tasks">

                        <div class="task">
                            <input type="checkbox">
                            <span>Enviar contrato - Sofía</span>
                        </div>

                        <div class="task">
                            <input type="checkbox">
                            <span>Confirmar pago</span>
                        </div>

                        <div class="task">
                            <input type="checkbox">
                            <span>Preparar decoración</span>
                        </div>

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

            session["nombre"] = (
                USUARIOS[usuario]["nombre"]
            )

            return redirect("/")

        return "Usuario o contraseña incorrectos"

    return """
    <form method="POST">
        <h2>Login</h2>

        <input
            name="usuario"
            placeholder="Usuario"
        >

        <input
            name="password"
            type="password"
            placeholder="Contraseña"
        >

        <button>
            Entrar
        </button>

    </form>
    """


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


    hoy = datetime.now()

    anio = hoy.year
    mes = hoy.month

    eventos = Evento.query.filter(
        db.extract('month', Evento.fecha_evento) == mes,
        db.extract('year', Evento.fecha_evento) == anio
    ).all()


    nombre_usuario = session.get(
        "nombre",
        "Invitado"
    )

    # ==========================
    # GENERAR DIAS DEL MES
    # ==========================

    total_dias = calendar.monthrange(anio, mes)[1]

    dias = []

    for numero_dia in range(1, total_dias + 1):

        eventos_del_dia = []

        for evento in eventos:

            if evento.fecha_evento.day == numero_dia:

                eventos_del_dia.append(evento)

        dias.append({
            "numero": numero_dia,
            "eventos": eventos_del_dia
        })

    return render_template_string(
        HTML,
        dias=dias,
        mes=hoy.strftime("%B"),
        anio=anio,
        nombre_usuario=nombre_usuario
    )

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)