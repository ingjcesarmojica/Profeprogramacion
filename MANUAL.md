# Manual de Usuario - EnglishAI Tutor (Mr. James)

> Guia completa de como funciona, se instala y se usa el agente profesor de ingles.

---

## Tabla de Contenidos

1. [Que es EnglishAI Tutor?](#1-que-es-englishai-tutor)
2. [Caracteristicas principales](#2-caracteristicas-principales)
3. [Arquitectura del sistema](#3-arquitectura-del-sistema)
4. [Instalacion paso a paso](#4-instalacion-paso-a-paso)
5. [Configuracion de servicios](#5-configuracion-de-servicios)
6. [Como funciona el flujo conversacional](#6-como-funciona-el-flujo-conversacional)
7. [Modos de aprendizaje](#7-modos-de-aprendizaje)
8. [Niveles CEFR](#8-niveles-cefr)
9. [API Reference](#9-api-reference)
10. [Mantenimiento y operaciones](#10-mantenimiento-y-operaciones)
11. [Personalizacion](#11-personalizacion)
12. [Solucion de problemas](#12-solucion-de-problemas)

---

## 1. Que es EnglishAI Tutor?

**EnglishAI Tutor** es un agente conversacional de inteligencia artificial diseñado para ensenar ingles a hispanohablantes de manera personalizada, 24/7.

### El profesor: Mr. James

- **Nombre**: Mr. James (James Wilson)
- **Nacionalidad**: Estadounidense (California)
- **Especialidad**: Ensenanza de ingles como segundo idioma (ESL/EFL)
- **Experiencia simulada**: 15 anos ensenando a hispanohablantes
- **Idiomas**: Ingles (nativo), Espanol (fluido)
- **Personalidad**: Pacifico, alentador, claro, adaptativo

### Filosofia pedagogica

Mr. James sigue estos principios:

- **Metodo socratico**: guia al estudiante para descubrir respuestas
- **Correccion constructiva**: nunca hace sentir mal al estudiante
- **Celebracion del progreso**: refuerza cada logro, por pequeno que sea
- **Ejemplos contextuales**: usa situaciones relevantes para hispanohablantes
- **Conciencia linguistica**: conoce los errores tipicos de hablantes de espanol

---

## 2. Caracteristicas principales

### Funcionalidades del estudiante

| Caracteristica | Descripcion |
|---|---|
| Clases personalizadas | Adaptadas al nivel CEFR (A1-C2) |
| 5 modos de practica | Conversation, Grammar, Vocabulary, Quiz, Pronunciation |
| 6 objetivos | Travel, Work, Studies, Exams, Entertainment, Personal |
| Audio en ingles | TTS con voces neuronales (US, UK, AU) |
| Seguimiento de progreso | Lecciones, vocabulario, errores |
| Base de conocimiento | RAG con temario completo |
| Disponibilidad 24/7 | Siempre disponible para practicar |

### Funcionalidades tecnicas

| Caracteristica | Descripcion |
|---|---|
| Multi-LLM | OpenRouter (principal) + Gemini (fallback) |
| RAG vectorial | Pinecone con embeddings de Gemini |
| Base de datos | Supabase (PostgreSQL) |
| TTS neural | edge-tts (Microsoft) |
| Sesiones persistentes | Flask session con cookies |
| API REST | 11 endpoints documentados |
| Deploy-ready | Gunicorn + Procfile para Heroku |

---

## 3. Arquitectura del sistema

```
+----------------------------------+
|       NAVEGADOR (Estudiante)     |
|   index.html (Chat UI)           |
+----------------------------------+
              |
              | HTTP (fetch)
              v
+----------------------------------+
|       FLASK APP (app.py)         |
|   - Rutas API REST               |
|   - Gestion de sesiones          |
|   - Sistema de pasos             |
+----------------------------------+
        |       |        |         |
        v       v        v         v
+--------+  +------+  +-------+  +--------+
|edge-tts|  |  LLM |  |  RAG  |  |Supabase|
|  (TTS) |  |(OpenR|  |(Pinec)|  |  (BD)  |
|        |  |/Gem) |  |  one) |  |        |
+--------+  +------+  +-------+  +--------+
```

### Componentes principales

1. **Frontend** (`templates/index.html`)
   - Interfaz de chat tipo widget
   - Avatar del profesor (emoji)
   - Burbujas de conversacion
   - Botones contextuales
   - Boton de audio (TTS)

2. **Backend Flask** (`app.py`)
   - 11 endpoints REST
   - Sistema de sesiones
   - Manejo del flujo conversacional
   - Construccion de prompts para LLM

3. **LLM** (OpenRouter / Gemini)
   - Genera respuestas del profesor
   - Explica gramatica
   - Corrige errores
   - Mantiene la personalidad

4. **RAG** (Pinecone + Gemini embeddings)
   - Almacena conocimiento pedagogico
   - Busca contexto relevante
   - Enriquece las respuestas del LLM

5. **Base de datos** (Supabase)
   - Perfil del estudiante
   - Historial de conversaciones
   - Progreso y metricas
   - Vocabulario aprendido

6. **TTS** (edge-tts)
   - Convierte texto a audio
   - 7 voces en ingles disponibles
   - Audio base64 para reproduccion

---

## 4. Instalacion paso a paso

### Requisitos previos

- Python 3.11+
- pip
- Una cuenta en cada servicio:
  - OpenRouter (https://openrouter.ai) **o** Google AI Studio (Gemini)
  - Pinecone (https://pinecone.io)
  - Supabase (https://supabase.com)

### Paso 1: Clonar o descargar el proyecto

```bash
cd E:\AgentesMailab\AgenteIngles\agentcallpingles-main
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

Dependencias instaladas:
- Flask 3.1.1 (web framework)
- Flask-CORS 5.0.1 (CORS)
- edge-tts 7.2.8 (TTS)
- google-generativeai 0.8.0 (Gemini)
- gunicorn 23.0.0 (production server)
- python-dotenv 1.1.0 (env vars)
- pinecone 6.0.0 (vector DB)
- PyPDF2 3.0.0 (PDF processing)
- supabase 2.0.0 (database client)

### Paso 4: Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales (ver seccion 5).

### Paso 5: Crear tablas en Supabase

1. Ir a Supabase Dashboard > SQL Editor
2. Copiar el contenido de `schema_supabase.sql`
3. Ejecutar

### Paso 6: Indexar conocimiento en Pinecone

```bash
python upload_knowledge.py
```

Esto sube `conocimiento_ingles.md` (~20KB) a Pinecone, creando chunks con embeddings.

### Paso 7: Ejecutar

```bash
python app.py
```

Abrir http://localhost:5000

---

## 5. Configuracion de servicios

### Variables de entorno (`.env`)

```bash
# --- LLM principal (obligatorio) ---
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
OPENROUTER_MODEL=xiaomi/mimo-v2.5

# --- Gemini como fallback (obligatorio) ---
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXX

# --- Pinecone para RAG (obligatorio) ---
PINECONE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# --- Supabase para base de datos (obligatorio) ---
SUPABASE_URL=https://tuproyecto.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx

# --- TTS (opcional, default ya incluido) ---
TTS_VOICE=en-US-GuyNeural

# --- Servidor (opcional) ---
PORT=5000

# --- Seguridad (obligatorio en produccion) ---
SECRET_KEY=tu-clave-secreta-segura-aqui
```

### Como obtener cada API key

#### OpenRouter
1. Ir a https://openrouter.ai
2. Crear cuenta
3. Ir a "Keys" > "Create Key"
4. Copiar la key

#### Google AI Studio (Gemini)
1. Ir a https://aistudio.google.com
2. Crear API key
3. Copiar la key

#### Pinecone
1. Ir a https://app.pinecone.io
2. Crear cuenta
3. Crear un API key
4. El index se crea automaticamente al ejecutar `upload_knowledge.py`

#### Supabase
1. Ir a https://supabase.com
2. Crear nuevo proyecto
3. Settings > API
4. Copiar `URL` y `anon public` key

### Configuracion de Pinecone

El sistema crea automaticamente un indice llamado **`englishai-tutor`** con:
- Dimension: 768 (compatible con Gemini embeddings)
- Metrica: cosine
- Cloud: AWS
- Region: us-east-1

Si necesitas otra region, edita `rag.py` linea 42.

---

## 6. Como funciona el flujo conversacional

### Diagrama de estados

```
INICIO
   |
   v
[welcome] "Hola! Soy Mr. James. Cual es tu nombre?"
   |
   v
[ask_name] "Cual es tu nivel de ingles?" (muestra botones A1-C2)
   |
   v
[ask_level] "Cual es tu objetivo?" (muestra botones: Travel, Work, etc.)
   |
   v
[ask_goal] "Que quieres practicar?" (muestra modos)
   |
   v
[select_mode] --(selecciona modo)--> [in_session]
                                                |
                                                v
                              "Empecemos [Modo] practice!"
                                                |
                                                v
                              Conversacion libre con LLM
                                                |
                                +---------------+---------------+
                                |               |               |
                          change_mode      progress        goodbye
                                |               |               |
                                v               v               v
                         [change_mode]    Muestra stats    [goodbye]
                          (cambia modo)    del estudiante   (fin)
```

### Estados detallados

| Estado | Mensaje | Input esperado | Siguiente estado |
|---|---|---|---|
| `welcome` | "Hello! I am Mr. James..." | (ninguno, solo inicial) | `ask_name` |
| `ask_name` | "What is your name?" | texto libre (nombre) | `ask_level` |
| `ask_level` | "What is your level?" | boton A1/A2/B1/B2/C1/C2 | `ask_goal` |
| `ask_goal` | "What is your goal?" | boton travel/work/studies/etc | `select_mode` |
| `select_mode` | "What to practice today?" | boton modo | `in_session` |
| `in_session` | (generado por LLM) | texto libre | `in_session` (loop) |
| `change_mode` | "What to practice now?" | boton modo | `in_session` |
| `goodbye` | "It was a pleasure..." | (ninguno) | fin |

### Como se almacenan las sesiones

Flask usa sesiones con cookies firmadas. El estado del estudiante se guarda en:

```python
session["student"] = {
    "nombre": "Carlos",
    "email": "carlos@example.com",  # si lo ingreso
    "nivel": "B1",
    "objetivo": "work",
    "modo_actual": "conversation",
    "paso_actual": "in_session",
    "registered": False
}
```

El `SECRET_KEY` se usa para firmar las cookies. En produccion, usa uno seguro.

---

## 7. Modos de aprendizaje

### Conversation (Conversacion) - Default

**Proposito**: Practica libre sobre cualquier tema.

**Como funciona**:
- El LLM responde como Mr. James
- Habla 100% en ingles
- Corrige errores sutilmente
- Adapta complejidad al nivel del estudiante

**Ejemplo**:
```
Estudiante: I go to the store yesterday
Mr. James: Great try! Just a small correction: 
"yesterday" is past time, so we use past simple:
"I went to the store yesterday." 
Can you make another sentence using past simple?
```

### Grammar (Gramatica)

**Proposito**: Ensenar reglas gramaticales con ejemplos.

**Como funciona**:
- LLM explica la regla
- Da 2-3 ejemplos
- Pide al estudiante que practique

**Ejemplo**:
```
Estudiante: Teach me about present perfect
Mr. James: Present perfect is used for past actions 
with present relevance. Form: have/has + past participle.
Example: "I have lived in Madrid for 3 years."
Try it: Tell me something you have done in your life!
```

### Vocabulary (Vocabulario)

**Proposito**: Ensenar palabras nuevas con contexto.

**Como funciona**:
- LLM introduce palabras por tema
- Da ejemplo de uso
- Pide al estudiante que las use

**Ejemplo**:
```
Estudiante: Teach me food vocabulary
Mr. James: Lets learn food words! Here are 5 useful ones:
- "cuisine" = tipo de comida (Italian cuisine)
- "beverage" = bebida
- "dish" = plato
- "spicy" = picante
- "delicious" = delicioso
Make a sentence with one of these!
```

### Quiz (Cuestionario)

**Proposito**: Evaluar conocimiento con preguntas.

**Como funciona**:
- LLM genera preguntas segun nivel
- Preguntas de opcion multiple o completar
- Da feedback inmediato

**Ejemplo**:
```
Mr. James: Quiz time! Choose the correct option:
"She ___ to the gym every day."
a) go
b) goes  <- Correct!
c) going
d) gone

You got it right! Great job!
```

### Pronunciation (Pronunciacion)

**Proposito**: Practicar pronunciacion de frases.

**Como funciona**:
- LLM da una frase para repetir
- Estudiante la repite (en chat)
- LLM da tips de pronunciacion

**Ejemplo**:
```
Mr. James: Repeat this: "The weather is wonderful today."
Tip: "weather" sounds like "WEH-ther", not "WEE-ther".
Try another: "She sells seashells by the seashore."
```

---

## 8. Niveles CEFR

El sistema sigue el **Marco Comun Europeo de Referencia (CEFR)** con 6 niveles:

### A1 - Beginner (Principiante)
- **Vocabulario**: ~500 palabras
- **Tiempos**: Present simple, present continuous
- **Puede**: Saludar, presentarse, hablar de rutina

### A2 - Elementary (Elemental)
- **Vocabulario**: ~1000 palabras
- **Tiempos**: Pasado simple, futuro (going to)
- **Puede**: Hablar de eventos pasados, hacer planes

### B1 - Intermediate (Intermedio)
- **Vocabulario**: ~2000 palabras
- **Tiempos**: Presente perfecto, condicionales tipo 1
- **Puede**: Expresar opiniones, contar experiencias

### B2 - Upper-Intermediate
- **Vocabulario**: ~4000 palabras
- **Tiempos**: Condicionales 1-3, pasiva, reported speech
- **Puede**: Discutir temas abstractos, escribir ensayos

### C1 - Advanced (Avanzado)
- **Vocabulario**: ~6000+ palabras
- **Tiempos**: Modales perfectos, mix avanzado
- **Puede**: Escribir academicamente, debatir

### C2 - Proficiency (Maestria)
- **Vocabulario**: 8000+ palabras
- **Tiempos**: Dominio total
- **Puede**: Dominio casi nativo

Como elegir el nivel correcto?:
- **No se nada**: A1
- **Se frases basicas**: A2
- **Puedo conversar en temas diarios**: B1
- **Me defiendo en viajes/trabajo**: B2
- **Leo libros sin mucho diccionario**: C1
- **Hablo casi como nativo**: C2


---

## 9. API Reference

Todos los endpoints devuelven JSON.

### GET /

Retorna la interfaz HTML del chat.

**Respuesta**: HTML

---

### POST /api/chat

Endpoint principal del chat. Acepta dos tipos de input:

#### A) Mensaje de texto del estudiante
```json
{
  "message": "I want to learn grammar"
}
```

**Respuesta**:
```json
{
  "message": "Great! Let's talk about grammar...",
  "botones": [
    {"texto": "Change mode", "valor": "change_mode"},
    {"texto": "My progress", "valor": "progress"},
    {"texto": "End session", "valor": "goodbye"}
  ],
  "paso": "in_session"
}
```

#### B) Accion de boton
```json
{
  "action": "B1"
}
```

**Valores de action**:
- `init` - Iniciar conversacion
- `A1`, `A2`, `B1`, `B2`, `C1`, `C2` - Seleccionar nivel
- `travel`, `work`, `studies`, `exams`, `entertainment`, `personal` - Objetivo
- `conversation`, `grammar`, `vocabulary`, `quiz`, `pronunciation` - Modo
- `change_mode` - Cambiar modo
- `progress` - Ver progreso
- `goodbye` - Terminar sesion

**Respuesta**: Similar a (A) con el siguiente paso del flujo.

---

### POST /api/speak

Genera audio TTS en ingles.

**Request**:
```json
{
  "text": "Hello! How are you today?"
}
```

**Respuesta exitosa**:
```json
{
  "audioContent": "base64delAudio...",
  "audioUrl": "data:audio/mp3;base64,xxx",
  "useBrowserTTS": false,
  "engine": "edge-tts"
}
```

**Respuesta fallback** (si falla edge-tts):
```json
{
  "audioContent": null,
  "useBrowserTTS": true,
  "text": "Hello! How are you today?"
}
```

El frontend usa Web Speech API como fallback.

---

### GET /api/levels

Lista los niveles CEFR disponibles.

**Respuesta**:
```json
{
  "levels": ["A1", "A2", "B1", "B2", "C1", "C2"]
}
```

---

### GET /api/modes

Lista los modos de aprendizaje.

**Respuesta**:
```json
{
  "modes": [
    {
      "id": "conversation",
      "nombre": "Conversation",
      "emoji": "💬",
      "descripcion": "Free talk - practice speaking about any topic"
    },
    ...
  ]
}
```

---

### GET /api/voices

Lista las voces TTS disponibles.

**Respuesta**:
```json
{
  "voices": [
    {
      "id": "en-US-GuyNeural",
      "name": "Guy",
      "gender": "Male",
      "region": "US",
      "recommended": true
    },
    ...
  ],
  "current": "en-US-GuyNeural"
}
```

**Voces disponibles**:
- `en-US-GuyNeural` (M, US) - default
- `en-US-JennyNeural` (F, US)
- `en-US-DavisNeural` (M, US)
- `en-US-AriaNeural` (F, US)
- `en-GB-RyanNeural` (M, UK)
- `en-GB-SoniaNeural` (F, UK)
- `en-AU-WilliamNeural` (M, AU)

---

### GET /api/health

Health check del sistema.

**Respuesta**:
```json
{
  "status": "ok",
  "service": "EnglishAI Tutor",
  "version": "1.0",
  "rag_available": true,
  "gemini_configured": true,
  "openrouter_configured": true
}
```

---

### GET /api/pinecone-status

Estado del indice de Pinecone.

**Respuesta**:
```json
{
  "status": "ok",
  "index": "englishai-tutor",
  "dimension": 768,
  "total_vectors": 45
}
```

---

### GET /api/student

Informacion del estudiante actual (de la sesion).

**Respuesta**:
```json
{
  "student": {
    "nombre": "Carlos",
    "email": "",
    "nivel": "B1",
    "objetivo": "work",
    "modo_actual": "conversation",
    "paso_actual": "in_session",
    "registered": false
  }
}
```

---

### POST /api/reset

Reinicia la sesion del estudiante (limpia cookies).

**Respuesta**:
```json
{
  "message": "Session reset",
  "ok": true
}
```

---

## 10. Mantenimiento y operaciones

### Re-indexar conocimiento

Si modificas `conocimiento_ingles.md`:

```bash
python upload_knowledge.py
```

El script preguntara si desea eliminar lo anterior antes de subir.

### Ver logs

Los logs de Flask se muestran en consola. Para guardar:

```bash
python app.py > logs/app.log 2>&1
```

### Backup de Supabase

Desde el dashboard de Supabase:
1. Settings > Database
2. Backups > Create backup

O via CLI:
```bash
supabase db dump > backup.sql
```

### Monitoreo

Verifica regularmente:
- `/api/health` - estado general
- `/api/pinecone-status` - estado del RAG
- Logs de Flask - errores 500
- Dashboard de Supabase - uso de BD
- Dashboard de Pinecone - cuota

### Actualizar dependencias

```bash
pip install --upgrade -r requirements.txt
```

### Deploy en produccion (Heroku)

1. Crear app en Heroku
2. Agregar add-ons:
   - Heroku Postgres (o usar Supabase externo)
3. Set env vars:
   ```bash
   heroku config:set OPENROUTER_API_KEY=xxx
   heroku config:set PINECONE_API_KEY=xxx
   # etc
   ```
4. Push:
   ```bash
   git push heroku main
   ```

El `Procfile` ya esta configurado: `web: gunicorn app:app`

---

## 11. Personalizacion

### Cambiar la personalidad del profesor

Editar `app.py`, seccion `SYSTEM_PROMPT_BASE`. Ejemplo para hacerlo mas formal:

```python
SYSTEM_PROMPT_BASE = """You are Professor Smith, a formal academic English teacher...
- Always use "Mr./Ms." when addressing the student
- Use academic vocabulary
- Focus on formal writing style
..."""
```

### Cambiar la voz TTS por defecto

En `.env`:
```
TTS_VOICE=en-GB-RyanNeural
```

O listar las voces disponibles:
```bash
curl http://localhost:5000/api/voices
```

### Agregar mas modos de aprendizaje

1. En `guion.py`, agregar al dict `MODOS`:
```python
"writing": {
    "id": "writing",
    "nombre": "Writing",
    "emoji": "✍️",
    "descripcion": "Practice writing essays and emails"
}
```

2. En `index.html`, agregar boton en el array de `select_mode`

3. En `app.py`, agregar el modo al `SYSTEM_PROMPT_BASE`:
```
- Writing: Help with essays, emails, formal letters
```

### Cambiar el esquema de BD

Si necesitas campos adicionales (ej: `avatar_url`):

1. Agregar columna en Supabase:
```sql
ALTER TABLE estudiantes ADD COLUMN avatar_url TEXT;
```

2. Modificar `database.py > guardar_estudiante()`:
```python
registro = {
    ...
    "avatar_url": datos.get("avatar_url", ""),
}
```

3. Usar en el frontend

### Cambiar la base de conocimiento

Edita `conocimiento_ingles.md`. Estructura recomendada:
- Una seccion por tema
- Ejemplos claros
- Errores comunes marcados con ❌
- Formas correctas marcadas con ✅

Luego re-indexa:
```bash
python upload_knowledge.py
```

### Limitar el numero de mensajes

Por defecto no hay limite. Para agregar:

En `app.py`, agregar contador en sesion:
```python
if session.get("msg_count", 0) > 50:
    return jsonify({"message": "Session limit reached..."}), 429
session["msg_count"] = session.get("msg_count", 0) + 1
```

---

## 12. Solucion de problemas

### "GEMINI_API_KEY no configurada"

**Causa**: Falta API key en `.env`

**Solucion**:
1. Verificar que `.env` existe (no `.env.example`)
2. Verificar que tiene `GEMINI_API_KEY=AIzaSy...`
3. Reiniciar el servidor

### "Pinecone not connected"

**Causa**: API key invalida o sin internet

**Solucion**:
1. Verificar `PINECONE_API_KEY` en `.env`
2. Probar conexion: `curl https://api.pinecone.io`
3. Verificar que la key tenga permisos

### El bot responde muy lento

**Causa**: Modelo LLM muy grande o latencia de red

**Solucion**:
1. Usar un modelo mas rapido en `OPENROUTER_MODEL`:
   ```
   OPENROUTER_MODEL=mistralai/mistral-7b-instruct
   ```
2. Reducir `max_tokens` en `app.py` (default: 400)
3. Habilitar cache de respuestas

### "Supabase no disponible"

**Causa**: URL o key incorrectas

**Solucion**:
1. Verificar `SUPABASE_URL` (formato: `https://xxx.supabase.co`)
2. Verificar `SUPABASE_KEY` (key anon, no service_role)
3. Verificar que las tablas existen (ejecutar `schema_supabase.sql`)

### El audio TTS no suena

**Causa**: edge-tts no puede generar el audio

**Solucion**:
1. El sistema usa fallback automatico: Web Speech API del navegador
2. Si tampoco suena, verificar permisos de audio del navegador
3. Verificar que la voz existe: `edge-tts --list-voices`

### Error 500 en /api/chat

**Causa**: Error interno

**Solucion**:
1. Ver logs: aparecen en consola
2. Comunes:
   - LLM no responde (verificar API key)
   - Supabase no disponible (verificar conexion)
   - RAG falla (verificar Pinecone)
3. Test individual:
   ```bash
   curl http://localhost:5000/api/health
   ```

### El bot no entiende el nombre

**Causa**: Validacion muy estricta

**Solucion**:
- Nombres validos: "Maria", "John", "Ana Lucia"
- Nombres invalidos: "123", "x" (muy corto)
- Si el nombre tiene numeros, el sistema lo acepta igualmente
- Editar `validar_nombre` en `guion.py` para cambiar reglas

### Las sesiones no persisten

**Causa**: Cookies no se guardan o `SECRET_KEY` cambia

**Solucion**:
1. En desarrollo, verificar que el navegador acepta cookies
2. En produccion, HTTPS es obligatorio para cookies
3. No cambiar `SECRET_KEY` (rompe sesiones existentes)

### El bot se "olvida" del nivel

**Causa**: Sesion expirada o reinicio del servidor

**Solucion**:
- Las sesiones Flask usan cookies firmadas en el cliente
- Si el servidor reinicia, las sesiones siguen funcionando
- Si se cambia `SECRET_KEY`, todas las sesiones se invalidan
- Solucion permanente: guardar perfil en Supabase (campo `email`)

---

## Apendice A: Glosario de terminos tecnicos

| Termino | Significado |
|---|---|
| **API** | Application Programming Interface - forma de comunicar sistemas |
| **CEFR** | Common European Framework of Reference - niveles de idiomas |
| **Embedding** | Representacion numerica de texto para busqueda semantica |
| **Flask** | Framework web de Python |
| **LLM** | Large Language Model (modelo de lenguaje grande) |
| **Pinecone** | Base de datos vectorial |
| **RAG** | Retrieval-Augmented Generation - LLM + busqueda en BD |
| **Supabase** | Backend as a Service con PostgreSQL |
| **TTS** | Text-to-Speech (texto a voz) |
| **edge-tts** | Libreria para usar Microsoft TTS gratis |

---

## Apendice B: Comandos utiles

```bash
# Instalar
pip install -r requirements.txt

# Ejecutar desarrollo
python app.py

# Ejecutar produccion
gunicorn app:app --bind 0.0.0.0:5000 --workers 1

# Re-indexar conocimiento
python upload_knowledge.py

# Test rapido
curl http://localhost:5000/api/health

# Ver voces TTS
edge-tts --list-voices

# Limpiar cache Python
find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## Apendice C: Estructura de archivos

```
agentcallpingles-main/
+-- app.py                      # Flask app principal
+-- database.py                 # Cliente Supabase
+-- rag.py                      # RAG con Pinecone
+-- guion.py                    # Flujo conversacional
+-- upload_knowledge.py         # Indexador a Pinecone
+-- conocimiento_ingles.md      # Base de conocimiento
+-- schema_supabase.sql         # Schema de BD
+-- requirements.txt            # Dependencias
+-- .env.example                # Plantilla de env vars
+-- Procfile                    # Config Heroku
+-- runtime.txt                 # Version Python
+-- start.sh                    # Script de inicio
+-- README.md                   # README principal
+-- MANUAL.md                   # Este manual
+-- templates/
|   +-- index.html              # UI del chat
```

---

## Soporte y contacto

- **Documentacion tecnica**: `README.md`
- **Manual de usuario**: `MANUAL.md` (este archivo)
- **Logs**: Consola del servidor
- **Health check**: http://localhost:5000/api/health

---

**Version**: 1.0
**Ultima actualizacion**: 2026
**Licencia**: MIT
