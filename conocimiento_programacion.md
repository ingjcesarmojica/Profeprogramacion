# Base de Conocimiento - Ing. MOJICA
## Documento de Referencia para el Agente Profesor de Programación

---

## 1. SOBRE CODEAI TUTOR - ING. MOJICA

### ¿Qué es CodeAI Tutor?
CodeAI Tutor es un profesor virtual de programación disponible 24 horas, 7 días a la semana. Utiliza Inteligencia Artificial avanzada para brindar clases personalizadas a hispanohablantes que desean aprender a programar, desde cero absoluto hasta el nivel de Ingeniero de IA. Ofrece práctica de conceptos, ejercicios paso a paso, proyectos guiados, quizzes interactivos, ayuda con código y contenido especializado en inteligencia artificial.

### Nuestra misión
Hacer que la programación sea accesible, personalizada y efectiva para todos los hispanohablantes, sin importar su nivel inicial. El Ing. MOJICA es un mentor paciente, motivador y didáctico que celebra cada logro y nunca juzga los errores.

### Diferenciadores
- Disponible 24/7 - estudias cuando quieras
- 100% en español - interfaz, explicaciones y mensajes
- 7 niveles de aprendizaje - desde cero hasta Ingeniería de IA
- 6 modos de aprendizaje adaptados a diferentes estilos
- Rutas personalizadas según el objetivo del estudiante (trabajo, IA, web, videojuegos, etc.)
- Corrección constructiva con feedback pedagógico
- Explicaciones claras con analogías de la vida cotidiana
- Ejemplos de código en cualquier lenguaje popular

---

## 2. EL PROFESOR: BYTE

### Perfil
- **Nombre**: Ing. MOJICA
- **Nacionalidad**: Digital, originario de Internet
- **Idiomas**: Español nativo (también entiende términos técnicos en inglés)
- **Personalidad**: Amable, paciente, motivador, didáctico. Como un mentor que adora enseñar.

### Valores pedagógicos
- Cada error es una oportunidad de aprendizaje
- Las analogías simples son la mejor forma de explicar conceptos complejos
- La práctica constante es la clave para dominar la programación
- Cada estudiante tiene su propio ritmo y merece respeto
- Celebrar los pequeños logros motiva el aprendizaje continuo

---

## 3. CURRÍCULO DE LOS 7 NIVELES

### 3.1 NIVEL INICIO (sin experiencia previa)

**Objetivo**: Introducir al estudiante al mundo de la programación, desarrollar pensamiento lógico y algorítmico.

#### Temas clave
- ¿Qué es programar? Programar es dar instrucciones a una computadora
- Pensamiento computacional: descomposición, patrones, abstracción, algoritmos
- ¿Qué es un lenguaje de programación?
- ¿Qué es Python y por qué es ideal para empezar?
- Instalación de Python y un editor (VS Code)
- Tu primer programa: `print("¡Hola, mundo!")`
- Variables: imagina que son una caja con una etiqueta
- Tipos de datos básicos: números enteros (int), decimales (float), texto (str)
- Operadores aritméticos: +, -, *, /, // (división entera), % (módulo), ** (potencia)
- Operadores de comparación: ==, !=, <, >, <=, >=

#### Ejemplo de código (INICIO)
```python
# Mi primer programa
nombre = input("¿Cómo te llamas? ")
print("¡Hola,", nombre, "! Bienvenido al mundo de la programación.")
```

#### Conceptos a reforzar
- Un programa se ejecuta línea por línea, de arriba hacia abajo
- Python distingue entre mayúsculas y minúsculas
- Los comentarios empiezan con `#` y no se ejecutan

---

### 3.2 NIVEL NOVATO (primer lenguaje)

**Objetivo**: Que el estudiante domine los fundamentos de un primer lenguaje y pueda escribir programas simples.

#### Temas clave
- Tipos de datos: int, float, str, bool (True/False)
- Entrada y salida de datos: `input()`, `print()`
- Conversión de tipos: `int()`, `float()`, `str()`
- Operadores lógicos: `and`, `or`, `not`
- Condicionales: `if`, `elif`, `else`
- Bucles: `for` (para iterar sobre una secuencia), `while` (mientras se cumpla una condición)
- Listas: `[1, 2, 3]`, acceder por índice, `append()`, `len()`
- Tuplas: similares a las listas pero inmutables `(1, 2, 3)`
- Diccionarios: `{"clave": "valor"}`
- Funciones básicas: `def mi_funcion():`
- Manejo de strings: concatenación, f-strings (`f"Hola {nombre}"`)
- Importación de módulos: `import math`, `import random`

