<script setup>
import { ref, onMounted } from 'vue'
import { listarTareas, crearTarea, cambiarDone, eliminarTarea, editarTarea } from './api/tasks'
import EstadoMensaje from './components/EstadoMensaje.vue'
import TaskForm from './components/TaskForm.vue'

const tareas = ref([])
const cargando = ref(false)
const error = ref('')
const filtro = ref(null) // null = todas, true = hechas, false = pendientes

// Edición
const editandoId = ref(null)
const edicion = ref({ title: '', priority: 'medium' })

async function cargar() {
  cargando.value = true
  error.value = ''
  try {
    tareas.value = await listarTareas(filtro.value)
  } catch (e) {
    error.value = e.message
  } finally {
    cargando.value = false
  }
}

async function guardar(datos) {
  try {
    await crearTarea(datos)
    await cargar()
  } catch (e) {
    error.value = e.message
  }
}

async function alternar(t) {
  try {
    await cambiarDone(t.id, !t.done)
    await cargar()
  } catch (e) {
    error.value = e.message
  }
}

async function borrar(id) {
  try {
    await eliminarTarea(id)
    await cargar()
  } catch (e) {
    error.value = e.message
  }
}

function empezarEdicion(t) {
  editandoId.value = t.id
  edicion.value = { title: t.title, priority: t.priority }
}

function cancelarEdicion() {
  editandoId.value = null
}

async function guardarEdicion(id) {
  if (!edicion.value.title.trim()) {
    error.value = 'El título no puede estar vacío'
    return
  }
  try {
    await editarTarea(id, {
      title: edicion.value.title.trim(),
      priority: edicion.value.priority,
    })
    editandoId.value = null
    await cargar()
  } catch (e) {
    error.value = e.message
  }
}

function filtrar(valor) {
  filtro.value = valor
  cargar()
}

onMounted(cargar)
</script>

<template>
  <main>
    <h1>Tareas</h1>

    <TaskForm @guardar="guardar" />

    <div>
      <button @click="filtrar(null)">Todas</button>
      <button @click="filtrar(false)">Pendientes</button>
      <button @click="filtrar(true)">Hechas</button>
    </div>

    <EstadoMensaje :cargando="cargando" :error="error" :vacio="!cargando && !error && tareas.length === 0" />

    <ul>
      <li v-for="t in tareas" :key="t.id">
        <template v-if="editandoId === t.id">
          <input v-model="edicion.title" maxlength="120" />
          <select v-model="edicion.priority">
            <option value="low">Baja</option>
            <option value="medium">Media</option>
            <option value="high">Alta</option>
          </select>
          <button @click="guardarEdicion(t.id)">Guardar</button>
          <button @click="cancelarEdicion">Cancelar</button>
        </template>

        <template v-else>
          <input type="checkbox" :checked="t.done" @change="alternar(t)" />
          <span :style="{ textDecoration: t.done ? 'line-through' : 'none' }">
            {{ t.title }}
          </span>
          <small>({{ t.priority }})</small>
          <button @click="empezarEdicion(t)">Editar</button>
          <button @click="borrar(t.id)">Eliminar</button>
        </template>
      </li>
    </ul>
  </main>
</template>