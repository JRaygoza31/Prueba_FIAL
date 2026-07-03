from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Evento(db.Model):
    __tablename__="eventos"

    id=db.Column(db.Integer,primary_key=True)

    folio_sistema=db.Column(db.String(20),unique=True,nullable=False)
    folio_cliente=db.Column(db.String(50))

    nombre=db.Column(db.String(150),nullable=False)
    telefono=db.Column(db.String(20),nullable=False)
    telefono_secundario=db.Column(db.String(20))

    fecha_evento=db.Column(db.Date,nullable=False)
    salon=db.Column(db.String(150),nullable=False)
    municipio=db.Column(db.String(100),nullable=False)
    direccion=db.Column(db.String(250),nullable=False)

    horario_show=db.Column(db.String(100),nullable=False)
    total_horas=db.Column(db.String(50),nullable=False)
    horario_evento=db.Column(db.String(50),nullable=False)

    nombre_festejado=db.Column(db.String(150),nullable=False)
    tipo_fiesta=db.Column(db.String(100),nullable=False)

    tematica=db.Column(db.String(150))
    paquete=db.Column(db.String(100),nullable=False)
    descripcion_paquete = db.Column(db.Text)
    numero_personajes=db.Column(db.Integer,default=1)
    personajes = db.Column(db.String(150),nullable=False)
    costo_total=db.Column(db.Float,nullable=False)
    restante=db.Column(db.Float,nullable=False)

    anticipo=db.Column(db.Float,nullable=False)
    fecha_anticipo=db.Column(db.Date)
    imagen_anticipo=db.Column(db.String(300))

    extras=db.Column(db.Text)
    observaciones=db.Column(db.Text)

    fecha_registro=db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
    # CONTRATO

    contrato_generado = db.Column(db.Boolean, default=False,     nullable=False
    )

    fecha_contrato = db.Column(
        db.DateTime
    )

    contrato_enviado = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    

    def __repr__(self):
        return f"<Evento {self.folio_sistema} - {self.nombre_festejado}>"