#### Ejemplo de código (NOVATO)
```python
# Adivina el número
import random
numero_secreto = random.randint(1, 10)
intento = int(input("Adivina el número (1-10): "))
if intento == numero_secreto:
    print("¡Excelente! Adivinaste.")
elif intento < numero_secreto:
    print("El número es mayor.")
else:
    print("El número es menor.")
```

#### Buenas prácticas
- Nombres de variables descriptivos: `edad_usuario` en vez de `x`
- Indentación consistente (4 espacios en Python)
- Comentarios para explicar el "por qué", no el "qué"

PLACEHOLDER_PART2
### 3.3 NIVEL APRENDIZ (estructuras y POO inicial)

**Objetivo**: Que el estudiante domine estructuras de control avanzadas, funciones y los fundamentos de la Programación Orientada a Objetos.

#### Temas clave
- Funciones avanzadas: parámetros, argumentos, `return`, valores por defecto, `*args`, `**kwargs`
- Alcance de variables: local vs global
- Listas por comprensión: `[x*2 for x in range(10)]`
- Diccionarios anidados y listas de diccionarios
- Manejo de excepciones: `try`, `except`, `finally`, `raise`
- Archivos: leer y escribir con `open()`, `with`
- Módulos y paquetes: `import`, `from ... import`
- Programación Orientada a Objetos (POO):
  - Clases y objetos
  - Atributos y métodos
  - El método `__init__` (constructor)
  - `self` y la referencia al objeto actual
  - Herencia: clases padre y subclases
  - Encapsulamiento: atributos públicos y privados (con `_` o `__`)
  - Polimorfismo: mismo método, diferente comportamiento
- Git y GitHub: comandos básicos (`git init`, `git add`, `git commit`, `git push`)

#### Ejemplo de código (APRENDIZ)
```python
class Perro:
    def __init__(self, nombre, raza):
        self.nombre = nombre
        self.raza = raza
        self.energia = 100

    def ladrar(self):
        print(f"{self.nombre} dice: ¡Guau!")

    def correr(self, minutos):
        self.energia -= minutos * 2
        print(f"{self.nombre} corrió {minutos} min. Energía: {self.energia}")

mi_perro = Perro("Firulais", "Labrador")
mi_perro.ladrar()
mi_perro.correr(10)
```

#### Buenas prácticas
- DRY: Don't Repeat Yourself (no repetir código)
- Una función debe hacer una sola cosa bien hecha
- Clases para modelar entidades del mundo real
- Hacer commits pequeños y descriptivos en Git

---

### 3.4 NIVEL TÉCNICO (frameworks, bases de datos, desarrollo web/móvil)

**Objetivo**: Que el estudiante aprenda a usar frameworks, bases de datos, APIs y empiece a crear aplicaciones web o móviles.

#### Temas clave
- HTML5, CSS3 y JavaScript (ES6+): fundamentos
  - DOM, eventos, fetch API
- Un framework frontend (recomendado: React)
  - Componentes, props, estado (useState), efectos (useEffect)
  - JSX, hooks, routing
- Un framework backend (Node.js/Express, Python/Django/Flask, Java/Spring)
  - Rutas, middlewares, controladores
  - Manejo de peticiones HTTP (GET, POST, PUT, DELETE)
- SQL y bases de datos relacionales (PostgreSQL, MySQL)
  - CREATE, SELECT, INSERT, UPDATE, DELETE
  - JOIN, GROUP BY, índices
- ORMs: SQLAlchemy, Prisma, Sequelize
- APIs REST: principios, autenticación con tokens
- Testing unitario: pytest, Jest, JUnit
- Control de versiones avanzado: branches, merge, rebase, pull requests
- Desarrollo móvil: Flutter (Dart), React Native, Swift (iOS), Kotlin (Android)

#### Ejemplo de código (TÉCNICO)
```python
# API REST con Flask
from flask import Flask, jsonify, request
app = Flask(__name__)
tareas = []

@app.route('/tareas', methods=['GET'])
def listar_tareas():
    return jsonify(tareas)

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    tarea = request.json
    tareas.append(tarea)
    return jsonify(tarea), 201

if __name__ == '__main__':
    app.run(debug=True)
```

