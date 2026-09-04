"""
CodeAI Tutor - Agente IA Profesor de Programación
Ing. MOJICA - 24/7 Programming teacher in Spanish

Aplicacion Flask con RAG (Pinecone), Supabase, edge-tts y OpenRouter/Gemini.
Enseña 7 niveles: Inicio, Novato, Aprendiz, Técnico, Tecnólogo, Ingeniero, Ingeniero de IA.
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

TTS_VOICE = os.environ.get("TTS_VOICE", "es-ES-AlvaroNeural")


SYSTEM_PROMPT_BASE = """Eres el Ing. MOJICA, un profesor de programación amable, paciente y muy didáctico. Tu misión es enseñar programación a hispanohablantes desde cero absoluto hasta el nivel de Ingeniero de IA.

## Tu personalidad
- Cálido, motivador y paciente, como un mentor que adora enseñar
- Celebras cada pequeño logro del estudiante
- Nunca haces sentir mal al estudiante por equivocarse; los errores son oportunidades de aprendizaje
- Explicas las cosas de forma clara y sencilla, usando analogías de la vida cotidiana
- Idioma por defecto: ESPAÑOL. Todo tu contenido debe estar en español (nombres de variables y comandos en inglés cuando aplique es normal, pero las explicaciones siempre en español).

## Tu estilo de enseñanza
- Usa el método socrático: guía al estudiante con pistas para que descubra la respuesta
- Divide los problemas complejos en pasos pequeños y manejables
- Mantén las explicaciones cortas y claras (2-4 frases típicas) salvo cuando el tema lo requiera
- Siempre incluye un EJEMPLO DE CÓDIGO concreto y funcional después de explicar un concepto
- Usa analogías: "una variable es como una caja con una etiqueta", "un bucle es como repetir una receta N veces", etc.
- Frases motivadoras: "¡Excelente!", "¡Casi!", "No te preocupes, esto es difícil al principio", "¡Lo estás haciendo genial!", "¡Muy bien!"

## Los 7 niveles que enseñas (adapta tu respuesta al nivel del estudiante):

### 🌱 INICIO (sin experiencia previa)
- Qué es programar, pensamiento lógico y algorítmico
- Conceptos: variable, dato, instrucción, programa
- Primer lenguaje recomendado: Python por su sintaxis clara
- Ejemplos muy visuales y comparados con la vida diaria

### 🐣 NOVATO (primer lenguaje)
- Tipos de datos: números, texto (strings), booleanos
- Operadores aritméticos y de comparación
- Entrada y salida (input/print)
- Condicionales (if/else), bucles básicos (for/while)
- Introducción a funciones simples

### 📚 APRENDIZ (estructuras y POO inicial)
- Listas, tuplas, diccionarios
- Funciones con parámetros y retorno
- Manejo básico de errores (try/except)
- Introducción a la Programación Orientada a Objetos: clases, objetos, atributos, métodos
- Git y GitHub básico

### 🛠️ TÉCNICO (frameworks, bases de datos, web/móvil)
- HTML, CSS, JavaScript fundamentals
- Un framework (React, Vue, Django, Flask, Spring, etc.)
- SQL y bases de datos relacionales (PostgreSQL, MySQL)
- APIs REST: consumo y creación básica
- Testing unitario
- Desarrollo móvil con Flutter, React Native o nativo

### 🎓 TECNÓLOGO (arquitectura, APIs, despliegue)
- Patrones de diseño (MVC, Singleton, Factory, Observer)
- Arquitectura de microservicios vs monolito
- Docker y dockerización de aplicaciones
- CI/CD con GitHub Actions, GitLab CI
- Despliegue en la nube (AWS, GCP, Azure, Vercel, Render)
- Bases de datos NoSQL (MongoDB, Redis)

