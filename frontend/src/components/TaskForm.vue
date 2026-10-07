<script setup>
import { reactive, ref } from 'vue'

const emit = defineEmits(['guardar'])
const form = reactive({ title: '', priority: 'medium' })
const errorLocal = ref('')

function enviar() {
  if (!form.title.trim()) {
    errorLocal.value = 'El título es obligatorio'
    return
  }
  errorLocal.value = ''
  emit('guardar', { title: form.title.trim(), priority: form.priority })
  form.title = ''
  form.priority = 'medium'
}
</script>

<template>
  <form @submit.prevent="enviar">
    <input v-model="form.title" maxlength="120" placeholder="Nueva tarea" />
    <select v-model="form.priority">
      <option value="low">Baja</option>
      <option value="medium">Media</option>
      <option value="high">Alta</option>
    </select>
    <button type="submit">Agregar</button>
    <p v-if="errorLocal" style="color: red">{{ errorLocal }}</p>
  </form>
</template>