#### Buenas prácticas
- Separación de responsabilidades: modelo, vista, controlador (MVC)
- Validar siempre las entradas del usuario
- Escribir tests desde el inicio (TDD)
- Usar variables de entorno para credenciales
- Documentar endpoints con OpenAPI/Swagger

PLACEHOLDER_PART3
### 3.5 NIVEL TECNÓLOGO (arquitectura, APIs, despliegue)

**Objetivo**: Que el estudiante entienda patrones de diseño, arquitecturas de software y despliegue en la nube.

#### Temas clave
- Patrones de diseño:
  - Creacionales: Singleton, Factory, Builder
  - Estructurales: Adapter, Decorator, Facade
  - De comportamiento: Observer, Strategy, State
- Arquitectura de software:
  - Monolito vs microservicios
  - MVC, MVVM, Clean Architecture
  - Event-Driven Architecture
- Contenedores: Docker, Docker Compose
- Orquestación básica: Docker Swarm
- CI/CD: GitHub Actions, GitLab CI, Jenkins
- Despliegue en la nube:
  - AWS: EC2, S3, RDS, Lambda
  - GCP: App Engine, Cloud Run, Cloud SQL
  - Azure: App Service, Functions
  - PaaS: Heroku, Vercel, Render, Railway
- Bases de datos NoSQL: MongoDB, Redis, Cassandra
- WebSockets para comunicación en tiempo real
- GraphQL como alternativa a REST
- Mensajería asíncrona: colas, pub/sub

#### Ejemplo de código (TECNÓLOGO)
```dockerfile
# Dockerfile para una aplicación Python
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/miapp
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=pass
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

#### Buenas prácticas
- 12-Factor App: configuración, dependencias, procesos, port binding
- Infrastructure as Code: Terraform, Pulumi
- Logs centralizados: ELK Stack, Loki
- Health checks y readiness probes

---

### 3.6 NIVEL INGENIERO (sistemas distribuidos, DevOps, buenas prácticas)

**Objetivo**: Que el estudiante domine sistemas distribuidos, orquestación avanzada, seguridad y principios de diseño sólidos.

#### Temas clave
- Sistemas distribuidos:
  - Teorema CAP (Consistency, Availability, Partition tolerance)
  - Message brokers: Apache Kafka, RabbitMQ
  - Servicios gRPC
- Orquestación de contenedores: Kubernetes (K8s)
  - Pods, deployments, services, ingress
  - Helm charts
  - kubectl, minikube, managed K8s (EKS, GKE, AKS)
- Principios de diseño:
  - SOLID (Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion)
  - DRY, KISS, YAGNI
  - Clean Code de Robert C. Martin
- Arquitectura hexagonal (Ports and Adapters)
- Domain-Driven Design (DDD): bounded contexts, agregados, value objects
- Event Sourcing y CQRS
- Observabilidad:
  - Logging estructurado
  - Métricas con Prometheus
  - Dashboards con Grafana
  - Tracing distribuido con Jaeger o Zipkin
- Seguridad:
  - OWASP Top 10
  - HTTPS, certificados, Let's Encrypt
  - Autenticación: OAuth2, JWT, OpenID Connect
  - Hashing: bcrypt, Argon2
  - Inyección SQL, XSS, CSRF
- Performance: caching, load balancing, CDN
- Chaos engineering: probar la resiliencia del sistema

#### Buenas prácticas (INGENIERO)
- Refactorización continua: el código viejo se mejora, no se reemplaza
- Code reviews constructivos y respetuosos
- Pair programming y mob programming
- Documentación: ADRs (Architecture Decision Records)
- Postmortems sin culpa cuando hay incidentes

PLACEHOLDER_PART4
### 3.7 NIVEL INGENIERO DE IA (machine learning, deep learning, MLOps)

**Objetivo**: Que el estudiante domine el ciclo completo de un proyecto de IA, desde las matemáticas subyacentes hasta el despliegue y monitoreo de modelos en producción.

#### Temas clave - Matemáticas para IA
- Álgebra lineal: vectores, matrices, transformaciones
- Cálculo: derivadas, gradientes, regla de la cadena
- Probabilidad y estadística: distribuciones, Bayes, hipótesis
- Optimización: gradient descent, Adam, learning rate

#### Machine Learning clásico
- Tipos de aprendizaje: supervisado, no supervisado, por refuerzo
- Regresión: lineal, polinómica, ridge, lasso
- Clasificación: logística, SVM, árboles de decisión, random forest
- Clustering: k-means, DBSCAN, jerárquico
- Métricas: accuracy, precision, recall, F1, ROC-AUC
- Feature engineering y selección
- scikit-learn: el caballito de batalla de ML en Python
- Validación cruzada, overfitting, underfitting

#### Deep Learning
- Redes neuronales artificiales: perceptrón, capas, funciones de activación
- Backpropagation y gradient descent
- Frameworks: PyTorch (recomendado), TensorFlow, JAX
- Redes convolucionales (CNN) para imágenes
- Redes recurrentes (RNN, LSTM, GRU) para secuencias
- Transformers y atención: la arquitectura detrás de los LLMs
- GANs (Generative Adversarial Networks)
- Transfer learning y fine-tuning

#### Large Language Models (LLMs)
- Prompt engineering: zero-shot, few-shot, chain-of-thought
- Modelos populares: GPT, Claude, Llama, Mistral, Gemini
- RAG (Retrieval-Augmented Generation): combinar LLMs con bases de conocimiento
- Fine-tuning: LoRA, QLoRA, PEFT
- Agentes de IA: ReAct, function calling, herramientas
- Hugging Face: el GitHub de los modelos de IA

#### MLOps (Machine Learning Operations)
- Versionado de datos: DVC, Delta Lake
- Versionado de modelos: MLflow, DVC
- Pipelines: Kubeflow, Airflow, Prefect
- Deployment de modelos:
  - APIs con FastAPI o TorchServe
  - Modelos en el edge con ONNX, TensorRT
- Monitoreo en producción: drift detection, A/B testing
- Costos y eficiencia: cuantización, pruning, distillation

#### Ética en IA
- Sesgos algorítmicos: cómo detectarlos y mitigarlos
- Interpretabilidad: SHAP, LIME
- Privacidad: differential privacy, federated learning
- Regulación: GDPR, AI Act de la UE
- Uso responsable y transparencia

#### Ejemplo de código (INGENIERO DE IA)
```python
# Clasificación con scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd

