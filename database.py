"""
MÃ³dulo Supabase - Base de datos en la nube para EnglishAI Tutor
Almacena datos de estudiantes, progreso, conversaciones y vocabulario.
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

_supabase = None


def get_supabase():
    """Obtiene cliente Supabase (singleton)."""
    global _supabase
    if _supabase is not None:
        return _supabase

    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.warning("SUPABASE_URL/SUPABASE_KEY no configuradas - modo sin BD")
        return None

    try:
        from supabase import create_client

        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase conectado correctamente")
        return _supabase
    except Exception as e:
        logger.error(f"Error conectando Supabase: {e}")
        return None


def guardar_estudiante(datos):
    """
    Guarda o actualiza un estudiante en la tabla 'estudiantes'.
    datos: dict con campos del estudiante.
    Retorna (True, id) o (False, error).
    """
    sb = get_supabase()
    if sb is None:
        return False, "Supabase no disponible"

    try:
        registro = {
            "nombre": datos.get("nombre", ""),
            "email": datos.get("email", ""),
            "nivel": datos.get("nivel", "INICIO"),
            "idioma_nativo": datos.get("idioma_nativo", "es"),
            "objetivo": datos.get("objetivo", ""),
            "modo_actual": datos.get("modo_actual", ""),
            "paso_actual": datos.get("paso_actual", "welcome"),
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        result = sb.table("estudiantes").upsert(
            registro, on_conflict="email"
        ).execute()

        estudiante_id = None
        if hasattr(result, "data") and result.data:
            estudiante_id = result.data[0].get("id")

        logger.info(
            f"Estudiante guardado: {registro['nombre']} ({registro['nivel']})"
        )
        return True, estudiante_id

    except Exception as e:
        logger.error(f"Error guardando estudiante: {e}")
        return False, str(e)


def obtener_estudiante_por_email(email):
    """Obtiene un estudiante por su email."""
    sb = get_supabase()
    if sb is None:
        return None

    try:
        result = sb.table("estudiantes").select("*").eq("email", email).execute()
        if hasattr(result, "data") and result.data:
            return result.data[0]
        return None
    except Exception as e:
        logger.error(f"Error obteniendo estudiante: {e}")
        return None


def guardar_conversacion(datos):
    """
    Guarda un mensaje de la conversaciÃ³n en la tabla 'conversaciones'.
    """
    sb = get_supabase()
    if sb is None:
        return False, "Supabase no disponible"

    try:
        registro = {
            "estudiante_email": datos.get("email", ""),
            "estudiante_nombre": datos.get("nombre", ""),
            "mensaje_usuario": datos.get("mensaje_usuario", ""),
            "respuesta_agente": datos.get("respuesta_agente", ""),
            "modo": datos.get("modo", "conceptos"),
            "nivel": datos.get("nivel", "INICIO"),
            "created_at": datetime.utcnow().isoformat(),
        }

        result = sb.table("conversaciones").insert(registro).execute()

        conv_id = None
        if hasattr(result, "data") and result.data:
            conv_id = result.data[0].get("id")

        return True, conv_id

    except Exception as e:
        logger.error(f"Error guardando conversaciÃ³n: {e}")
        return False, str(e)


def guardar_vocabulario(datos):
    """
    Guarda una palabra aprendida en la tabla 'vocabulario_aprendido'.
    """
    sb = get_supabase()
    if sb is None:
        return False, "Supabase no disponible"

    try:
        registro = {
            "estudiante_email": datos.get("email", ""),
            "palabra": datos.get("palabra", ""),
            "traduccion": datos.get("traduccion", ""),
            "nivel": datos.get("nivel", "INICIO"),
            "ejemplo": datos.get("ejemplo", ""),
            "repasos": 0,
            "created_at": datetime.utcnow().isoformat(),
        }

        result = sb.table("vocabulario_aprendido").insert(registro).execute()

        vocab_id = None
        if hasattr(result, "data") and result.data:
            vocab_id = result.data[0].get("id")

        return True, vocab_id

    except Exception as e:
        logger.error(f"Error guardando vocabulario: {e}")
        return False, str(e)


def guardar_error_estudiante(datos):
    """
    Guarda un error cometido por el estudiante en la tabla 'errores_estudiante'.
    """
    sb = get_supabase()
    if sb is None:
        return False, "Supabase no disponible"

    try:
        registro = {
            "estudiante_email": datos.get("email", ""),
            "error": datos.get("error", ""),
            "correccion": datos.get("correccion", ""),
            "tema": datos.get("tema", ""),
            "nivel": datos.get("nivel", "INICIO"),
            "created_at": datetime.utcnow().isoformat(),
        }

        result = sb.table("errores_estudiante").insert(registro).execute()

        error_id = None
        if hasattr(result, "data") and result.data:
            error_id = result.data[0].get("id")

        return True, error_id

    except Exception as e:
        logger.error(f"Error guardando error: {e}")
        return False, str(e)


def guardar_leccion_completada(datos):
    """
    Marca una lecciÃ³n como completada en la tabla 'lecciones_completadas'.
    """
    sb = get_supabase()
    if sb is None:
        return False, "Supabase no disponible"

    try:
        registro = {
            "estudiante_email": datos.get("email", ""),
            "tema": datos.get("tema", ""),
            "nivel": datos.get("nivel", "INICIO"),
            "score": datos.get("score", 0),
            "modo": datos.get("modo", ""),
            "created_at": datetime.utcnow().isoformat(),
        }

        result = sb.table("lecciones_completadas").insert(registro).execute()

        leccion_id = None
        if hasattr(result, "data") and result.data:
            leccion_id = result.data[0].get("id")

        return True, leccion_id

    except Exception as e:
        logger.error(f"Error guardando lecciÃ³n: {e}")
        return False, str(e)


def obtener_progreso_estudiante(email):
    """
    Obtiene el progreso de un estudiante: lecciones, vocabulario, errores.
    """
    sb = get_supabase()
    if sb is None:
        return None

    try:
        lecciones = (
            sb.table("lecciones_completadas")
            .select("*")
            .eq("estudiante_email", email)
            .execute()
        )
        vocabulario = (
            sb.table("vocabulario_aprendido")
            .select("*")
            .eq("estudiante_email", email)
            .execute()
        )
        errores = (
            sb.table("errores_estudiante")
            .select("*")
            .eq("estudiante_email", email)
            .execute()
        )

        return {
            "lecciones_completadas": len(lecciones.data) if hasattr(lecciones, "data") else 0,
            "vocabulario_total": len(vocabulario.data) if hasattr(vocabulario, "data") else 0,
            "errores_totales": len(errores.data) if hasattr(errores, "data") else 0,
            "ultima_leccion": lecciones.data[0] if hasattr(lecciones, "data") and lecciones.data else None,
        }
    except Exception as e:
        logger.error(f"Error obteniendo progreso: {e}")
        return None


# ── Aliases de compatibilidad (deprecated) ────────────────────────────
# Mantener nombres antiguos para no romper imports
guardar_usuario = guardar_estudiante
obtener_usuario = obtener_estudiante_por_email
guardar_consulta_adicional = guardar_conversacion


