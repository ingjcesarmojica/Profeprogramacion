# EnglishAI Tutor - Mr. James

> AI-powered English teacher for Spanish speakers, available 24/7.

An intelligent English tutor agent built with Flask, Pinecone RAG, Supabase, edge-tts, and OpenRouter/Gemini. Mr. James teaches English to Spanish speakers with personalized classes, conversation practice, grammar lessons, vocabulary, quizzes, and pronunciation drills.

## Features

- **5 Learning Modes**: Conversation, Grammar, Vocabulary, Quiz, Pronunciation
- **6 CEFR Levels**: A1, A2, B1, B2, C1, C2
- **Adaptive teaching**: Adjusts to student level
- **RAG knowledge base**: Pinecone + Gemini embeddings
- **Text-to-speech**: English voices via edge-tts
- **Progress tracking**: Lessons, vocabulary, mistakes in Supabase
- **Spanish-aware**: Knows common Spanish-speaker mistakes
- **Bilingual explanations**: Uses Spanish only when needed

## Tech Stack

- **Backend**: Flask 3.x
- **LLM**: OpenRouter (default) + Gemini (fallback)
- **Vector DB**: Pinecone (RAG)
- **Database**: Supabase (PostgreSQL)
- **TTS**: edge-tts (Microsoft neural voices)
- **Embeddings**: Gemini embedding-001
- **Deploy**: Gunicorn (Heroku-ready via Procfile)

## Project Structure

```
agentcallpingles-main/
+- app.py                      # Flask app with routes
+- database.py                 # Supabase client & queries
+- rag.py                      # Pinecone RAG + embeddings
+- guion.py                    # Conversation flow & validators
+- upload_knowledge.py         # Index knowledge base to Pinecone
+- conocimiento_ingles.md      # Knowledge base (markdown)
+- schema_supabase.sql         # Database schema
+- requirements.txt            # Python dependencies
+- .env.example                # Environment variables template
+- Procfile                    # Heroku deploy
+- start.sh                    # Startup script
+- runtime.txt                 # Python version
+- templates/
   +- index.html               # Chat UI
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in the values:

```bash
cp .env.example .env
```

You need:
- `OPENROUTER_API_KEY` or `GEMINI_API_KEY` (LLM)
- `PINECONE_API_KEY` (RAG)
- `SUPABASE_URL` and `SUPABASE_KEY` (database)
- `TTS_VOICE` (default: `en-US-GuyNeural`)

### 3. Create database tables

Run the SQL in `schema_supabase.sql` in your Supabase SQL editor.

### 4. Index the knowledge base

```bash
python upload_knowledge.py
```

This uploads `conocimiento_ingles.md` to Pinecone.

### 5. Run locally

```bash
python app.py
```

Open http://localhost:5000

## Conversation Flow

1. **Welcome** - Mr. James greets the student
2. **Ask name** - Student provides their name
3. **Ask level** - Choose CEFR level (A1-C2)
4. **Ask goal** - Why are you learning English? (travel/work/studies/etc.)
5. **Select mode** - Choose practice mode
6. **In session** - Free practice with LLM
7. **Change mode** - Switch between modes anytime
8. **Goodbye** - End session

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Chat UI |
| `/api/chat` | POST | Main chat (message or action) |
| `/api/speak` | POST | TTS audio generation |
| `/api/levels` | GET | Available CEFR levels |
| `/api/modes` | GET | Available learning modes |
| `/api/voices` | GET | Available TTS voices |
| `/api/health` | GET | Health check |
| `/api/pinecone-status` | GET | Pinecone index stats |
| `/api/student` | GET | Current student info |
| `/api/reset` | POST | Reset session |

## Available TTS Voices (English)

- `en-US-GuyNeural` (M, US) - default
- `en-US-JennyNeural` (F, US)
- `en-US-DavisNeural` (M, US)
- `en-US-AriaNeural` (F, US)
- `en-GB-RyanNeural` (M, UK)
- `en-GB-SoniaNeural` (F, UK)
- `en-AU-WilliamNeural` (M, AU)

## License

MIT

## Credits

Built for Spanish speakers learning English, by an AI tutoring system designed to be patient, encouraging, and effective.
