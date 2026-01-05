<template>
  <div class="flex gap-2 mb-2 flex-wrap">
    <button
      v-for="tpl in templates"
      :key="tpl.label"
      @click="$emit('insert', tpl.code)"
      class="px-3 py-1 bg-gray-200 hover:bg-gray-300 text-sm rounded"
    >
      {{ tpl.label }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  templates: Array
});
</script>
