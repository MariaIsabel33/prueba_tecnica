const BASE = import.meta.env.VITE_API_URL

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (res.status === 204) return null
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    const msg = typeof data?.detail === 'string' ? data.detail : 'Datos inválidos'
    throw new Error(msg)
  }
  return data
}

export const listarTareas = (done = null) =>
  request(`/api/tasks${done === null ? '' : `?done=${done}`}`)

export const crearTarea = (t) =>
  request('/api/tasks', { method: 'POST', body: JSON.stringify(t) })

export const cambiarDone = (id, done) =>
  request(`/api/tasks/${id}`, { method: 'PATCH', body: JSON.stringify({ done }) })

export const editarTarea = (id, cambios) =>
  request(`/api/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(cambios) })

export const eliminarTarea = (id) =>
  request(`/api/tasks/${id}`, { method: 'DELETE' })