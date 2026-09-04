-- ================================================
-- SCHEMA: Base de datos CodeAI Tutor - Ing. MOJICA
-- 7 niveles de programación: INICIO, NOVATO, APRENDIZ, TECNICO, TECNOLOGO, INGENIERO, INGENIERO_IA
-- Supabase (PostgreSQL)
-- Ejecutar en SQL Editor de Supabase Dashboard
-- ================================================

-- Tabla: estudiantes
CREATE TABLE IF NOT EXISTS estudiantes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    nivel TEXT DEFAULT ''INICIO'' CHECK (nivel IN (''INICIO'',''NOVATO'',''APRENDIZ'',''TECNICO'',''TECNOLOGO'',''INGENIERO'',''INGENIERO_IA'')),
    idioma_nativo TEXT DEFAULT ''es'',
    objetivo TEXT,
    modo_actual TEXT,
    paso_actual TEXT DEFAULT ''welcome'',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: conversaciones
CREATE TABLE IF NOT EXISTS conversaciones (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    estudiante_email TEXT,
    estudiante_nombre TEXT,
    mensaje_usuario TEXT,
    respuesta_agente TEXT,
    modo TEXT DEFAULT ''conceptos'',
    nivel TEXT DEFAULT ''INICIO'',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: lecciones_completadas
CREATE TABLE IF NOT EXISTS lecciones_completadas (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    estudiante_email TEXT NOT NULL,
    tema TEXT NOT NULL,
    nivel TEXT DEFAULT ''INICIO'',
    score INTEGER DEFAULT 0,
    modo TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: vocabulario_aprendido
CREATE TABLE IF NOT EXISTS vocabulario_aprendido (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    estudiante_email TEXT NOT NULL,
    palabra TEXT NOT NULL,
    traduccion TEXT,
    nivel TEXT DEFAULT ''INICIO'',
    ejemplo TEXT,
    repasos INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: errores_estudiante
CREATE TABLE IF NOT EXISTS errores_estudiante (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    estudiante_email TEXT NOT NULL,
    error TEXT NOT NULL,
    correccion TEXT,
    tema TEXT,
    nivel TEXT DEFAULT ''INICIO'',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indices
CREATE INDEX IF NOT EXISTS idx_estudiantes_email ON estudiantes(email);
CREATE INDEX IF NOT EXISTS idx_conversaciones_email ON conversaciones(estudiante_email);
CREATE INDEX IF NOT EXISTS idx_conversaciones_created ON conversaciones(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_lecciones_email ON lecciones_completadas(estudiante_email);
CREATE INDEX IF NOT EXISTS idx_vocabulario_email ON vocabulario_aprendido(estudiante_email);
CREATE INDEX IF NOT EXISTS idx_errores_email ON errores_estudiante(estudiante_email);

-- Vista: progreso del estudiante
CREATE OR REPLACE VIEW vista_progreso_estudiante AS
SELECT
    e.email,
    e.nombre,
    e.nivel,
    COUNT(DISTINCT l.id) AS lecciones_completadas,
    COUNT(DISTINCT v.id) AS palabras_aprendidas,
    COUNT(DISTINCT er.id) AS errores_totales
FROM estudiantes e
LEFT JOIN lecciones_completadas l ON l.estudiante_email = e.email
LEFT JOIN vocabulario_aprendido v ON v.estudiante_email = e.email
LEFT JOIN errores_estudiante er ON er.estudiante_email = e.email
GROUP BY e.email, e.nombre, e.nivel;

-- Vista de estadisticas globales
CREATE OR REPLACE VIEW vista_estadisticas AS
SELECT
    (SELECT COUNT(*) FROM estudiantes) AS total_estudiantes,
    (SELECT COUNT(*) FROM conversaciones) AS total_conversaciones,
    (SELECT COUNT(*) FROM lecciones_completadas) AS total_lecciones,
    (SELECT COUNT(*) FROM vocabulario_aprendido) AS total_vocabulario;

-- ================================================
-- FIN DEL SCHEMA
-- ================================================
