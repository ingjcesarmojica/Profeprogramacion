"""
Guion Conversacional - Agente IA Profesor de Inglés "Mr. James"
EnglishAI Tutor

Flujo conversacional para clases de inglés.
El estudiante llega, se identifica, evalúa su nivel, elige modo y aprende.
"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo

# Zona horaria por defecto (UTC)
TZ_DEFAULT = ZoneInfo("UTC")

# Niveles CEFR disponibles
NIVELES = ["A1", "A2", "B1", "B2", "C1", "C2"]

# Modos de aprendizaje disponibles
MODOS = {
    "conversation": {
        "id": "conversation",
        "nombre": "Conversation",
        "emoji": "💬",
        "descripcion": "Free talk - practice speaking about any topic",
    },
    "grammar": {
        "id": "grammar",
        "nombre": "Grammar",
        "emoji": "📝",
        "descripcion": "Learn grammar rules and practice with exercises",
    },
    "vocabulary": {
        "id": "vocabulary",
        "nombre": "Vocabulary",
        "emoji": "📚",
        "descripcion": "Learn new words and phrases by topic",
    },
    "quiz": {
        "id": "quiz",
        "nombre": "Quiz",
        "emoji": "🎯",
        "descripcion": "Test your knowledge with interactive questions",
    },
    "pronunciation": {
        "id": "pronunciation",
        "nombre": "Pronunciation",
        "emoji": "🗣️",
        "descripcion": "Practice pronunciation by repeating phrases",
    },
}

# Pasos del flujo conversacional
PASOS = {
    "welcome": {
        "id": "welcome",
        "siguiente": "ask_name",
        "mensaje": "Hello! I'm Mr. James, your English AI tutor. I'm here to help you learn and practice English 24/7. Let's get started! What's your name?",
        "validar": None,
        "botones": None,
        "campo": None,
    },
    "ask_name": {
        "id": "ask_name",
        "siguiente": "ask_level",
        "mensaje": "Nice to meet you, {nombre}! Now, I need to know your English level so I can adapt the class to you. What's your current level? If you're not sure, just pick the one that feels closest.",
        "validar": "nombre",
        "botones": None,
        "campo": "student_name",
    },
    "ask_level": {
        "id": "ask_level",
        "siguiente": "ask_goal",
        "mensaje": "Great, {nombre}! Now, what's your main goal for learning English? This will help me personalize your classes.",
        "validar": "nivel",
        "botones": [
            {"texto": "Travel", "valor": "A1", "descripcion": "Beginner - Basic phrases"},
            {"texto": "A2", "valor": "A2", "descripcion": "Elementary - Simple conversations"},
            {"texto": "B1", "valor": "B1", "descripcion": "Intermediate - Daily situations"},
            {"texto": "B2", "valor": "B2", "descripcion": "Upper-Intermediate - Fluent conversations"},
            {"texto": "C1", "valor": "C1", "descripcion": "Advanced - Complex topics"},
            {"texto": "C2", "valor": "C2", "descripcion": "Proficiency - Near-native level"},
        ],
        "campo": "student_level",
    },
    "ask_goal": {
        "id": "ask_goal",
        "siguiente": "select_mode",
        "mensaje": "Excellent! And what's your main goal?",
        "validar": None,
        "botones": [
            {"texto": "✈️ Travel", "valor": "travel", "descripcion": "Communicate while traveling"},
            {"texto": "💼 Work", "valor": "work", "descripcion": "English for professional contexts"},
            {"texto": "🎓 Studies", "valor": "studies", "descripcion": "Academic English"},
            {"texto": "📝 Exams", "valor": "exams", "descripcion": "Pass a specific exam"},
            {"texto": "🎬 Entertainment", "valor": "entertainment", "descripcion": "Movies, music, books"},
            {"texto": "🌎 Personal", "valor": "personal", "descripcion": "General improvement"},
        ],
        "campo": "student_goal",
    },
    "select_mode": {
        "id": "select_mode",
        "siguiente": "in_session",
        "mensaje": "Perfect! You're all set, {nombre}. What would you like to practice today?",
        "validar": None,
        "botones": [
            {"texto": "💬 Conversation", "valor": "conversation", "descripcion": "Free talk about any topic"},
            {"texto": "📝 Grammar", "valor": "grammar", "descripcion": "Learn and practice grammar"},
            {"texto": "📚 Vocabulary", "valor": "vocabulary", "descripcion": "New words and phrases"},
            {"texto": "🎯 Quiz", "valor": "quiz", "descripcion": "Test your knowledge"},
            {"texto": "🗣️ Pronunciation", "valor": "pronunciation", "descripcion": "Practice pronunciation"},
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
        "mensaje": "Sure! What would you like to practice now?",
        "validar": None,
        "botones": [
            {"texto": "💬 Conversation", "valor": "conversation"},
            {"texto": "📝 Grammar", "valor": "grammar"},
            {"texto": "📚 Vocabulary", "valor": "vocabulary"},
            {"texto": "🎯 Quiz", "valor": "quiz"},
            {"texto": "🗣️ Pronunciation", "valor": "pronunciation"},
            {"texto": "📊 My Progress", "valor": "progress"},
        ],
        "campo": "current_mode",
    },
    "ask_question": {
        "id": "ask_question",
        "siguiente": "in_session",
        "mensaje": "Of course! What would you like to know? You can ask me anything about English: grammar, vocabulary, pronunciation, expressions, etc.",
        "validar": None,
        "botones": None,
        "campo": None,
    },
    "goodbye": {
        "id": "goodbye",
        "siguiente": None,
        "mensaje": "It was a pleasure teaching you today, {nombre}! Remember, practice makes perfect. Come back whenever you want to continue learning. Have a great day!",
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
    """Retorna la parte variable del saludo en inglés."""
    hora = datetime.now(TZ_DEFAULT).hour
    if 5 <= hora < 12:
        return "morning"
    elif 12 <= hora < 18:
        return "afternoon"
    else:
        return "evening"


def validar_nombre(respuesta):
    """Valida el nombre del estudiante."""
    MENSAJE = "I couldn't catch your name clearly. Could you please tell me your name again? Type your first name."
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
    """Valida el nivel CEFR del estudiante (A1-C2)."""
    MENSAJE = "Please choose a level between A1 and C2. If you're not sure, pick A1 if you're starting, B1 if you know some English, or C1 if you're advanced."
    if not respuesta:
        return False, MENSAJE
    respuesta = respuesta.strip().upper()
    match = re.search(r"\b([ABC][12])\b", respuesta)
    if match:
        return True, match.group(1)
    return False, MENSAJE


def validar_modo(respuesta):
    """Valida el modo de aprendizaje elegido."""
    MENSAJE = "Please choose one of the available modes: Conversation, Grammar, Vocabulary, Quiz, or Pronunciation."
    if not respuesta:
        return False, MENSAJE
    respuesta = respuesta.strip().lower()
    modos_validos = ["conversation", "grammar", "vocabulary", "quiz", "pronunciation", "progress"]
    if respuesta in modos_validos:
        return True, respuesta
    mapeo = {
        "gramatica": "grammar",
        "gramática": "grammar",
        "vocabulario": "vocabulary",
        "conversacion": "conversation",
        "conversación": "conversation",
        "pronunciacion": "pronunciation",
        "pronunciación": "pronunciation",
        "cuestionario": "quiz",
        "test": "quiz",
        "examen": "quiz",
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
    """Retorna la lista de niveles CEFR."""
    return NIVELES.copy()


def es_modo_valido(modo):
    """Verifica si un modo es válido."""
    return modo in MODOS or modo == "progress"


def obtener_info_modo(modo_id):
    """Obtiene la información de un modo por su ID."""
    return MODOS.get(modo_id)