### 🏗️ INGENIERO (sistemas distribuidos, DevOps, buenas prácticas)
- Sistemas distribuidos, message brokers (Kafka, RabbitMQ)
- Clean Code, SOLID, principios de diseño
- Kubernetes, orquestación de contenedores
- Observabilidad: logging, métricas, tracing (Prometheus, Grafana)
- Seguridad: OWASP Top 10, autenticación (OAuth2, JWT)
- Arquitectura hexagonal, DDD, event sourcing

### 🤖 INGENIERO DE IA (machine learning, deep learning, MLOps)
- Matemáticas para IA: álgebra lineal, cálculo, probabilidad y estadística
- Machine Learning clásico: regresión, clasificación, clustering, scikit-learn
- Deep Learning: redes neuronales, CNN, RNN, LSTM, Transformers
- Frameworks: PyTorch, TensorFlow, Hugging Face
- LLMs: prompt engineering, fine-tuning, RAG, agentes
- MLOps: versionado de datos y modelos, pipelines, MLflow, deployment de modelos
- Ética en IA, sesgos, interpretabilidad

## Cosas que SÍ puedo hacer:
- Explicar conceptos de programación con ejemplos en cualquier lenguaje popular (Python, JavaScript, Java, C++, C#, Go, Rust, PHP, Ruby, etc.)
- Ayudar a depurar (debuggear) código que el estudiante me envíe
- Diseñar rutas de aprendizaje según el objetivo del estudiante
- Corregir código con amabilidad y explicar por qué la versión mejorada es mejor
- Recomendar recursos (documentación, cursos, libros)
- Explicar buenas prácticas y patrones de diseño

## Cosas que NO puedo hacer:
- Hacer el trabajo/tarea del estudiante por él (soy su guía, no su sustituto)
- Dar certificaciones oficiales
- Juzgar o criticar duramente
- Responder en otro idioma que no sea español (salvo palabras técnicas universales)

## Formato de mis respuestas:
- CORTO (2-4 frases típico), salvo que pida una explicación profunda
- Siempre en ESPAÑOL
- Ejemplos de código con bloques markdown usando ```lenguaje
- Si corrijo: "¡Casi! La forma correcta es... porque..."
- Si el estudiante acierta: "¡Excelente!" / "¡Exacto!" / "¡Perfecto!" / "¡Muy bien!"

## Cuándo usar RAG (knowledge base):
- Si el estudiante pregunta por un tema específico, busca primero en la base de conocimiento con `search_knowledge` antes de responder
- Si no encuentras nada relevante, responde con tu conocimiento general
"""


NIVELES_DESCRIPCION_PROG = {
    "INICIO":       "Inicio - sin experiencia previa, primeros pasos en programación",
    "NOVATO":       "Novato - conceptos básicos y primer lenguaje",
    "APRENDIZ":     "Aprendiz - estructuras de control, funciones y POO inicial",
    "TECNICO":      "Técnico - frameworks, bases de datos y desarrollo web/móvil",
    "TECNOLOGO":    "Tecnólogo - arquitectura de software, APIs y despliegue",
    "INGENIERO":    "Ingeniero - sistemas distribuidos, DevOps y buenas prácticas",
    "INGENIERO_IA": "Ingeniero de IA - machine learning, deep learning y MLOps",
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
    nivel = student_data.get("nivel", "INICIO")
    nivel_desc = NIVELES_DESCRIPCION_PROG.get(nivel, "")
    modo = modo_actual or student_data.get("modo_actual", "conceptos")
    return f"""
## Información del estudiante actual
- Nombre: {student_data.get('nombre', 'Estudiante')}
- Nivel: {nivel} ({nivel_desc})
- Objetivo: {student_data.get('objetivo', 'no especificado')}
- Modo actual: {modo}

Adapta tu respuesta al nivel y modo del estudiante. Si el nivel es bajo (INICIO, NOVATO), usa analogías simples y evita jerga. Si el nivel es alto (INGENIERO, INGENIERO_IA), puedes profundizar en arquitectura y conceptos avanzados.
"""


def openrouter_response(user_message, student_data, modo_actual=""):
    """Llama a OpenRouter API."""
    if not OPENROUTER_CONFIGURED:
        return None
    try:
        rag_context = get_rag_context(user_message)
        student_ctx = build_student_context(student_data, modo_actual)
        prompt = f"""{SYSTEM_PROMPT_BASE}{student_ctx}{rag_context}

Estudiante dijo: {user_message}

Responde como el Ing. MOJICA de forma amable y motivadora. Mantén la respuesta corta (2-4 frases típicas) salvo que el tema requiera más profundidad. Responde SIEMPRE en español."""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://codeai-tutor.com",
            "X-Title": "CodeAI Tutor - Ing. MOJICA",
        }
        payload = {
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 600,
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

Estudiante dijo: {user_message}

Responde como el Ing. MOJICA, en español, de forma amable y motivadora:"""

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
    return "Disculpa, estoy teniendo problemas de conexión ahora mismo. Por favor, inténtalo de nuevo en un momento."


# ── Gestin de sesin del estudiante ───────────────────────────────────
def get_student_state():
    """Obtiene el estado del estudiante desde la sesin Flask."""
    if "student" not in session:
        session["student"] = {
            "nombre": "",
            "email": "",
            "nivel": "INICIO",
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
    """Genera audio TTS en español."""
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
            student['paso_actual'] = 'ask_name'
            session.modified = True
            return jsonify({
                'message': '¡Hola! Soy el Ing. MOJICA, tu tutor de programación con IA. Estoy aquí para enseñarte a programar las 24 horas, los 7 días de la semana, desde cero hasta Ingeniería de IA. ¡Empecemos! ¿Cómo te llamas?',
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

    # Accin: seleccionar nivel (los 7 niveles del Ing. MOJICA)
    niveles_validos = ["INICIO", "NOVATO", "APRENDIZ", "TECNICO", "TECNOLOGO", "INGENIERO", "INGENIERO_IA"]
    if action in niveles_validos:
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

    # Accin: seleccionar objetivo (en español, orientado a programación)
    objetivos = ["trabajo", "estudios", "emprendimiento", "ia", "web", "videojuegos", "datos", "hobby"]
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
                "message": "Para ver tu progreso, primero dime tu correo electrónico.",
                "botones": None,
                "paso": "ask_email",
            })
        progreso = obtener_progreso_estudiante(student["email"])
        if progreso:
            msg = f"Aquí tienes tu progreso, {student.get('nombre', 'estudiante')}:\n\n"
            msg += f"  Lecciones completadas: {progreso['lecciones_completadas']}\n"
            msg += f"  Conceptos aprendidos: {progreso['vocabulario_total']}\n"
            msg += f"  Errores registrados: {progreso['errores_totales']}\n"
            msg += f"\n¡Sigue así, lo estás haciendo genial! 🚀"
        else:
            msg = "Aún no has completado lecciones. ¡Vamos a practicar algo de programación!"
        return jsonify({
            "message": msg,
            "botones": [{"texto": "Continuar practicando", "valor": "change_mode"}],
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
        emoji_modo = info_modo["emoji"] if info_modo else "💡"
        welcome_msg = f"¡Excelente! Comenzaremos con el modo {emoji_modo} {nombre_modo}. ¿Qué te gustaría aprender o en qué puedo ayudarte?"
        return jsonify({
            "message": welcome_msg,
            "botones": [
                {"texto": "Cambiar modo", "valor": "change_mode"},
                {"texto": "Mi progreso", "valor": "progress"},
                {"texto": "Finalizar sesión", "valor": "goodbye"},
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

    # Accin: ver progreso (segundo handler, redundante pero seguro)
    if action == "progress":
        if not student.get("email"):
            return jsonify({
                "message": "Para ver tu progreso, primero necesito tu correo electrónico.",
                "botones": None,
                "paso": "ask_email",
            })
        progreso = obtener_progreso_estudiante(student["email"])
        if progreso:
            msg = f"Aquí tienes tu progreso, {student.get('nombre', 'estudiante')}:\n\n"
            msg += f"  Lecciones completadas: {progreso['lecciones_completadas']}\n"
            msg += f"  Conceptos aprendidos: {progreso['vocabulario_total']}\n"
            msg += f"  Errores registrados: {progreso['errores_totales']}\n"
            msg += f"\n¡Sigue así, lo estás haciendo genial! 🚀"
        else:
            msg = "Aún no has completado lecciones. ¡Vamos a practicar algo de programación!"
        return jsonify({
            "message": msg,
            "botones": [{"texto": "Continuar practicando", "valor": "change_mode"}],
            "paso": student.get("paso_actual"),
        })

    return jsonify({"message": "Acción no reconocida", "botones": None})


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
            "message": "¡Hola! Soy el Ing. MOJICA, tu tutor de programación con IA. Estoy aquí para enseñarte a programar las 24 horas, los 7 días de la semana, desde cero hasta Ingeniería de IA. ¡Empecemos! ¿Cómo te llamas?",
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
            student.get("modo_actual", "conceptos"),
        )
        # Guardar conversacin en BD
        try:
            if student.get("email"):
                guardar_conversacion({
                    "email": student["email"],
                    "nombre": student.get("nombre", ""),
                    "mensaje_usuario": user_message,
                    "respuesta_agente": response,
                    "modo": student.get("modo_actual", "conceptos"),
                    "nivel": student.get("nivel", "INICIO"),
                })
        except Exception as e:
            app.logger.error(f"Error guardando conversacion: {e}")
        return jsonify({
            "message": response,
            "botones": [
                {"texto": "Cambiar modo", "valor": "change_mode"},
                {"texto": "Mi progreso", "valor": "progress"},
                {"texto": "Finalizar sesión", "valor": "goodbye"},
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
        {"id": "es-ES-AlvaroNeural", "name": "Álvaro", "gender": "Male", "region": "España", "recommended": True},
        {"id": "es-ES-ElviraNeural", "name": "Elvira", "gender": "Female", "region": "España"},
        {"id": "es-ES-AlvaroNeural", "name": "Álvaro", "gender": "Male", "region": "España"},
        {"id": "es-MX-DaliaNeural", "name": "Dalia", "gender": "Female", "region": "México"},
        {"id": "es-MX-JorgeNeural", "name": "Jorge", "gender": "Male", "region": "México"},
        {"id": "es-AR-ElenaNeural", "name": "Elena", "gender": "Female", "region": "Argentina"},
        {"id": "es-AR-TomasNeural", "name": "Tomás", "gender": "Male", "region": "Argentina"},
        {"id": "es-CO-GonzaloNeural", "name": "Gonzalo", "gender": "Male", "region": "Colombia"},
        {"id": "es-CO-SalomeNeural", "name": "Salomé", "gender": "Female", "region": "Colombia"},
    ]
    return jsonify({"voices": voices, "current": TTS_VOICE})


@app.route("/api/reset", methods=["POST"])
def reset_session():
    """Reinicia la sesin del estudiante."""
    session.pop("student", None)
    return jsonify({"message": "Sesión reiniciada", "ok": True})


@app.route("/api/student", methods=["GET"])
def get_student_info():
    """Retorna la informacin del estudiante actual."""
    student = get_student_state()
    return jsonify({"student": student})


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "CodeAI Tutor - Ing. MOJICA",
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
    app.logger.info("CodeAI Tutor - Ing. MOJICA")
    app.logger.info("Enseña programación en 7 niveles: Inicio -> Ingeniero de IA")
    app.logger.info(f"Voice: {TTS_VOICE}")
    app.logger.info(f"Port: {port}")
    app.logger.info("=" * 60)
    app.run(host="0.0.0.0", port=port, debug=True)
