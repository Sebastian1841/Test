<template>
  <div class="overflow-hidden border rounded-lg">
    <table class="min-w-full text-sm">
      <thead class="bg-gray-50 text-gray-600">
        <tr>
          <th class="px-4 py-2 text-left">Fecha / Hora</th>
          <th class="px-4 py-2 text-left">Variable</th>
          <th class="px-4 py-2 text-left">Valor</th>
        </tr>
      </thead>

      <tbody>
        <TelemetryRow
          v-for="(value, key) in variables"
          :key="key"
          :timestamp="timestamp"
          :variable="key"
          :value="value"
        />
      </tbody>
    </table>
  </div>
</template>

<script setup>
import TelemetryRow from "./TelemetryRow.vue";

defineProps({
  timestamp: String,
  variables: Object,
});
</script>
