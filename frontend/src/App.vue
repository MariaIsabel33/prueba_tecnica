<script setup>
import { ref, onMounted } from 'vue'
import { listarTareas, crearTarea, cambiarDone, eliminarTarea } from './api/tasks'
import EstadoMensaje from './components/EstadoMensaje.vue'
import TaskForm from './components/TaskForm.vue'

const tareas = ref([])
const cargando = ref(false)
const error = ref('')
const filtro = ref(null) // null = todas, true = hechas, false = pendientes

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
        <input type="checkbox" :checked="t.done" @change="alternar(t)" />
        <span :style="{ textDecoration: t.done ? 'line-through' : 'none' }">
          {{ t.title }}
        </span>
        <small>({{ t.priority }})</small>
        <button @click="borrar(t.id)">Eliminar</button>
      </li>
    </ul>
  </main>
</template>