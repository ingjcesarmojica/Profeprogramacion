"""
Guion Conversacional - Agente IA Profesor de Programación "Profesor Byte"
CodeAI Tutor

Flujo conversacional para clases de programación en español.
El estudiante llega, se identifica, evalúa su nivel, elige modo y aprende.
7 niveles: Inicio, Novato, Aprendiz, Técnico, Tecnólogo, Ingeniero, Ingeniero de IA.
"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo

# Zona horaria por defecto (UTC)
TZ_DEFAULT = ZoneInfo("UTC")

# Niveles de programación disponibles (del más básico al más avanzado)
NIVELES = [
    "INICIO",
    "NOVATO",
    "APRENDIZ",
    "TECNICO",
    "TECNOLOGO",
    "INGENIERO",
    "INGENIERO_IA",
]

# Descripción de cada nivel
NIVELES_DESCRIPCION = {
    "INICIO":      "Inicio - sin experiencia previa, primeros pasos en programación",
    "NOVATO":      "Novato - conceptos básicos y primer lenguaje",
    "APRENDIZ":    "Aprendiz - estructuras de control, funciones y POO inicial",
    "TECNICO":     "Técnico - frameworks, bases de datos y desarrollo web/móvil",
    "TECNOLOGO":   "Tecnólogo - arquitectura de software, APIs y despliegue",
    "INGENIERO":   "Ingeniero - sistemas distribuidos, DevOps y buenas prácticas",
    "INGENIERO_IA":"Ingeniero de IA - machine learning, deep learning y MLOps",
}

# Modos de aprendizaje disponibles (en español)
MODOS = {
    "conceptos": {
        "id": "conceptos",
        "nombre": "Conceptos",
        "emoji": "💡",
        "descripcion": "Aprende los conceptos teóricos de programación con ejemplos",
    },
    "practica": {
        "id": "practica",
        "nombre": "Práctica",
        "emoji": "⌨️",
        "descripcion": "Resuelve ejercicios y retos de programación paso a paso",
    },
    "proyectos": {
        "id": "proyectos",
        "nombre": "Proyectos",
        "emoji": "🚀",
        "descripcion": "Construye proyectos reales guiados por el profesor",
    },
    "quiz": {
        "id": "quiz",
        "nombre": "Quiz",
        "emoji": "🎯",
        "descripcion": "Pon a prueba tus conocimientos con preguntas interactivas",
    },
    "codigo": {
        "id": "codigo",
        "nombre": "Código",
        "emoji": "🧩",
        "descripcion": "Te ayudo a entender, depurar y mejorar tu código",
    },
    "ia": {
        "id": "ia",
        "nombre": "IA",
        "emoji": "🤖",
        "descripcion": "Aprende sobre inteligencia artificial, machine learning y deep learning",
    },
}

# Pasos del flujo conversacional
PASOS = {
    "welcome": {
        "id": "welcome",
        "siguiente": "ask_name",
        "mensaje": "¡Hola! Soy el Profesor Byte, tu tutor de programación con IA. Estoy aquí para enseñarte a programar las 24 horas, los 7 días de la semana, desde cero hasta Ingeniería de IA. ¡Empecemos! ¿Cómo te llamas?",
        "validar": None,
        "botones": None,
        "campo": None,
    },
    "ask_name": {
        "id": "ask_name",
        "siguiente": "ask_level",
        "mensaje": "¡Mucho gusto, {nombre}! Para adaptar las clases a ti, necesito saber tu nivel actual de programación. ¿En qué nivel te encuentras? Si no estás seguro, elige el que más se parezca a ti.",
        "validar": "nombre",
        "botones": None,
        "campo": "student_name",
    },
    "ask_level": {
        "id": "ask_level",
        "siguiente": "ask_goal",
        "mensaje": "¡Perfecto, {nombre}! Selecciona tu nivel de programación:",
        "validar": "nivel",
        "botones": [
            {"texto": "🌱 Inicio",        "valor": "INICIO",       "descripcion": "Sin experiencia previa, primer contacto"},
            {"texto": "🐣 Novato",        "valor": "NOVATO",       "descripcion": "Conceptos básicos y primer lenguaje"},
            {"texto": "📚 Aprendiz",      "valor": "APRENDIZ",     "descripcion": "Estructuras de control, funciones y POO"},
            {"texto": "🛠️ Técnico",       "valor": "TECNICO",      "descripcion": "Frameworks, bases de datos y desarrollo web/móvil"},
            {"texto": "🎓 Tecnólogo",     "valor": "TECNOLOGO",    "descripcion": "Arquitectura de software, APIs y despliegue"},
            {"texto": "🏗️ Ingeniero",     "valor": "INGENIERO",    "descripcion": "Sistemas distribuidos, DevOps y buenas prácticas"},
            {"texto": "🤖 Ingeniero IA",  "valor": "INGENIERO_IA", "descripcion": "Machine learning, deep learning y MLOps"},
        ],
        "campo": "student_level",
    },
    "ask_goal": {
        "id": "ask_goal",
        "siguiente": "select_mode",
        "mensaje": "¡Excelente! ¿Cuál es tu objetivo principal al aprender a programar? Esto me ayudará a personalizar tu aprendizaje.",
        "validar": None,
        "botones": [
            {"texto": "💼 Trabajar como desarrollador", "valor": "trabajo",        "descripcion": "Conseguir empleo en tecnología"},
            {"texto": "🎓 Estudios / Universidad",       "valor": "estudios",       "descripcion": "Reforzar lo aprendido en la carrera"},
            {"texto": "🚀 Crear mi propio proyecto",     "valor": "emprendimiento", "descripcion": "Construir una startup o producto"},
            {"texto": "🤖 Aprender Inteligencia Artificial", "valor": "ia",         "descripcion": "Machine learning, deep learning, LLMs"},
            {"texto": "🌐 Desarrollo web",               "valor": "web",            "descripcion": "Frontend, backend o full stack"},
            {"texto": "🎮 Crear videojuegos",            "valor": "videojuegos",    "descripcion": "Desarrollo de juegos con Unity, Godot, etc."},
            {"texto": "📊 Análisis de datos",            "valor": "datos",          "descripcion": "Ciencia de datos y visualización"},
            {"texto": "🧑‍💻 Curiosidad / Hobby",          "valor": "hobby",          "descripcion": "Aprender por diversión y crecimiento personal"},
        ],
        "campo": "student_goal",
    },
    "select_mode": {
        "id": "select_mode",
        "siguiente": "in_session",
        "mensaje": "¡Todo listo, {nombre}! ¿Qué te gustaría practicar hoy?",
        "validar": None,
        "botones": [
            {"texto": "💡 Conceptos",  "valor": "conceptos",  "descripcion": "Teoría con ejemplos claros"},
            {"texto": "⌨️ Práctica",   "valor": "practica",   "descripcion": "Ejercicios paso a paso"},
            {"texto": "🚀 Proyectos",  "valor": "proyectos",  "descripcion": "Proyectos guiados reales"},
            {"texto": "🎯 Quiz",       "valor": "quiz",       "descripcion": "Preguntas para evaluar tu nivel"},
            {"texto": "🧩 Código",     "valor": "codigo",     "descripcion": "Reviso, explico y depuro tu código"},
            {"texto": "🤖 IA",         "valor": "ia",         "descripcion": "Aprende sobre inteligencia artificial"},
        ],
        "campo": "current_mode",
    },
    "in_session": {
        "id": "in_session",
        "siguiente": "in_session",
        "mensaje": None,
        "validar": None,
        "botones": None,
        "campo": None,
    },
    "change_mode": {
        "id": "change_mode",
        "siguiente": "in_session",
        "mensaje": "¡Claro! ¿Qué quieres practicar ahora?",
        "validar": None,
        "botones": [
            {"texto": "💡 Conceptos",  "valor": "conceptos"},
            {"texto": "⌨️ Práctica",   "valor": "practica"},
            {"texto": "🚀 Proyectos",  "valor": "proyectos"},
            {"texto": "🎯 Quiz",       "valor": "quiz"},
            {"texto": "🧩 Código",     "valor": "codigo"},
            {"texto": "🤖 IA",         "valor": "ia"},
            {"texto": "📊 Mi progreso","valor": "progress"},
        ],
        "campo": "current_mode",
    },
    "ask_question": {
        "id": "ask_question",
        "siguiente": "in_session",
        "mensaje": "¡Por supuesto! Pregúntame lo que quieras sobre programación: algoritmos, lenguajes, frameworks, buenas prácticas, IA, etc.",
        "validar": None,
        "botones": None,
        "campo": None,
    },
    "goodbye": {
        "id": "goodbye",
        "siguiente": None,
        "mensaje": "¡Fue un placer enseñarte hoy, {nombre}! Recuerda: en programación, la práctica constante hace al maestro. Vuelve cuando quieras seguir aprendiendo. ¡Mucho éxito en tu camino como desarrollador! 👨‍💻",
        "validar": None,
        "botones": None,
        "campo": None,
    },
}


def obtener_paso(paso_id):
    """Obtiene un paso del guion por su ID."""
    return PASOS.get(paso_id)


def formatear_mensaje(paso, datos):
    """Formatea el mensaje del paso con los datos del estudiante."""
    mensaje = paso.get("mensaje", "")
    if mensaje is None:
        return ""
    try:
        return mensaje.format(**datos)
    except KeyError:
        return mensaje


def obtener_momento_del_dia():
    """Retorna la parte variable del saludo en español."""
    hora = datetime.now(TZ_DEFAULT).hour
    if 5 <= hora < 12:
        return "Buenos días"
    elif 12 <= hora < 19:
        return "Buenas tardes"
    else:
        return "Buenas noches"


def validar_nombre(respuesta):
    """Valida el nombre del estudiante."""
    MENSAJE = "No pude leer bien tu nombre. ¿Podrías decírmelo de nuevo? Escribe tu nombre."
    if not respuesta:
        return False, MENSAJE
    respuesta = respuesta.strip()
    respuesta = re.sub(r"[^\wáéíóúñüÁÉÍÓÚÑÜ\s]", "", respuesta).strip()
    if len(respuesta) < 2:
        return False, MENSAJE
    if not re.search(r"[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ]", respuesta):
        return False, MENSAJE
    if respuesta.replace(" ", "").isdigit():
        return False, MENSAJE
    nombre_limpio = " ".join(p.capitalize() for p in respuesta.split())
    return True, nombre_limpio


def validar_nivel(respuesta):
    """Valida el nivel de programación del estudiante."""
    MENSAJE = (
        "Por favor, elige un nivel válido: Inicio, Novato, Aprendiz, Técnico, "
        "Tecnólogo, Ingeniero o Ingeniero de IA. Si estás empezando, elige Inicio."
    )
    if not respuesta:
        return False, MENSAJE
    respuesta_limpia = respuesta.strip()
    # Quitar acentos para tolerar variantes
    sin_acentos = (
        respuesta_limpia.upper()
        .replace("Á", "A").replace("É", "E").replace("Í", "I")
        .replace("Ó", "O").replace("Ú", "U")
    )
    # Coincidencia exacta (case-insensitive)
    for nivel in NIVELES:
        if sin_acentos == nivel:
            return True, nivel
    # Tolerar "Ingeniero IA" -> "INGENIERO_IA" (espacio o guion)
    sin_acentos_normalizado = sin_acentos.replace(" ", "_").replace("-", "_")
    for nivel in NIVELES:
        if sin_acentos_normalizado == nivel:
            return True, nivel
    # Variantes comunes en español
    alias = {
        "PRINCIPIANTE": "INICIO",
        "BEGINNER": "INICIO",
        "BASICO": "NOVATO",
        "BÁSICO": "NOVATO",
        "INTERMEDIO": "APRENDIZ",
        "AVANZADO": "INGENIERO",
        "IA": "INGENIERO_IA",
        "INTELIGENCIA_ARTIFICIAL": "INGENIERO_IA",
        "INTELIGENCIA ARTIFICIAL": "INGENIERO_IA",
        "MACHINE_LEARNING": "INGENIERO_IA",
        "MACHINE LEARNING": "INGENIERO_IA",
        "ML": "INGENIERO_IA",
        "DEEP_LEARNING": "INGENIERO_IA",
        "DEEP LEARNING": "INGENIERO_IA",
        "TECNICO": "TECNICO",
        "TECNOLOGO": "TECNOLOGO",
    }
    if sin_acentos_normalizado in alias:
        return True, alias[sin_acentos_normalizado]
    if sin_acentos in alias:
        return True, alias[sin_acentos]
    return False, MENSAJE


def validar_modo(respuesta):
    """Valida el modo de aprendizaje elegido."""
    MENSAJE = (
        "Por favor, elige uno de los modos disponibles: Conceptos, Práctica, "
        "Proyectos, Quiz, Código o IA."
    )
    if not respuesta:
        return False, MENSAJE
    respuesta = respuesta.strip().lower()
    modos_validos = ["conceptos", "practica", "proyectos", "quiz", "codigo", "ia", "progress"]
    if respuesta in modos_validos:
        return True, respuesta
    # Alias en español y abreviaturas
    mapeo = {
        "concepto": "conceptos",
        "teoria": "conceptos",
        "teoría": "conceptos",
        "practicas": "practica",
        "prácticas": "practica",
        "ejercicio": "practica",
        "ejercicios": "practica",
        "proyecto": "proyectos",
        "cuestionario": "quiz",
        "test": "quiz",
        "examen": "quiz",
        "codigos": "codigo",
        "códigos": "codigo",
        "programacion": "codigo",
        "programación": "codigo",
        "inteligencia artificial": "ia",
        "machine learning": "ia",
        "deep learning": "ia",
        "progreso": "progress",
        "avance": "progress",
    }
    if respuesta in mapeo:
        return True, mapeo[respuesta]
    return False, MENSAJE


def validar_respuesta(paso, respuesta):
    """Valida la respuesta del estudiante según el tipo de campo."""
    tipo = paso.get("validar")
    if tipo is None:
        return True, respuesta
    if tipo == "nombre":
        return validar_nombre(respuesta)
    if tipo == "nivel":
        return validar_nivel(respuesta)
    if tipo == "modo":
        return validar_modo(respuesta)
    return True, respuesta


def obtener_modos():
    """Retorna la lista de modos disponibles."""
    return list(MODOS.values())


def obtener_niveles():
    """Retorna la lista de niveles de programación."""
    return NIVELES.copy()


def es_modo_valido(modo):
    """Verifica si un modo es válido."""
    return modo in MODOS or modo == "progress"


def obtener_info_modo(modo_id):
    """Obtiene la información de un modo por su ID."""
    return MODOS.get(modo_id)


def descripcion_nivel(nivel):
    """Retorna la descripción legible de un nivel."""
    return NIVELES_DESCRIPCION.get(nivel, "")

