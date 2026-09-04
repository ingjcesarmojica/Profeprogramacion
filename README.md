# CodeAI Tutor - Ing. MOJICA

> Tutor de Programación con IA en español, disponible 24/7. Enseña desde cero absoluto hasta Ingeniería de IA.

Un agente profesor de programación construido con Flask, Pinecone RAG, Supabase, edge-tts y OpenRouter/Gemini. **Ing. MOJICA** enseña programación a hispanohablantes con clases personalizadas, ejercicios prácticos, proyectos guiados, quizzes interactivos y soporte para los 7 niveles de aprendizaje (desde principiantes sin experiencia hasta ingenieros especializados en IA).

## Features

- **6 Modos de Aprendizaje**: Conceptos, Práctica, Proyectos, Quiz, Código, IA
- **7 Niveles de Programación**: INICIO, NOVATO, APRENDIZ, TÉCNICO, TECNÓLOGO, INGENIERO, INGENIERO DE IA
- **Enseñanza adaptativa**: Ajusta el lenguaje y la profundidad al nivel del estudiante
- **RAG (base de conocimiento)**: Pinecone + embeddings Gemini
- **Text-to-Speech en español**: Voces neurales de Microsoft vía edge-tts
- **Seguimiento de progreso**: Lecciones, conceptos y errores en Supabase
- **100% en español**: Interfaz, system prompt, mensajes y validaciones
- **Rutas de aprendizaje personalizadas** según objetivo del estudiante

## Los 7 Niveles de Enseñanza

| Nivel | Emoji | Descripción |
|-------|-------|-------------|
| **INICIO** | 🌱 | Sin experiencia previa, primer contacto con la programación |
| **NOVATO** | 🐣 | Conceptos básicos, primer lenguaje (recomendado: Python) |
| **APRENDIZ** | 📚 | Estructuras de control, funciones, POO inicial, Git |
| **TÉCNICO** | 🛠️ | Frameworks, SQL, APIs REST, testing, desarrollo web/móvil |
| **TECNÓLOGO** | 🎓 | Patrones de diseño, microservicios, Docker, CI/CD, cloud |
| **INGENIERO** | 🏗️ | Sistemas distribuidos, Kubernetes, SOLID, observabilidad, seguridad |
| **INGENIERO DE IA** | 🤖 | Machine Learning, Deep Learning, LLMs, MLOps, ética en IA |

## Los 6 Modos de Aprendizaje

| Modo | Emoji | Descripción |
|------|-------|-------------|
| **Conceptos** | 💡 | Teoría con ejemplos claros y analogías cotidianas |
| **Práctica** | ⌨️ | Ejercicios paso a paso para afianzar conocimientos |
| **Proyectos** | 🚀 | Proyectos reales guiados de principio a fin |
| **Quiz** | 🎯 | Preguntas interactivas para evaluar tu nivel |
| **Código** | 🧩 | Reviso, explico y depuro el código que envíes |
| **IA** | 🤖 | Contenido especializado en inteligencia artificial |

## Tech Stack

- **Backend**: Flask 3.x
- **LLM**: OpenRouter (default) + Gemini (fallback)
- **Vector DB**: Pinecone (RAG)
- **Database**: Supabase (PostgreSQL)
- **TTS**: edge-tts (voces neurales en español)
- **Embeddings**: Gemini embedding-001
- **Deploy**: Gunicorn (Heroku-ready vía Procfile)

## Project Structure

```
agentcallprogramacion-main/
+- app.py                       # Flask app con rutas y system prompt
+- database.py                  # Cliente Supabase y queries
+- rag.py                       # RAG con Pinecone + embeddings
+- guion.py                     # Flujo conversacional y validadores (7 niveles, 6 modos)
+- upload_knowledge.py          # Indexa la base de conocimiento a Pinecone
+- conocimiento_programacion.md # Base de conocimiento en español
+- schema_supabase.sql          # Schema de BD (CHECK para 7 niveles)
+- requirements.txt             # Dependencias Python
+- .env.example                 # Template de variables de entorno
+- Procfile                     # Deploy Heroku
+- start.sh                     # Script de arranque
+- runtime.txt                  # Versión de Python
+- MANUAL.md                    # Manual de uso detallado
+- templates/
   +- index.html                # Chat UI (español)
```

