# Manual de Usuario - CodeAI Tutor (Ing. MOJICA)

> Su Profe de Programación con IA en español, disponible 24/7. Enseña desde cero absoluto hasta Ingeniería de IA.

Bienvenido al manual oficial del agente **CodeAI Tutor**, un profesor virtual de programación construido con Flask, Pinecone RAG, Supabase, edge-tts y OpenRouter/Gemini. Este manual explica en detalle cómo funciona, cómo instalarlo, cómo personalizarlo y cómo resolver los problemas más comunes.

---

## Tabla de Contenidos

1. ¿Qué es CodeAI Tutor?
2. Características principales
3. Arquitectura del sistema
4. Instalación paso a paso
5. Configuración de servicios
6. Cómo funciona el flujo conversacional
7. Modos de aprendizaje
8. Los 7 niveles de programación
9. API Reference
10. Mantenimiento y operaciones
11. Personalización
12. Solución de problemas

Apéndices:
- A. Glosario de términos técnicos
- B. Comandos útiles
- C. Estructura de archivos

---

## 1. ¿Qué es CodeAI Tutor?

CodeAI Tutor es un agente profesor de programación disponible las 24 horas, los 7 días de la semana. Utiliza Inteligencia Artificial avanzada para enseñar programación a hispanohablantes en 7 niveles progresivos: **INICIO, NOVATO, APRENDIZ, TÉCNICO, TECNÓLOGO, INGENIERO e INGENIERO DE IA**.

### El profesor: Ing. MOJICA

- **Nombre**: Ing. MOJICA (Su Profe de Programación)
- **Idioma**: Español nativo (entiende términos técnicos en inglés)
- **Personalidad**: Amable, paciente, motivador y didáctico
- **Especialidad**: Programación desde cero hasta Ingeniería de IA

### Filosofía pedagógica

Ing. MOJICA sigue estos principios:

1. **Cada error es una oportunidad de aprendizaje**: nunca se juzga al estudiante, se le guía.
2. **Las analogías simples son la mejor herramienta**: una variable es una caja con etiqueta, un bucle es repetir una receta, etc.
3. **La práctica constante es la clave**: el estudiante programa desde el primer día.
4. **Adaptación al nivel**: el lenguaje y la profundidad se ajustan automáticamente.
5. **Celebrar los pequeños logros**: cada paso cuenta en el camino del aprendizaje.

---

## 2. Características principales

### Funcionalidades del estudiante

- ✅ Saludo personalizado en español
- ✅ Selección de nivel entre los 7 niveles disponibles
- ✅ Definición de objetivo de aprendizaje (trabajo, estudios, IA, web, etc.)
- ✅ 6 modos de aprendizaje: Conceptos, Práctica, Proyectos, Quiz, Código, IA
- ✅ Respuestas adaptadas al nivel y al modo elegido
- ✅ Audio TTS en español con voces neurales de Microsoft
- ✅ Visualización de progreso (lecciones, conceptos, errores)
- ✅ Cambio de modo en cualquier momento
- ✅ Botones interactivos para guiar la conversación

### Funcionalidades técnicas

- ✅ API REST con Flask
- ✅ Integración con LLM (OpenRouter por defecto, Gemini como fallback)
- ✅ RAG (Retrieval-Augmented Generation) con Pinecone
- ✅ Base de datos PostgreSQL en Supabase
- ✅ Persistencia de sesiones con Flask session
- ✅ Edge-TTS para audio de alta calidad
- ✅ Listo para deploy en Heroku (Procfile incluido)
- ✅ Configuración mediante variables de entorno

---

## 3. Arquitectura del sistema

