<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-gray-800">
        Última telemetría
      </h2>

      <button
        @click="load"
        class="px-4 py-2 rounded-lg bg-blue-600 text-white text-sm font-medium
               hover:bg-blue-700 transition"
      >
        Actualizar
      </button>
    </div>

    <TelemetryTable
      v-if="data"
      :timestamp="data.timestamp"
      :variables="data.variables"
    />

    <p v-else class="text-sm text-gray-400">
      Presiona “Actualizar” para cargar datos
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { getLastTelemetry } from "../services/telemetry.service";
import TelemetryTable from "../components/telemetry/TelemetryTable.vue";

const data = ref(null);

async function load() {
  data.value = await getLastTelemetry("DEV-01");
}
</script>
