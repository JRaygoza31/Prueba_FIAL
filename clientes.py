from flask import Blueprint, request, render_template_string, redirect, jsonify, Response
from models import db, Evento
import pandas as pd
import io
from datetime import datetime

clientes_bp = Blueprint("clientes", __name__)

# =========================================================
# ACTUALIZAR CAMPO (EDIT EXCEL STYLE)
# =========================================================
@clientes_bp.route("/clientes/editar", methods=["POST"])
def editar_campo():
    data = request.json
    evento = Evento.query.get(data["id"])

    if not evento:
        return jsonify({"ok": False})

    campo = data["campo"]
    valor = data["valor"]

    setattr(evento, campo, valor)
    db.session.commit()

    return jsonify({"ok": True})


# =========================================================
# ELIMINAR
# =========================================================
@clientes_bp.route("/clientes/eliminar/<int:id>")
def eliminar(id):
    evento = Evento.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return redirect("/clientes")


# =========================================================
# EXPORTAR EXCEL
# =========================================================
@clientes_bp.route("/clientes/exportar")
def exportar():
    eventos = Evento.query.all()
    data = [e.__dict__ for e in eventos]

    for d in data:
        d.pop("_sa_instance_state", None)

    df = pd.DataFrame(data)
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    output.seek(0)

    return Response(
        output,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=eventos.xlsx"}
    )


# =========================================================
# LISTADO PRINCIPAL CON FILTROS DINÁMICOS
# =========================================================
@clientes_bp.route("/clientes")
def clientes():
    # 1. Obtener parámetros de búsqueda desde la URL (GET)
    tipo_evento = request.args.get("tipo_evento", "")
    desde = request.args.get("desde", "")
    hasta = request.args.get("hasta", "")
    buscar = request.args.get("buscar", "")
    ordenar_por = request.args.get("ordenar_por", "fecha_evento")

    # 2. Construir la Query Base
    query = Evento.query

    # Filtro: Tipo de evento
    if tipo_evento and tipo_evento != "Todos":
        query = query.filter(Evento.tipo_fiesta == tipo_evento)

    # Filtro: Rango de fechas (Desde / Hasta)
    if desde:
        query = query.filter(Evento.fecha_evento >= desde)
    if hasta:
        query = query.filter(Evento.fecha_evento <= hasta)

    # Filtro: Barra de búsqueda (Cliente / Salón / Dirección / Folio)
    if buscar:
        search_filter = (
            Evento.nombre.ilike(f"%{buscar}%") |
            Evento.salon.ilike(f"%{buscar}%") |
            Evento.direccion.ilike(f"%{buscar}%") |
            Evento.folio_sistema.ilike(f"%{buscar}%") |
            Evento.folio_cliente.ilike(f"%{buscar}%")
        )
        query = query.filter(search_filter)

    # =====================================
# ORDENAMIENTO
# =====================================

    if ordenar_por == "fecha_evento":

        query = query.order_by(
            Evento.fecha_evento.asc()
        )

    elif ordenar_por == "fecha_registro":

        query = query.order_by(
            Evento.fecha_registro.desc()
        )

    else:

        # Más recientes creados primero
        query = query.order_by(
            Evento.id.desc()
        )

    # Ejecutar consulta
    eventos = query.all()

    # 3. Obtener lista de tipos de eventos únicos para llenar el select dinámicamente
    # Esto evita tener que escribir los tipos de fiesta a mano
    tipos_disponibles = [t[0] for t in db.session.query(Evento.tipo_fiesta).distinct().all() if t[0]]

    # 4. Construir las filas de la tabla HTML
    filas = ""
    for e in eventos:
                filas += f"""
        <tr>
            <td>{e.id}</td>
            <td contenteditable onblur="guardar(this,{e.id},'folio_sistema')">{e.folio_sistema or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'folio_cliente')">{e.folio_cliente or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'nombre')">{e.nombre or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'telefono')">{e.telefono or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'telefono_secundario')">{e.telefono_secundario or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'fecha_evento')">{e.fecha_evento or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'salon')">{e.salon or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'municipio')">{e.municipio or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'direccion')">{e.direccion or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'horario_show')">{e.horario_show or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'total_horas')">{e.total_horas or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'horario_evento')">{e.horario_evento or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'nombre_festejado')">{e.nombre_festejado or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'tipo_fiesta')">{e.tipo_fiesta or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'tematica')">{e.tematica or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'numero_personajes')">{e.numero_personajes or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'personajes')">{e.personajes or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'paquete')">{e.paquete or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'costo_total')">{e.costo_total or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'anticipo')">{e.anticipo or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'restante')">{e.restante or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'fecha_anticipo')">{e.fecha_anticipo or ''}</td>
            <td>
                {f'<a href="/{e.imagen_anticipo}" target="_blank">Ver comprobante</a>' if e.imagen_anticipo else ''}
            </td>
            <td contenteditable onblur="guardar(this,{e.id},'extras')">{e.extras or ''}</td>
            <td contenteditable onblur="guardar(this,{e.id},'observaciones')">{e.observaciones or ''}</td>
            <td>{e.fecha_registro.strftime("%d/%m/%Y %H:%M") if e.fecha_registro else ""}</td>
            
            <td>
                <a href="/clientes/eliminar/{e.id}"
                   onclick="return confirm('¿Eliminar este evento?')"
                   style="color:white;background:red;padding:6px 10px;border-radius:8px;text-decoration:none;">
                    🗑
                </a>
            </td>
        </tr>
        """

    # Generar opciones del selector de tipo de evento manteniendo el seleccionado
    opciones_tipo = f'<option value="Todos" {"selected" if tipo_evento == "Todos" else ""}>Todos</option>'
    for t in tipos_disponibles:
        seleccionado = "selected" if tipo_evento == t else ""
        opciones_tipo += f'<option value="{t}" {seleccionado}>{t}</option>'

    return render_template_string(f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Eventos PRO</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background:#f5f7fb;
    padding:20px;
    margin: 0;
}}
.header {{
    display:flex;
    justify-content:space-between;
    align-items: center;
    margin-bottom:20px;
}}
.actions a {{
    margin-left:10px;
}}

