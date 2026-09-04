"""
EnglishAI Tutor - Agente IA Profesor de Ingles
Mr. James - 24/7 English teacher for Spanish speakers

Aplicacion Flask con RAG (Pinecone), Supabase, edge-tts y OpenRouter/Gemini.
"""

import os
import io
import asyncio
import base64
import re
import json
import tempfile
import threading
import requests
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import logging
import edge_tts
import google.generativeai as genai
from dotenv import load_dotenv
from database import (
    guardar_estudiante,
    guardar_conversacion,
    guardar_vocabulario,
    guardar_error_estudiante,
    guardar_leccion_completada,
    obtener_estudiante_por_email,
    obtener_progreso_estudiante,
)
from guion import (
    PASOS,
    MODOS,
    obtener_paso,
    formatear_mensaje,
    validar_respuesta,
    obtener_modos,
    obtener_niveles,
    es_modo_valido,
    obtener_info_modo,
    obtener_momento_del_dia,
)

try:
    from rag import search_knowledge, add_text_file, add_pdf, list_documents, delete_document
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "englishai-tutor-secret-change-in-production-2026")

logging.basicConfig(level=logging.INFO)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-2.5-flash")
    GEMINI_CONFIGURED = True
else:
    gemini_model = None
    GEMINI_CONFIGURED = False
    app.logger.warning("GEMINI_API_KEY no configurada")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "xiaomi/mimo-v2.5").strip()
OPENROUTER_CONFIGURED = bool(OPENROUTER_API_KEY)

TTS_VOICE = os.environ.get("TTS_VOICE", "en-US-GuyNeural")


SYSTEM_PROMPT_BASE = """You are Mr. James, a friendly and patient English teacher who specializes in teaching Spanish speakers.

## Your personality
- Warm, encouraging, and patient - like a friend who loves teaching
- You celebrate every small success
- You never make the student feel bad for making mistakes
- You explain things in simple, clear ways
- You use Spanish ONLY when the student seems confused or asks for clarification
- Default language: ENGLISH

## Your teaching style
- Use the Socratic method: guide students to discover answers
- Give examples relevant to Spanish speakers (mention common mistakes)
- Keep explanations SHORT and clear (2-4 sentences max)
- Always provide examples after explaining a rule
- Use encouraging phrases: "Great job!", "Almost!", "Don't worry, this is tricky", "You are doing amazing!"

## Common mistakes Spanish speakers make (always be aware):
- "I have 25 years" -> "I am 25 years old"
- "I am agree" -> "I agree"
- "The party is in my house" -> "The party is AT my house"
- Using present perfect with specific past time (yesterday, last week)
- Translating "tener" directly (use "to be" for age, hunger, etc.)
- Forgetting "the" or "a/an"

## Things you CAN do:
- Teach grammar (all levels A1-C2)
- Practice conversation
- Teach vocabulary with context
- Correct mistakes with kindness
- Explain false cognates (embarazada/pregnant, etc.)
- Help with pronunciation tips

## Things you CANNOT do:
- Complete homework for the student
- Give official certifications
- Judge or criticize harshly
- Use Spanish as the default (only when needed)

## Format of your responses:
- SHORT (2-4 sentences typical)
- Use simple English
- Give examples in English
- If correcting: "Almost! The correct way is..."
- If praising: "Great job!" / "Exactly right!" / "Perfect!"
"""

NIVELES_DESCRIPCION = {
    "A1": "Beginner - basic phrases and introductions",
    "A2": "Elementary - simple daily conversations",
    "B1": "Intermediate - daily situations and opinions",
    "B2": "Upper-Intermediate - fluent conversations",
    "C1": "Advanced - complex topics",
    "C2": "Proficiency - near-native level",
}