```
┌─────────────────────┐
│   Navegador Web     │
│  (templates/index)  │
└──────────┬──────────┘
           │ HTTP/JSON
           ▼
┌─────────────────────┐
│   Flask App (app.py)│
│  ┌───────────────┐  │
│  │ Endpoints REST│  │
│  └───────┬───────┘  │
│          │          │
│  ┌───────▼───────┐  │
│  │ guion.py      │◄─┼──► Validación, flujo conversacional
│  └───────┬───────┘  │
│  ┌───────▼───────┐  │
│  │ LLM (OpenR/G) │──┼──► OpenRouter / Gemini
│  └───────┬───────┘  │
│  ┌───────▼───────┐  │
│  │ RAG (rag.py)  │──┼──► Pinecone (embeddings)
│  └───────┬───────┘  │
│  ┌───────▼───────┐  │
│  │ DB (database) │──┼──► Supabase (PostgreSQL)
│  └───────────────┘  │
└─────────────────────┘
```

### Componentes principales

- **`app.py`**: Aplicación Flask con todas las rutas y el system prompt en español.
- **`guion.py`**: Flujo conversacional (welcome, ask_name, ask_level, ask_goal, select_mode, in_session, change_mode, ask_question, goodbye).
- **`database.py`**: Cliente Supabase y operaciones CRUD.
- **`rag.py`**: Integración con Pinecone para búsqueda semántica.
- **`upload_knowledge.py`**: Script para indexar la base de conocimiento.
- **`conocimiento_programacion.md`**: Base de conocimiento en español (currículo completo de los 7 niveles).
- **`schema_supabase.sql`**: Schema de la base de datos con la CHECK constraint para los 7 niveles.
- **`templates/index.html`**: UI del chat en español.

PLACEHOLDER_PART2
## 4. Instalación paso a paso

### Requisitos previos