## Setup

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copia `.env.example` a `.env` y completa los valores:

```bash
cp .env.example .env
```

Necesitas:
- `OPENROUTER_API_KEY` o `GEMINI_API_KEY` (LLM)
- `PINECONE_API_KEY` (RAG)
- `SUPABASE_URL` y `SUPABASE_KEY` (base de datos)
- `TTS_VOICE` (default: `es-ES-ElviraNeural`)

### 3. Crear las tablas en la base de datos

Ejecuta el SQL en `schema_supabase.sql` desde el SQL Editor de Supabase.

El schema valida que el nivel del estudiante pertenezca a los 7 valores permitidos:
`INICIO`, `NOVATO`, `APRENDIZ`, `TECNICO`, `TECNOLOGO`, `INGENIERO`, `INGENIERO_IA`.

Si ya tienes una base de datos con el schema antiguo, actualiza el CHECK:

```sql
ALTER TABLE estudiantes DROP CONSTRAINT IF EXISTS estudiantes_nivel_check;
ALTER TABLE estudiantes ADD CONSTRAINT estudiantes_nivel_check
  CHECK (nivel IN ('INICIO','NOVATO','APRENDIZ','TECNICO','TECNOLOGO','INGENIERO','INGENIERO_IA'));
```

### 4. Indexar la base de conocimiento

```bash
python upload_knowledge.py
```

Esto sube `conocimiento_programacion.md` a Pinecone para alimentar el RAG.

### 5. Ejecutar localmente

```bash
python app.py
```

Abre http://localhost:5000 y verás al **Ing. MOJICA** listo para enseñar.

## Flujo de la Conversación

1. **Welcome** - El Ing. MOJICA saluda al estudiante
2. **Ask name** - El estudiante proporciona su nombre
3. **Ask level** - Elige uno de los 7 niveles (INICIO → INGENIERO_IA)
4. **Ask goal** - ¿Cuál es tu objetivo? (trabajo, estudios, IA, web, videojuegos, etc.)
5. **Select mode** - Elige uno de los 6 modos (Conceptos, Práctica, Proyectos, Quiz, Código, IA)
6. **In session** - Práctica libre con el LLM adaptado al nivel
7. **Change mode** - Cambia de modo en cualquier momento
8. **Mi progreso** - Ve tus lecciones, conceptos y errores registrados
9. **Goodbye** - Finaliza la sesión

## API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Chat UI |
| `/api/chat` | POST | Chat principal (message o action) |
| `/api/speak` | POST | Generación de audio TTS en español |
| `/api/levels` | GET | 7 niveles de programación |
| `/api/modes` | GET | 6 modos de aprendizaje |
| `/api/voices` | GET | Voces TTS disponibles en español |
| `/api/health` | GET | Health check del servicio |
| `/api/pinecone-status` | GET | Estadísticas del índice Pinecone |
| `/api/student` | GET | Información del estudiante actual |
| `/api/reset` | POST | Reinicia la sesión |

## Voces TTS Disponibles (Español)

- `es-MX-JorgeNeural` (M, México) - default (acento latino)
- `es-MX-DaliaNeural` (F, México)
- `es-CO-GonzaloNeural` (M, Colombia)
- `es-CO-SalomeNeural` (F, Colombia)
- `es-AR-TomasNeural` (M, Argentina)
- `es-AR-ElenaNeural` (F, Argentina)
- `es-ES-AlvaroNeural` (M, España)
- `es-ES-ElviraNeural` (F, España)

## Objetivos Soportados

- 💼 Trabajar como desarrollador
- 🎓 Estudios / Universidad
- 🚀 Crear mi propio proyecto / emprendimiento
- 🤖 Aprender Inteligencia Artificial
- 🌐 Desarrollo web
- 🎮 Crear videojuegos
- 📊 Análisis de datos
- 🧑‍💻 Curiosidad / Hobby

## Licencia

MIT

## Créditos

Construido para hispanohablantes que quieren aprender programación. El Ing. MOJICA es paciente, motivador y eficaz: enseña desde cero hasta Ingeniería de IA con clases personalizadas las 24 horas, los 7 días de la semana.