/* BARRA DE FILTROS ESTILO IMAGEN */
.filter-bar {{
    background: #eef2f7;
    padding: 15px 20px;
    border-radius: 12px;
    display: flex;
    gap: 15px;
    align-items: flex-end;
    margin-bottom: 25px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}}
.filter-group {{
    display: flex;
    flex-direction: column;
    gap: 5px;
    flex-grow: 1;
}}
.filter-group label {{
    font-size: 13px;
    font-weight: bold;
    color: #333;
}}
.filter-group input, .filter-group select {{
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-size: 14px;
    background: white;
    box-sizing: border-box;
    height: 40px;
}}
.filter-group input::placeholder {{
    color: #aaa;
}}
.btn-filtrar {{
    background: #2563eb;
    color: white;
    border: none;
    padding: 0 30px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    height: 40px;
    transition: background 0.2s;
}}
.btn-filtrar:hover {{
    background: #1d4ed8;
}}

/* TABLA */
.table-container {{
    overflow-x: auto;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}}
table {{
    width:100%;
    border-collapse:collapse;
    font-size:12px;
}}
th {{
    background:#1d275f;
    color:white;
    padding:12px 10px;
    position:sticky;
    top:0;
    text-align: left;
}}
td {{
    border:1px solid #eee;
    padding:8px;
    min-width:120px;
}}
td[contenteditable="true"] {{
    background:#fffdf5;
}}
</style>
</head>
<body>

<div class="header">
    <h2>📋 BASE DE DATOS - EVENTOS -</h2>
    <div class="actions">
        <a href="/" style="padding:8px;background:#6366f1;color:white;border-radius:8px;text-decoration:none;">⬅️ Inicio</a>
        <a href="/generar_contrato" style="padding:8px;background:#2563eb;color:white;border-radius:8px;text-decoration:none;">📝 Contrato</a>
        <a href="/clientes/exportar" style="padding:8px;background:#059669;color:white;border-radius:8px;text-decoration:none;">📥 Exportar</a>
    </div>
</div>

<form method="GET" action="/clientes" class="filter-bar">
    <div class="filter-group" style="flex-grow: 1.5;">
        <label>Tipo de evento</label>
        <select name="tipo_evento">
            {opciones_tipo}
        </select>
    </div>

    <div class="filter-group">
        <label>Desde</label>
        <input type="date" name="desde" value="{desde}">
    </div>

    <div class="filter-group">
        <label>Hasta</label>
        <input type="date" name="hasta" value="{hasta}">
    </div>

    <div class="filter-group" style="flex-grow: 2.5;">
        <label>Buscar</label>
        <input type="text" name="buscar" placeholder="Cliente / Salón / Dirección / Folio" value="{buscar}">
    </div>

    <div class="filter-group" style="flex-grow: 1.5;">
        <label>Ordenar por</label>
        <select name="ordenar_por">

            <option
                value="id"
                {"selected" if ordenar_por=="id" else ""}
            >
                Más recientes
            </option>

            <option
                value="fecha_evento"
                {"selected" if ordenar_por=="fecha_evento" else ""}
            >
                Fecha del evento
            </option>

            <option
                value="fecha_registro"
                {"selected" if ordenar_por=="fecha_registro" else ""}
            >
                Fecha de registro
            </option>

        </select>
    </div>

    <button type="submit" class="btn-filtrar">Filtrar</button>
</form>

<div class="table-container">
    <table>
    <thead>
    <tr>
        <th>ID</th>

        <th>Folio Sistema</th>
        <th>Folio Cliente</th>

        <th>Nombre</th>
        <th>Teléfono</th>
        <th>Teléfono Secundario</th>

        <th>Fecha Evento</th>
        <th>Salón</th>
        <th>Municipio</th>
        <th>Dirección</th>

        <th>Horario Show</th>
        <th>Total Horas</th>
        <th>Horario Evento</th>

        <th>Nombre Festejado</th>
        <th>Tipo Fiesta</th>

        <th>Temática</th>

        <th>Número Personajes</th>
        <th>Personajes</th>

        <th>Paquete</th>

        <th>Costo Total</th>
        <th>Anticipo</th>
        <th>Restante</th>

        <th>Fecha Anticipo</th>
        <th>Imagen Anticipo</th>

        <th>Extras</th>
        <th>Observaciones</th>

        <th>Fecha Registro</th>

        <th>Acción</th>
    </tr>
    </thead>
    <tbody>
    {filas}
    </tbody>
    </table>
</div>

<script>
function guardar(el, id, campo) {{
    fetch("/clientes/editar", {{
        method: "POST",
        headers: {{
            "Content-Type": "application/json"
        }},
        body: JSON.stringify({{
            id: id,
            campo: campo,
            valor: el.innerText.trim()
        }})
    }});
}}
</script>

</body>
</html>
""")