<script setup>
defineProps({ cargando: Boolean, error: String, vacio: Boolean })
</script>

<template>
  <p v-if="cargando">Cargando...</p>
  <p v-else-if="error" style="color: red">⚠ {{ error }}</p>
  <p v-else-if="vacio">No hay tareas.</p>
</template>