async def generate_edge_tts(text, voice=None):
    """Genera audio con edge-tts y retorna base64."""
    if voice is None:
        voice = TTS_VOICE
    communicate = edge_tts.Communicate(text, voice)
    tmp_path = os.path.join(os.path.dirname(__file__), "tmp_audio.mp3")
    await communicate.save(tmp_path)
    with open(tmp_path, "rb") as f:
        audio_data = f.read()
    os.remove(tmp_path)
    return base64.b64encode(audio_data).decode("utf-8")


def get_rag_context(user_message):
    """Busca contexto relevante en Pinecone."""
    if not RAG_AVAILABLE:
        return ""
    try:
        docs = search_knowledge(user_message, n_results=3)
        if not docs:
            return ""
        rag_parts = []
        for d in docs:
            rag_parts.append(f"[Source: {d['source']}]\n{d['text']}")
        return "\n\n## Relevant knowledge base info:\n" + "\n---\n".join(rag_parts)
    except Exception as e:
        app.logger.error(f"RAG error: {e}")
        return ""


def build_student_context(student_data, modo_actual=""):
    """Construye el contexto del estudiante para el LLM."""
    nivel = student_data.get("nivel", "A1")
    nivel_desc = NIVELES_DESCRIPCION.get(nivel, "")
    return f"""
## Current student information
- Name: {student_data.get('nombre', 'Student')}
- Level: {nivel} ({nivel_desc})
- Goal: {student_data.get('objetivo', 'not specified')}
- Current mode: {modo_actual or student_data.get('modo_actual', 'conversation')}
"""


def openrouter_response(user_message, student_data, modo_actual=""):
    """Llama a OpenRouter API."""
    if not OPENROUTER_CONFIGURED:
        return None
    try:
        rag_context = get_rag_context(user_message)
        student_ctx = build_student_context(student_data, modo_actual)
        prompt = f"""{SYSTEM_PROMPT_BASE}{student_ctx}{rag_context}

User said: {user_message}

Respond as Mr. James in a friendly, encouraging way. Keep it short (2-4 sentences typical)."""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://englishai-tutor.com",
            "X-Title": "EnglishAI Tutor - Mr. James",
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 400,
        }
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        app.logger.error(f"OpenRouter error: {e}")
        return None


def gemini_response(user_message, student_data, modo_actual=""):
    """Llama a Gemini API como fallback."""
    if not GEMINI_CONFIGURED or gemini_model is None:
        return None
    try:
        rag_context = get_rag_context(user_message)
        student_ctx = build_student_context(student_data, modo_actual)
        prompt = f"""{SYSTEM_PROMPT_BASE}{student_ctx}{rag_context}

Student said: {user_message}

Respond as Mr. James:"""

        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        app.logger.error(f"Gemini error: {e}")
        return None


def get_llm_response(user_message, student_data, modo_actual=""):
    """Obtiene respuesta del LLM (OpenRouter primero, Gemini fallback)."""
    if OPENROUTER_CONFIGURED:
        result = openrouter_response(user_message, student_data, modo_actual)
        if result:
            return result
    if GEMINI_CONFIGURED:
        result = gemini_response(user_message, student_data, modo_actual)
        if result:
            return result
    return "Sorry, I am having trouble connecting right now. Please try again in a moment."


# ── Gestin de sesin del estudiante ───────────────────────────────────
def get_student_state():
    """Obtiene el estado del estudiante desde la sesin Flask."""
    if "student" not in session:
        session["student"] = {
            "nombre": "",
            "email": "",
            "nivel": "A1",
            "objetivo": "",
            "modo_actual": "",
            "paso_actual": "welcome",
            "registered": False,
        }
    return session["student"]


def save_student_to_db(student_data):
    """Guarda o actualiza el estudiante en Supabase."""
    try:
        ok, _ = guardar_estudiante(student_data)
        return ok
    except Exception as e:
        app.logger.error(f"Error guardando estudiante: {e}")
        return False


