<template>
  <tr class="hover:bg-blue-50 transition">
    <td class="px-4 py-2 text-gray-500">
      {{ formattedTime }}
    </td>
    <td class="px-4 py-2 font-medium text-gray-800">
      {{ variable }}
    </td>
    <td class="px-4 py-2 text-gray-700">
      {{ value }}
    </td>
  </tr>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  timestamp: String,
  variable: String,
  value: [String, Number],
});

const formattedTime = computed(() =>
  new Date(props.timestamp).toLocaleString()
);
</script>
