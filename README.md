# Gestor de tareas – Prueba técnica

Aplicación de tareas de extremo a extremo con **FastAPI (Python)**, **Vue 3** y **PostgreSQL**.

## Estructura

```
├── backend/     API en FastAPI (psycopg 3, Pydantic)
├── db/          schema.sql con la tabla tasks
├── frontend/    Vue 3 + Vite (Composition API, <script setup>)
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Git

## 1. Base de datos

Crear la base de datos y la tabla:

```bash
psql -U postgres -c "CREATE DATABASE tasks_db;"
psql -U postgres -d tasks_db -f db/schema.sql
```

También se puede ejecutar el contenido de `db/schema.sql` desde pgAdmin.

## 2. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

Copiar `.env.example` a `.env` y completar los valores:

```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/tasks_db
FRONTEND_ORIGIN=http://localhost:5173
```

Iniciar la API:

```bash
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs

## 3. Frontend

En otra terminal:

```bash
cd frontend
npm install
```

Copiar `.env.example` a `.env`:

```
VITE_API_URL=http://localhost:8000
```

Iniciar:

```bash
npm run dev
```

Disponible en http://localhost:5173

## Endpoints

| Método | Ruta | Descripción | Éxito |
|---|---|---|---|
| GET | `/api/tasks` | Lista las tareas, más recientes primero. Filtro opcional `?done=true/false` | 200 |
| POST | `/api/tasks` | Crea una tarea con `title` y `priority` | 201 |
| PATCH | `/api/tasks/{id}` | Cambia el valor de `done`; también permite editar `title` y `priority` | 200 |
| DELETE | `/api/tasks/{id}` | Elimina la tarea | 204 |

Errores: `422` si el título está vacío o la prioridad no es válida; `400` si el PATCH llega sin campos; `404` si la tarea no existe.

## Funcionalidades del frontend

- Formulario para crear tareas con título y prioridad; no envía si el título está vacío.
- Filtro: todas, pendientes y hechas.
- Lista de tareas con casilla para marcar como hecha, botón para editar y botón para eliminar.
- La lista se actualiza sin recargar la página después de cada acción.
- Mensajes de carga, error y lista vacía.

## Decisiones técnicas

- **Validación en dos capas:** Pydantic rechaza los datos inválidos (422) antes de llegar a la BD, y los `CHECK` de PostgreSQL garantizan la integridad aunque se inserte por fuera de la API.
- **Consultas parametrizadas** con `%s` de psycopg en todas las consultas; nunca se interpolan valores en el SQL.
- **Configuración por variables de entorno** (`DATABASE_URL`, `FRONTEND_ORIGIN`, `VITE_API_URL`); no hay credenciales en el código.
- **Frontend:** las llamadas HTTP están centralizadas en `src/api/tasks.js`; los componentes `TaskForm` y `EstadoMensaje` manejan el formulario y los estados de carga, error y lista vacía.

## Opcionales técnicos

| Opcional | Estado | Detalle |
|---|---|---|
| Editar título | ✅ Implementado | Desde la interfaz se puede editar el título y la prioridad de una tarea (botón **Editar** → **Guardar** / **Cancelar**). |
| Pruebas con pytest | ❌ No implementado | Se priorizó la funcionalidad obligatoria. Ver pendientes. |
| Docker Compose | ❌ No implementado | Se priorizó la funcionalidad obligatoria. Ver pendientes. |

**Cómo se implementó la edición:** el endpoint `PATCH /api/tasks/{id}` acepta los campos `title`, `priority` y `done`, todos opcionales, y solo actualiza los que se envían (`model_dump(exclude_unset=True)`). Así se mantiene el requisito original (cambiar `done`) y se reutiliza el mismo endpoint para editar. Los nombres de columna salen del modelo Pydantic y los valores siguen pasando como parámetros (`%s`).

## Pendientes y mejoras

- Pruebas con pytest sobre la API (un caso correcto y uno de error), y Vitest para el frontend.
- Docker Compose para levantar PostgreSQL, backend y frontend con un solo comando.
- Componente `TaskRow` separado para cada fila de la lista.