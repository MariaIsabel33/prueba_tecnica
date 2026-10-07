from fastapi import FastAPI, HTTPException
from psycopg import errors
from .db import get_conn
from .schemas import TaskIn, TaskDone

app = FastAPI()

import os
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/tasks")
def listar(done: bool | None = None):
    sql = "SELECT * FROM tasks"
    params = []
    if done is not None:
        sql += " WHERE done = %s"
        params.append(done)
    sql += " ORDER BY created_at DESC, id DESC"
    with get_conn() as conn:
        return conn.execute(sql, params).fetchall()

@app.post("/api/tasks", status_code=201)
def crear(datos: TaskIn):
    try:
        with get_conn() as conn:
            return conn.execute(
                """
                INSERT INTO tasks (title, priority)
                VALUES (%s, %s)
                RETURNING *
                """,
                (datos.title, datos.priority),
            ).fetchone()
    except errors.CheckViolation:
        raise HTTPException(status_code=400, detail="Los datos no cumplen las reglas")

@app.get("/api/tasks/{id}")
def obtener(id: int):
    with get_conn() as conn:
        item = conn.execute(
            "SELECT * FROM tasks WHERE id = %s", (id,)
        ).fetchone()
    if item is None:
        raise HTTPException(status_code=404, detail="No encontrado")
    return item

@app.patch("/api/tasks/{id}")
def actualizar_tarea(id: int, cambios: TaskDone):
    with get_conn() as conn:
        actualizado = conn.execute(
            """
            UPDATE tasks
            SET done = %s
            WHERE id = %s
            RETURNING *
            """,
            (cambios.done, id),
        ).fetchone()
    if actualizado is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return actualizado

@app.delete("/api/tasks/{item_id}", status_code=204)
def eliminar(item_id: int):
    with get_conn() as conn:
        resultado = conn.execute(
            "DELETE FROM tasks WHERE id = %s", (item_id,)
        )
    if resultado.rowcount == 0:
        raise HTTPException(status_code=404, detail="No encontrado")