# Cargar datos
df = pd.read_csv('datos.csv')
X = df.drop('target', axis=1)
y = df['target']

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entrenar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Evaluar
predicciones = modelo.predict(X_test)
print(classification_report(y_test, predicciones))
```

#### Buenas prácticas (INGENIERO DE IA)
- Empezar simple: baseline antes que modelos complejos
- Validar siempre con datos que el modelo no ha visto
- Documentar experimentos: qué se probó, qué funcionó, qué no
- Considerar el impacto social y ético desde el diseño
- Monitorear modelos en producción, no son "fire and forget"

---

PLACEHOLDER_PART4B
## 4. LENGUAJES POPULARES Y CUÁNDO USARLOS

| Lenguaje | Ideal para | Nivel recomendado |
|----------|------------|-------------------|
| **Python** | Principiantes, IA, ciencia de datos, scripting | INICIO → INGENIERO_IA |
| **JavaScript** | Web frontend y backend (Node.js), apps móviles | APRENDIZ → INGENIERO |
| **TypeScript** | JavaScript con tipos, proyectos grandes | TÉCNICO → INGENIERO |
| **Java** | Aplicaciones empresariales, Android | APRENDIZ → INGENIERO |
| **C#** | .NET, videojuegos con Unity | APRENDIZ → INGENIERO |
| **C++** | Sistemas, videojuegos de alto rendimiento, embebidos | APRENDIZ → INGENIERO |
| **Go** | Microservicios, infraestructura, cloud | TÉCNICO → INGENIERO |
| **Rust** | Sistemas seguros, alto rendimiento, WebAssembly | TÉCNICO → INGENIERO |
| **PHP** | Desarrollo web tradicional (WordPress, Laravel) | APRENDIZ → TÉCNICO |
| **Ruby** | Startups, web con Rails | APRENDIZ → TÉCNICO |
| **Swift** | Apps iOS y macOS | APRENDIZ → TÉCNICO |
| **Kotlin** | Apps Android, backend | APRENDIZ → INGENIERO |
| **Dart** | Flutter (apps móviles y web multiplataforma) | APRENDIZ → TÉCNICO |
| **SQL** | Bases de datos (no es un lenguaje de programación, pero esencial) | NOVATO → INGENIERO |

---

## 5. RECURSOS RECOMENDADOS

### Para aprender
- **freeCodeCamp**: cursos gratuitos en español e inglés
- **Codecademy**: interactivo, ideal para principiantes
- **Coursera / edX**: cursos universitarios (Andrew Ng, MIT, Stanford)
- **Udemy**: cursos pagos accesibles (Maximilian Schwarzmüller, etc.)
- **YouTube**: canales como MoureDev, HolaMundo, Fazt, Código Facilito
- **Documentación oficial**: el mejor recurso siempre es la doc oficial del lenguaje/framework

### Para practicar
- **LeetCode**: algoritmos y estructuras de datos (preparación para entrevistas)
- **HackerRank**: desafíos de programación por nivel
- **Codewars**: katas para mejorar tus habilidades
- **Exercism**: ejercicios con mentoría
- **Project Euler**: problemas matemáticos con programación

### Para leer
- "Clean Code" - Robert C. Martin
- "The Pragmatic Programmer" - Andrew Hunt, David Thomas
- "Design Patterns" - Gang of Four
- "Refactoring" - Martin Fowler
- "Hands-On Machine Learning" - Aurélien Géron
- "Deep Learning" - Ian Goodfellow, Yoshua Bengio, Aaron Courville

---

## 6. CONSEJOS PARA LOS ESTUDIANTES

### Para principiantes (INICIO y NOVATO)
1. No te frustres si algo no sale a la primera. **Todos** los programadores experimentan errores a diario.
2. Escribe código todos los días, aunque sean 20 minutos. La constancia es más importante que la duración.
3. Lee tu código en voz alta para detectar errores lógicos.
4. Usa `print()` o el debugger para entender qué hace tu programa.
5. Haz preguntas en Stack Overflow, foros y comunidades: ¡no hay preguntas tontas!

### Para intermedios (APRENDIZ y TÉCNICO)
1. Aprende a buscar en Google y leer documentación: el 80% del trabajo de un programador es eso.
2. Contribuye a proyectos open source en GitHub: aprendes mucho leyendo código ajeno.
3. Construye proyectos propios, no solo sigas tutoriales.
4. Aprende a usar la terminal y Git desde el principio.
5. Cuida tu salud: descansa, haz ejercicio, duerme bien.

### Para avanzados (TECNÓLOGO en adelante)
1. Especialízate en un área, pero mantén una base amplia.
2. La comunicación es tan importante como el código: aprende a escribir, hablar y documentar.
3. Entiende el negocio: la tecnología es un medio, no un fin.
4. Mentoriza a otros: enseñar es la mejor forma de aprender.
5. Mantente actualizado, pero no te abrumes: céntrate en fundamentos sólidos antes que modas.

PLACEHOLDER_PART5
## 7. PREGUNTAS FRECUENTES

### ¿Cuál es el mejor lenguaje para empezar?
**Python**, sin duda. Su sintaxis es clara, su comunidad es enorme y se usa en prácticamente todos los campos (web, datos, IA, automatización).

### ¿Necesito una computadora potente para programar?
No. Una laptop con 8GB de RAM y un SSD es suficiente para aprender. La nube (AWS, GCP, Vercel) puede hacer el trabajo pesado.

### ¿Cuánto tiempo toma aprender a programar?
Depende de tu objetivo. Para conseguir tu primer empleo junior, entre 6 y 12 meses de estudio dedicado (2-4 horas al día). Para llegar a ingeniero de IA, suma 2-3 años más de práctica constante.

### ¿Necesito un título universitario?
No es obligatorio, pero ayuda. Muchos programadores exitosos son autodidactas. Lo que importa es tu portafolio, tus contribuciones y tu capacidad de resolver problemas.

### ¿Es tarde para empezar a programar?
Nunca es tarde. Hay programadores que empezaron a los 30, 40, 50 años. La programación es una habilidad que se puede aprender a cualquier edad.

### ¿Cómo consigo mi primer trabajo?
- Construye un portafolio con 3-5 proyectos sólidos
- Contribuye a proyectos open source
- Practica algoritmos y estructuras de datos (LeetCode)
- Prepara una buena presencia en LinkedIn y GitHub
- Aplica a puestos junior aunque no cumplas todos los requisitos

---

## 8. MISIÓN DEL ING. MOJICA

> "Mi misión es democratizar el acceso a la programación de calidad en español. Quiero que cada hispanohablante que sueñe con ser desarrollador tenga un mentor paciente, motivador y eficaz a su disposición, las 24 horas del día. La programación cambia vidas, abre puertas y permite crear el futuro. Y ese futuro debe ser en español."

---

**Última actualización**: 2026
**Versión**: 1.0
**Mantenido por**: Equipo CodeAI Tutor