- Python 3.10 o superior
- pip (gestor de paquetes)
- Una cuenta en [OpenRouter](https://openrouter.ai/) o [Google AI Studio](https://aistudio.google.com/) para el LLM
- Una cuenta en [Pinecone](https://www.pinecone.io/) para el RAG
- Una cuenta en [Supabase](https://supabase.com/) para la base de datos

### Paso 1: Clonar o descargar el proyecto

```bash
git clone https://github.com/ingjcesarmojica/Profeprogramacion.git
cd Profeprogramacion
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Activar:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar variables de entorno

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Edita `.env` con tus claves reales (ver sección 5).

### Paso 5: Crear tablas en Supabase

Ejecuta el SQL en `schema_supabase.sql` desde el SQL Editor de Supabase Dashboard.

Si vienes de una versión anterior, actualiza la CHECK constraint:

```sql
ALTER TABLE estudiantes DROP CONSTRAINT IF EXISTS estudiantes_nivel_check;
ALTER TABLE estudiantes ADD CONSTRAINT estudiantes_nivel_check
  CHECK (nivel IN ('INICIO','NOVATO','APRENDIZ','TECNICO','TECNOLOGO','INGENIERO','INGENIERO_IA'));
```

### Paso 6: Indexar conocimiento en Pinecone

```bash
python upload_knowledge.py
```

Subirá `conocimiento_programacion.md` a Pinecone para que el RAG pueda consultarlo.

### Paso 7: Ejecutar

```bash
python app.py
```

Abre `http://localhost:5000` y verás a Ing. MOJICA listo para enseñarte programación.

---

## 5. Configuración de servicios

### Variables de entorno (`.env`)

```bash
# --- LLM principal (obligatorio) ---
OPENROUTER_API_KEY=tu_clave_openrouter
OPENROUTER_MODEL=xiaomi/mimo-v2.5

# --- Gemini como fallback (obligatorio) ---
GEMINI_API_KEY=tu_clave_gemini

# --- Pinecone para RAG (obligatorio) ---
PINECONE_API_KEY=tu_clave_pinecone

# --- Supabase para base de datos (obligatorio) ---
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=tu_clave_supabase

# --- TTS (opcional, default ya incluido) ---
TTS_VOICE=es-ES-ElviraNeural

# --- Servidor (opcional) ---
PORT=5000

# --- Seguridad (obligatorio en producción) ---
SECRET_KEY=tu-clave-secreta-unica
```

### Cómo obtener cada API key

#### OpenRouter
1. Ve a [openrouter.ai](https://openrouter.ai/) y crea una cuenta
2. Ve a "Keys" y crea una nueva clave
3. Cópiala en `OPENROUTER_API_KEY`

#### Google AI Studio (Gemini)
1. Ve a [aistudio.google.com](https://aistudio.google.com/)
2. Crea una clave de API
3. Cópiala en `GEMINI_API_KEY`

#### Pinecone
1. Ve a [pinecone.io](https://www.pinecone.io/) y crea una cuenta
2. Crea un nuevo índice con dimensión 768 (Gemini embeddings)
3. Cópiala en `PINECONE_API_KEY`

#### Supabase
1. Ve a [supabase.com](https://supabase.com/) y crea un proyecto
2. Ve a Settings → API y copia la URL y la `anon` key

### Configuración de Pinecone

El script `rag.py` espera:
- Índice con nombre `codeai-tutor` (configurable en `INDEX_NAME`)
- Dimensión 768 (embeddings de Gemini `embedding-001`)
- Métrica cosine

---

PLACEHOLDER_PART3
## 6. Cómo funciona el flujo conversacional

### Diagrama de estados

```
[init]
  │
  ▼
[welcome] ───► [ask_name] ───► [ask_level] ───► [ask_goal] ───► [select_mode]
                                                                     │
                                                                     ▼
                                            ┌────────────────► [in_session] ◄──┐
                                            │                         │         │
                                            │              ┌──────────┘         │
                                            │              │                    │
                                            │         [change_mode]          [goodbye]
                                            │              │                    
                                            └──────────────┘                    
                                                       [ask_question]
```

### Estados detallados

| Estado | Acción | Siguiente |
|--------|--------|-----------|
| `welcome` | Saluda y pregunta el nombre | `ask_name` |
| `ask_name` | Valida el nombre (mínimo 2 letras) | `ask_level` |
| `ask_level` | Muestra 7 botones con los niveles | `ask_goal` |
| `ask_goal` | Pregunta objetivo (8 opciones) | `select_mode` |
| `select_mode` | Muestra los 6 modos | `in_session` |
| `in_session` | Genera respuesta con LLM | `in_session` (loop) |
| `change_mode` | Permite cambiar de modo | `in_session` |
| `ask_question` | Responde preguntas libres | `in_session` |
| `goodbye` | Despedida y fin de sesión | (ninguno) |

### Cómo se almacenan las sesiones

- **Sesión Flask**: nombre, email, nivel, objetivo, modo actual, paso actual
- **Supabase (estudiantes)**: persiste los datos del estudiante al iniciar sesión
- **Supabase (conversaciones)**: guarda cada mensaje y respuesta
- **Supabase (lecciones_completadas)**: registra lecciones finalizadas
- **Supabase (vocabulario_aprendido)**: lleva registro de conceptos aprendidos
- **Supabase (errores_estudiante)**: almacena errores para repaso futuro

---

## 7. Modos de aprendizaje

### 💡 Conceptos (default)

Modo teórico. El profesor explica los conceptos con ejemplos claros y analogías cotidianas. Ideal para entender "el por qué" de las cosas.

**Cuándo usarlo**: cuando estás aprendiendo un tema nuevo y necesitas una explicación estructurada.

### ⌨️ Práctica

Modo hands-on. El profesor te propone ejercicios y retos paso a paso, validando tu código y dándote feedback.

**Cuándo usarlo**: cuando ya entiendes los conceptos y quieres afianzarlos programando.

### 🚀 Proyectos

Modo guiado. Construyes proyectos reales (calculadora, API, juego, app web) con la ayuda del profesor en cada paso.

**Cuándo usarlo**: cuando quieres construir algo concreto para tu portafolio.

### 🎯 Quiz

Modo interactivo. El profesor te hace preguntas para evaluar tu nivel y reforzar lo aprendido.

**Cuándo usarlo**: para autoevaluarte antes de avanzar al siguiente nivel.

### 🧩 Código

Modo depuración. Le envías tu código al profesor y él lo revisa, explica y mejora contigo.

**Cuándo usarlo**: cuando tienes un error que no entiendes o quieres mejorar una solución.

### 🤖 IA

Modo especializado. Contenido exclusivo sobre Machine Learning, Deep Learning, LLMs, MLOps y ética en IA.

**Cuándo usarlo**: en el nivel INGENIERO_IA, o cuando quieras profundizar en inteligencia artificial.

---

## 8. Los 7 niveles de programación

### 🌱 INICIO (sin experiencia previa)

**Perfil**: nunca ha programado o tiene una idea muy vaga.

**Temas**: pensamiento computacional, variables, tipos básicos, `print()`, operadores aritméticos y de comparación.

**Lenguaje recomendado**: Python (sintaxis clara, comunidad grande).

### 🐣 NOVATO (primer lenguaje)

**Perfil**: ya escribió su primer "Hola mundo" y conoce los tipos básicos.

**Temas**: condicionales (if/else), bucles (for/while), listas, funciones, manejo de strings, módulos.

### 📚 APRENDIZ (estructuras y POO)

**Perfil**: maneja bucles y funciones, listo para POO.

**Temas**: funciones avanzadas, excepciones, archivos, POO (clases, herencia, encapsulamiento), Git.

### 🛠️ TÉCNICO (frameworks y web/móvil)

**Perfil**: ya programa con soltura en al menos un lenguaje.

**Temas**: HTML/CSS/JS, un framework (React/Vue/Django/Flask), SQL, APIs REST, testing, Git avanzado.

PLACEHOLDER_PART4
### 🎓 TECNÓLOGO (arquitectura y despliegue)

**Perfil**: domina al menos un framework y desarrolla aplicaciones completas.

**Temas**: patrones de diseño (MVC, Singleton, Factory), Docker, CI/CD, despliegue en cloud (AWS/GCP/Azure/Vercel), bases de datos NoSQL, microservicios.

### 🏗️ INGENIERO (sistemas distribuidos y DevOps)

**Perfil**: arquitecto de software o lead developer.

**Temas**: Kubernetes, Kafka/RabbitMQ, principios SOLID, observabilidad (Prometheus, Grafana), seguridad (OAuth2, JWT, OWASP), Domain-Driven Design.

### 🤖 INGENIERO DE IA (Machine Learning y MLOps)

**Perfil**: científico de datos o ingeniero de ML/AI.

**Temas**: álgebra lineal, estadística, Machine Learning clásico, Deep Learning, PyTorch/TensorFlow, Transformers, LLMs (GPT, Claude, Llama), RAG, MLOps, ética en IA.

---

## 9. API Reference

### GET `/`

Sirve la UI del chat (`templates/index.html`).

### POST `/api/chat`

Endpoint principal del chat. Acepta dos tipos de payload:

#### A) Mensaje de texto del estudiante

```json
{ "message": "¿Qué es una variable en Python?" }
```

#### B) Acción de botón

```json
{ "action": "INICIO" }
```

Acciones válidas para niveles: `INICIO`, `NOVATO`, `APRENDIZ`, `TECNICO`, `TECNOLOGO`, `INGENIERO`, `INGENIERO_IA`.

Acciones válidas para objetivos: `trabajo`, `estudios`, `emprendimiento`, `ia`, `web`, `videojuegos`, `datos`, `hobby`.

Acciones válidas para modos: `conceptos`, `practica`, `proyectos`, `quiz`, `codigo`, `ia`.

Otras acciones: `init`, `change_mode`, `progress`, `goodbye`.

### POST `/api/speak`

Genera audio TTS en español.

```json
{ "text": "¡Hola! Soy Ing. MOJICA." }
```

Retorna un JSON con `audioContent` (base64) y `audioUrl`.

### GET `/api/levels`

Devuelve los 7 niveles disponibles:

```json
{ "levels": ["INICIO","NOVATO","APRENDIZ","TECNICO","TECNOLOGO","INGENIERO","INGENIERO_IA"] }
```

### GET `/api/modes`

Devuelve los 6 modos con su información.

### GET `/api/voices`

Devuelve las 8 voces TTS disponibles en español.

### GET `/api/health`

Health check del servicio.

```json
{
  "status": "ok",
  "service": "CodeAI Tutor - Ing. MOJICA",
  "version": "1.0",
  "rag_available": true,
  "gemini_configured": true,
  "openrouter_configured": true
}
```

### GET `/api/pinecone-status`

Estadísticas del índice Pinecone (total de vectores indexados).

### GET `/api/student`

Información del estudiante en la sesión actual.

### POST `/api/reset`

Reinicia la sesión del estudiante.

---

## 10. Mantenimiento y operaciones

### Re-indexar conocimiento

```bash
python upload_knowledge.py
```

Útil cuando modificas `conocimiento_programacion.md` o quieres actualizar el RAG.

### Ver logs

```bash
# Los logs están en stdout
python app.py

# Para producción (Gunicorn)
heroku logs --tail
```

### Backup de Supabase

Desde el Dashboard de Supabase:

1. Settings → Database → Backups
2. Activar backups automáticos (plan Pro) o hacer backups manuales con `pg_dump`.

### Monitoreo

- **Logs**: nivel INFO por defecto en Flask
- **Errores**: se loguean con `app.logger.error(...)` y `traceback`
- **Health check**: `/api/health` retorna el estado del servicio

### Actualizar dependencias

```bash
pip install --upgrade -r requirements.txt
```

### Deploy en producción (Heroku)

```bash
heroku login
heroku create tu-app-codeai
heroku config:set OPENROUTER_API_KEY=xxx
heroku config:set GEMINI_API_KEY=xxx
git push heroku main
heroku run python upload_knowledge.py
```

---

PLACEHOLDER_PART4B
## 11. Personalización

### Cambiar la personalidad del profesor

Edita el `SYSTEM_PROMPT_BASE` en `app.py`. Ejemplo:

```python
SYSTEM_PROMPT_BASE = '''
Eres el Ing. MOJICA, un profesor de programación amable...
[Personaliza el tono, las frases motivadoras, etc.]
'''
```

### Cambiar la voz TTS por defecto

Edita `.env`:

```bash
TTS_VOICE=es-MX-JorgeNeural
```

Voces disponibles (acento latino por defecto): `es-MX-JorgeNeural`, `es-MX-DaliaNeural`, `es-CO-GonzaloNeural`, `es-CO-SalomeNeural`, `es-AR-TomasNeural`, `es-AR-ElenaNeural`, `es-ES-AlvaroNeural`, `es-ES-ElviraNeural`.

### Agregar más modos de aprendizaje

1. Agrega el modo en `guion.py` → diccionario `MODOS`
2. Actualiza el botón en `PASOS["select_mode"]["botones"]` y `PASOS["change_mode"]["botones"]`
3. Actualiza `MODOS_VALIDOS` en `handle_action()` de `app.py`

### Cambiar el esquema de BD

Edita `schema_supabase.sql` y aplica los cambios en Supabase.

### Cambiar la base de conocimiento

Edita `conocimiento_programacion.md` y ejecuta:

```bash
python upload_knowledge.py
```

### Limitar el número de mensajes

En `database.py`, función `guardar_conversacion()`, agrega lógica para mantener solo los últimos N mensajes por estudiante.

---

## 12. Solución de problemas

### "GEMINI_API_KEY no configurada"

- Verifica que `.env` tenga la variable
- Reinicia el servidor

### "Pinecone not connected"

- Verifica tu `PINECONE_API_KEY`
- Verifica que el índice exista en Pinecone Dashboard

### El bot responde muy lento

- OpenRouter/Gemini pueden tener latencia alta
- Considera usar un modelo más rápido (cambiar `OPENROUTER_MODEL`)
- Reduce `max_tokens` en el system prompt

### "Supabase no disponible"

- Verifica `SUPABASE_URL` y `SUPABASE_KEY`
- Verifica que las tablas existan (ejecuta `schema_supabase.sql`)

### El audio TTS no suena

- Verifica que `edge-tts` esté instalado
- El navegador puede bloquear el audio automático; revisa la consola

### Error 500 en `/api/chat`

- Revisa los logs del servidor
- Generalmente es por falta de API keys

### El bot no entiende el nombre

- El nombre debe tener al menos 2 letras y no ser solo números

### Las sesiones no persisten

- Flask usa cookies de sesión; verifica que `SECRET_KEY` esté configurado
- En producción, asegúrate de que las cookies estén habilitadas

### El bot se "olvida" del nivel

- El nivel se guarda en `session["student"]["nivel"]`
- Se persiste en Supabase solo cuando se inicia una sesión de práctica

---

## Apéndice A: Glosario de términos técnicos

| Término | Significado |
|---------|-------------|
| **LLM** | Large Language Model (modelo de lenguaje grande como GPT, Gemini) |
| **RAG** | Retrieval-Augmented Generation: combina LLM con búsqueda en una base de conocimiento |
| **Embeddings** | Representación numérica de texto que captura su significado |
| **Pinecone** | Base de datos vectorial para búsqueda semántica |
| **Supabase** | Backend-as-a-Service con PostgreSQL, autenticación y storage |
| **Flask** | Microframework web para Python |
| **TTS** | Text-to-Speech: convierte texto en audio |
| **Edge TTS** | Servicio de Microsoft para TTS neural |
| **OpenRouter** | Proxy para acceder a múltiples LLMs con una sola API |
| **Gemini** | Familia de modelos LLM de Google |
| **System prompt** | Instrucciones iniciales que definen el comportamiento del LLM |
| **POO** | Programación Orientada a Objetos |
| **CI/CD** | Continuous Integration / Continuous Deployment |
| **MLOps** | Machine Learning Operations |

---

## Apéndice B: Comandos útiles

```bash
# Instalar
pip install -r requirements.txt

# Ejecutar desarrollo
python app.py

# Ejecutar producción
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2

# Re-indexar conocimiento
python upload_knowledge.py

# Test rápido
curl http://localhost:5000/api/health

# Ver voces TTS
curl http://localhost:5000/api/voices

# Limpiar cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +
```

---

## Apéndice C: Estructura de archivos

```
agentcallprogramacion-main/
+- app.py                       # Flask app + system prompt
+- database.py                  # Cliente Supabase
+- rag.py                       # RAG con Pinecone
+- guion.py                     # Flujo conversacional
+- upload_knowledge.py          # Indexar conocimiento
+- conocimiento_programacion.md # Base de conocimiento en español
+- schema_supabase.sql          # Schema de BD
+- requirements.txt             # Dependencias
+- .env.example                 # Template de variables
+- .gitignore                   # Archivos ignorados
+- Procfile                     # Deploy Heroku
+- start.sh                     # Script de arranque
+- runtime.txt                  # Versión de Python
+- README.md                    # Documentación principal
+- MANUAL.md                    # Este manual
+- templates/
   +- index.html                # Chat UI
```

---

## Soporte y contacto

- **Repositorio**: https://github.com/ingjcesarmojica/Profeprogramacion
- **Issues**: https://github.com/ingjcesarmojica/Profeprogramacion/issues

¡Bienvenido al mundo de la programación con Ing. MOJICA, Su Profe de Programación! 🚀




