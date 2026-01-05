<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Telemetría -->
      <div class="bg-white rounded-xl shadow p-6">
        <TelemetryView />
      </div>

      <!-- Scripts -->
      <div class="bg-white rounded-xl shadow p-6">
        <ScriptView />
      </div>
    </div>
  </div>
</template>

<script setup>
import TelemetryView from "./views/TelemetriaView.vue";
import ScriptView from "./views/ScriptView.vue";
</script>
