from sqlalchemy import (
    Column, Integer, String, Date, DECIMAL,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship, DeclarativeBase


# ── Base declarativa ───────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ── Representante ──────────────────────────────────────────────────────────────
class Representante(Base):
    __tablename__ = "Representante"

    id_representante = Column(Integer, primary_key=True, autoincrement=True)
    nombres          = Column(String(100), nullable=False)
    apellidos        = Column(String(100), nullable=False)
    cedula           = Column(String(20),  nullable=False, unique=True)
    fecha_nacimiento = Column(Date,        nullable=False)
    direccion        = Column(String(255))
    telefono         = Column(String(20))
    correo           = Column(String(150))

    # Relación inversa: un representante puede tener varios estudiantes
    estudiantes = relationship("Estudiante", back_populates="representante")

    def __repr__(self):
        return f"<Representante {self.apellidos}, {self.nombres} — C.I: {self.cedula}>"


# ── Estudiante ─────────────────────────────────────────────────────────────────
class Estudiante(Base):
    __tablename__ = "Estudiante"

    id_estudiante    = Column(Integer, primary_key=True, autoincrement=True)
    cedula           = Column(String(20),  nullable=False, unique=True)
    nombres          = Column(String(100), nullable=False)
    apellidos        = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date,        nullable=False)
    direccion        = Column(String(255))
    id_representante = Column(Integer, ForeignKey("Representante.id_representante"), nullable=False)

    # Relaciones
    representante = relationship("Representante", back_populates="estudiantes")
    inscripciones = relationship("Inscripcion",   back_populates="estudiante")

    def __repr__(self):
        return f"<Estudiante {self.apellidos}, {self.nombres} — C.I: {self.cedula}>"


# ── Docente ────────────────────────────────────────────────────────────────────
class Docente(Base):
    __tablename__ = "Docente"

    id_docente   = Column(Integer, primary_key=True, autoincrement=True)
    cedula       = Column(String(20),  nullable=False, unique=True)
    nombres      = Column(String(100), nullable=False)
    apellidos    = Column(String(100), nullable=False)
    especialidad = Column(String(150))
    correo       = Column(String(150))
    telefono     = Column(String(20))

    # Relación muchos-a-muchos con Asignatura a través de Asignatura_Docente
    asignaturas = relationship(
        "Asignatura",
        secondary="Asignatura_Docente",
        back_populates="docentes"
    )

    def __repr__(self):
        return f"<Docente {self.apellidos}, {self.nombres}>"


# ── Asignatura ─────────────────────────────────────────────────────────────────
class Asignatura(Base):
    __tablename__ = "Asignatura"

    id_asignatura  = Column(Integer, primary_key=True, autoincrement=True)
    nombre_materia = Column(String(150), nullable=False)

    # Relación muchos-a-muchos con Docente
    docentes = relationship(
        "Docente",
        secondary="Asignatura_Docente",
        back_populates="asignaturas"
    )

    # Relación con calificaciones
    calificaciones = relationship("Calificacion", back_populates="asignatura")

    def __repr__(self):
        return f"<Asignatura {self.nombre_materia}>"


# ── Asignatura_Docente (tabla pivote) ──────────────────────────────────────────
class AsignaturaDocente(Base):
    __tablename__ = "Asignatura_Docente"

    id_docente    = Column(Integer, ForeignKey("Docente.id_docente"),       primary_key=True)
    id_asignatura = Column(Integer, ForeignKey("Asignatura.id_asignatura"), primary_key=True)


# ── Año_Seccion ────────────────────────────────────────────────────────────────
class AñoSeccion(Base):
    __tablename__ = "Año_Seccion"

    id_seccion      = Column(Integer,     primary_key=True, autoincrement=True)
    año             = Column(Integer,     nullable=False)   # 1 al 5 (grado)
    seccion         = Column(String(10),  nullable=False)   # Ej: 'A', 'B'
    periodo_escolar = Column(String(20),  nullable=False)   # Ej: '2025-2026'

    # Restricción: no puede haber dos secciones iguales en el mismo período
    __table_args__ = (
        UniqueConstraint("año", "seccion", "periodo_escolar", name="uq_seccion_periodo"),
    )

    # Relación con inscripciones
    inscripciones = relationship("Inscripcion", back_populates="seccion")

    def __repr__(self):
        return f"<AñoSeccion {self.año}° '{self.seccion}' — {self.periodo_escolar}>"


# ── Inscripcion ────────────────────────────────────────────────────────────────
class Inscripcion(Base):
    __tablename__ = "Inscripcion"

    id_inscripcion = Column(Integer, primary_key=True, autoincrement=True)
    id_estudiante  = Column(Integer, ForeignKey("Estudiante.id_estudiante"), nullable=False)
    id_seccion     = Column(Integer, ForeignKey("Año_Seccion.id_seccion"),   nullable=False)

    # Relaciones
    estudiante     = relationship("Estudiante",  back_populates="inscripciones")
    seccion        = relationship("AñoSeccion",  back_populates="inscripciones")
    asistencias    = relationship("Asistencia",  back_populates="inscripcion")
    calificaciones = relationship("Calificacion", back_populates="inscripcion")

    def __repr__(self):
        return f"<Inscripcion estudiante={self.id_estudiante} seccion={self.id_seccion}>"


# ── Asistencia ─────────────────────────────────────────────────────────────────
class Asistencia(Base):
    __tablename__ = "Asistencia"

    id_asistencia  = Column(Integer, primary_key=True, autoincrement=True)
    id_inscripcion = Column(Integer, ForeignKey("Inscripcion.id_inscripcion"), nullable=False)
    fecha          = Column(Date,       nullable=False)
    estado         = Column(String(20), nullable=False)  # 'Presente', 'Ausente', 'Justificado'

    # Relación
    inscripcion = relationship("Inscripcion", back_populates="asistencias")

    def __repr__(self):
        return f"<Asistencia {self.fecha} — {self.estado}>"


# ── Calificacion ───────────────────────────────────────────────────────────────
class Calificacion(Base):
    __tablename__ = "Calificacion"

    id_nota        = Column(Integer,      primary_key=True, autoincrement=True)
    id_inscripcion = Column(Integer,      ForeignKey("Inscripcion.id_inscripcion"), nullable=False)
    id_asignatura  = Column(Integer,      ForeignKey("Asignatura.id_asignatura"),   nullable=False)
    momento        = Column(String(50),   nullable=False)         # 'Momento 1', 'Momento 2', 'Momento 3'
    puntaje        = Column(DECIMAL(5,2), nullable=False)
    fecha_registro = Column(Date,         nullable=False)
    tipo_de_nota   = Column(String(50),   nullable=False)         # 'Nota_Final', 'Nota_Recuperativa'

    # Relaciones
    inscripcion = relationship("Inscripcion", back_populates="calificaciones")
    asignatura  = relationship("Asignatura",  back_populates="calificaciones")

    def __repr__(self):
        return f"<Calificacion {self.tipo_de_nota} — Momento {self.momento}: {self.puntaje}>"