# ── Rutas Flask ─────────────────────────────────────────────────────
@app.before_request
def log_config():
    app.logger.info(
        f"Gemini: {GEMINI_CONFIGURED}, OpenRouter: {OPENROUTER_CONFIGURED}, Voice: {TTS_VOICE}"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/speak", methods=["POST"])
def speak_text():
    """Genera audio TTS en ingles."""
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text"}), 400

        audio_content = asyncio.run(generate_edge_tts(text))
        return jsonify({
            "audioContent": audio_content,
            "audioUrl": f"data:audio/mp3;base64,{audio_content}",
            "useBrowserTTS": False,
            "engine": "edge-tts",
        })
    except Exception as e:
        app.logger.error(f"edge-tts error: {e}")
        return jsonify({
            "audioContent": None,
            "audioUrl": None,
            "useBrowserTTS": True,
            "text": text,
            "error": str(e),
        })


@app.route("/api/chat", methods=["POST"])
def chat():
    """Endpoint principal del chat."""
    try:
        data = request.json
        user_message = data.get("message", "").strip()
        action = data.get("action", "")  # Para botones

        student = get_student_state()
        paso_actual = student.get("paso_actual", "welcome")

        app.logger.info(
            f"Chat - paso={paso_actual}, msg={user_message[:50]}, action={action}"
        )

        # Accion init: bienvenida inicial
        if action == 'init':
            student['paso_actual'] = 'welcome'
            session.modified = True
            return jsonify({
                'message': 'Hello! I am Mr. James, your English AI tutor. I am here to help you learn and practice English 24/7. What is your name?',
                'botones': None,
                'paso': 'ask_name',
            })

        # Manejar acciones de botones
        if action:
            return handle_action(action, student)

        # Manejar flujo de pasos
        return handle_step(paso_actual, user_message, student)

    except Exception as e:
        app.logger.error(f"Chat error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def handle_action(action, student):
    """Maneja acciones de botones (level, mode, goal)."""
    paso_actual = student.get("paso_actual", "welcome")

    # Accin: seleccionar nivel
    if action in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        student["nivel"] = action
        student["paso_actual"] = "ask_goal"
        session.modified = True
        paso = obtener_paso("ask_goal")
        msg = formatear_mensaje(paso, student) if paso else ""
        return jsonify({
            "message": msg,
            "botones": paso.get("botones") if paso else None,
            "paso": "ask_goal",
        })

    # Accin: seleccionar objetivo
    objetivos = ["travel", "work", "studies", "exams", "entertainment", "personal"]
    if action in objetivos:
        student["objetivo"] = action
        student["paso_actual"] = "select_mode"
        session.modified = True
        paso = obtener_paso("select_mode")
        msg = formatear_mensaje(paso, student) if paso else ""
        return jsonify({
            "message": msg,
            "botones": paso.get("botones") if paso else None,
            "paso": "select_mode",
        })

    # Accin: ver progreso (debe chequearse ANTES de modo)
    if action == "progress":
        if not student.get("email"):
            return jsonify({
                "message": "To see your progress, please tell me your email first.",
                "botones": None,
                "paso": "ask_email",
            })
        progreso = obtener_progreso_estudiante(student["email"])
        if progreso:
            msg = f"Here is your progress, {student.get('nombre', 'student')}:\n\n"
            msg += f"  Lessons completed: {progreso['lecciones_completadas']}\n"
            msg += f"  Words learned: {progreso['vocabulario_total']}\n"
            msg += f"  Mistakes tracked: {progreso['errores_totales']}\n"
            msg += f"\nKeep up the great work!"
        else:
            msg = "You havent started any lessons yet. Lets practice something!"
        return jsonify({
            "message": msg,
            "botones": [{"texto": "Continue practicing", "valor": "change_mode"}],
            "paso": student.get("paso_actual"),
        })

    # Accin: seleccionar modo
    if es_modo_valido(action) and action != "progress":
        student["modo_actual"] = action
        student["paso_actual"] = "in_session"
        session.modified = True
        # Guardar estudiante en BD al iniciar sesin
        if not student.get("registered") and student.get("email"):
            save_student_to_db(student)
            student["registered"] = True
        info_modo = obtener_info_modo(action)
        nombre_modo = info_modo["nombre"] if info_modo else action.title()
        welcome_msg = f"Great! Lets start {nombre_modo} practice. What would you like to talk about or learn?"
        return jsonify({
            "message": welcome_msg,
            "botones": [
                {"texto": "Change mode", "valor": "change_mode"},
                {"texto": "End session", "valor": "goodbye"},
            ],
            "paso": "in_session",
            "modo": action,
        })

    # Accin: cambiar modo
    if action == "change_mode":
        student["paso_actual"] = "change_mode"
        session.modified = True
        paso = obtener_paso("change_mode")
        return jsonify({
            "message": paso.get("mensaje"),
            "botones": paso.get("botones"),
            "paso": "change_mode",
        })

    # Accin: despedida
    if action == "goodbye":
        student["paso_actual"] = "goodbye"
        session.modified = True
        paso = obtener_paso("goodbye")
        msg = formatear_mensaje(paso, student)
        return jsonify({"message": msg, "botones": None, "paso": "goodbye"})

    # Accin: ver progreso
    if action == "progress":
        if not student.get("email"):
            return jsonify({
                "message": "To see your progress, please register first. Tell me your email.",
                "botones": None,
                "paso": "ask_email",
            })
        progreso = obtener_progreso_estudiante(student["email"])
        if progreso:
            msg = f"Here is your progress, {student.get('nombre', 'student')}:\n\n"
            msg += f"  Lessons completed: {progreso['lecciones_completadas']}\n"
            msg += f"  Words learned: {progreso['vocabulario_total']}\n"
            msg += f"  Mistakes tracked: {progreso['errores_totales']}\n"
            msg += f"\nKeep up the great work!"
        else:
            msg = "You havent started any lessons yet. Lets practice something!"
        return jsonify({
            "message": msg,
            "botones": [{"texto": "Continue practicing", "valor": "change_mode"}],
            "paso": student.get("paso_actual"),
        })

    return jsonify({"message": "Unknown action", "botones": None})


def handle_step(paso_actual, user_message, student):
    """Maneja un paso del flujo conversacional."""
    paso = obtener_paso(paso_actual)

    if not paso:
        # Si no hay paso, reiniciar
        student["paso_actual"] = "welcome"
        session.modified = True
        paso = obtener_paso("welcome")

    # Welcome: pedir nombre
    if paso_actual == "welcome":
        student["paso_actual"] = "ask_name"
        session.modified = True
        return jsonify({
            "message": "Hello! I am Mr. James, your English AI tutor. I am here to help you learn and practice English 24/7. What is your name?",
            "botones": None,
            "paso": "ask_name",
        })

    # Fallback: si no reconoce el paso, tratar como ask_name
    if paso_actual not in ["welcome", "ask_name", "ask_level", "ask_goal", "select_mode", "in_session", "change_mode", "goodbye", "ask_question"]:
        student["paso_actual"] = "ask_name"
        session.modified = True
        paso_actual = "ask_name"

    # Pedir nombre
    if paso_actual == "ask_name":
        ok, nombre = validar_respuesta({"validar": "nombre"}, user_message)
        if not ok:
            return jsonify({
                "message": nombre,  # mensaje de error
                "botones": None,
                "paso": "ask_name",
            })
        student["nombre"] = nombre
        student["paso_actual"] = "ask_level"
        session.modified = True
        paso = obtener_paso("ask_level")
        msg = formatear_mensaje(paso, student)
        return jsonify({
            "message": msg,
            "botones": paso.get("botones"),
            "paso": "ask_level",
        })

    # In session: generar respuesta con LLM
    if paso_actual == "in_session":
        # Llamar al LLM
        response = get_llm_response(
            user_message,
            student,
            student.get("modo_actual", "conversation"),
        )
        # Guardar conversacin en BD
        try:
            if student.get("email"):
                guardar_conversacion({
                    "email": student["email"],
                    "nombre": student.get("nombre", ""),
                    "mensaje_usuario": user_message,
                    "respuesta_agente": response,
                    "modo": student.get("modo_actual", "conversation"),
                    "nivel": student.get("nivel", "A1"),
                })
        except Exception as e:
            app.logger.error(f"Error guardando conversacion: {e}")
        return jsonify({
            "message": response,
            "botones": [
                {"texto": "Change mode", "valor": "change_mode"},
                {"texto": "My progress", "valor": "progress"},
                {"texto": "End session", "valor": "goodbye"},
            ],
            "paso": "in_session",
        })

    # Otros pasos: generar mensaje
    msg = formatear_mensaje(paso, student)
    return jsonify({
        "message": msg,
        "botones": paso.get("botones"),
        "paso": paso_actual,
    })


# ── Endpoints auxiliares ─────────────────────────────────────────────
@app.route("/api/levels", methods=["GET"])
def list_levels():
    return jsonify({"levels": obtener_niveles()})


@app.route("/api/modes", methods=["GET"])
def list_modes_endpoint():
    return jsonify({"modes": obtener_modos()})


@app.route("/api/voices", methods=["GET"])
def list_voices():
    voices = [
        {"id": "en-US-GuyNeural", "name": "Guy", "gender": "Male", "region": "US", "recommended": True},
        {"id": "en-US-JennyNeural", "name": "Jenny", "gender": "Female", "region": "US"},
        {"id": "en-US-DavisNeural", "name": "Davis", "gender": "Male", "region": "US"},
        {"id": "en-US-AriaNeural", "name": "Aria", "gender": "Female", "region": "US"},
        {"id": "en-GB-RyanNeural", "name": "Ryan", "gender": "Male", "region": "UK"},
        {"id": "en-GB-SoniaNeural", "name": "Sonia", "gender": "Female", "region": "UK"},
        {"id": "en-AU-WilliamNeural", "name": "William", "gender": "Male", "region": "Australia"},
    ]
    return jsonify({"voices": voices, "current": TTS_VOICE})


@app.route("/api/reset", methods=["POST"])
def reset_session():
    """Reinicia la sesin del estudiante."""
    session.pop("student", None)
    return jsonify({"message": "Session reset", "ok": True})


@app.route("/api/student", methods=["GET"])
def get_student_info():
    """Retorna la informacin del estudiante actual."""
    student = get_student_state()
    return jsonify({"student": student})


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "EnglishAI Tutor",
        "version": "1.0",
        "rag_available": RAG_AVAILABLE,
        "gemini_configured": GEMINI_CONFIGURED,
        "openrouter_configured": OPENROUTER_CONFIGURED,
    })


@app.route("/api/pinecone-status", methods=["GET"])
def pinecone_status():
    if not RAG_AVAILABLE:
        return jsonify({"error": "RAG not available"}), 500
    try:
        from rag import get_pc, get_index, INDEX_NAME, DIMENSION
        pc = get_pc()
        if pc is None:
            return jsonify({"error": "Pinecone not connected"}), 500
        existing = pc.list_indexes()
        index_names = [idx.name for idx in existing.indexes]
        if INDEX_NAME not in index_names:
            return jsonify({"status": "no_index", "indexes": index_names, "expected": INDEX_NAME})
        idx = pc.Index(INDEX_NAME)
        stats = idx.describe_index_stats()
        return jsonify({
            "status": "ok",
            "index": INDEX_NAME,
            "dimension": DIMENSION,
            "total_vectors": stats.total_vector_count,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Main ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.logger.info("=" * 60)
    app.logger.info("EnglishAI Tutor - Mr. James")
    app.logger.info(f"Voice: {TTS_VOICE}")
    app.logger.info(f"Port: {port}")
    app.logger.info("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=True)
