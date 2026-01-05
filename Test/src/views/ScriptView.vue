<template>
  <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6">

    <!-- SELECT -->
    <div class="mb-6">
      <VariableSelect
        :variables="variables"
        v-model="selected"
        @deleted="onDeleted"
      />
    </div>

    <!-- CONTENT -->
    <div class="mt-6">

      <!-- EDITOR -->
      <transition name="fade">
        <div
          v-if="selected"
          class="relative border border-gray-200 rounded-xl bg-gray-50 shadow-inner p-4"
        >
          <!-- Label -->
          <div
            class="absolute -top-3 left-4 px-3 py-0.5 bg-white border border-gray-200
                   rounded-full text-xs font-semibold text-gray-600 shadow-sm"
          >
            Variable seleccionada
          </div>

          <ScriptEditor
            device="DEV-01"
            :variable="selected"
            @saved="reloadVariables"
          />
        </div>
      </transition>

      <!-- EMPTY STATE -->
      <div
        v-if="!selected"
        class="flex items-center justify-center rounded-lg border border-dashed
               border-gray-300 bg-gray-50 py-8"
      >
        <p class="text-sm text-gray-500">
          Selecciona una variable para editar su script
        </p>
      </div>

    </div>

  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import VariableSelect from "../components/scripts/VariableSelect.vue";
import ScriptEditor from "../components/scripts/ScriptEditor.vue";
import { getVariables } from "../services/variable.service";

const selected = ref("");
const variables = ref([]);

async function loadVariables() {
  variables.value = await getVariables("DEV-01");
}

function reloadVariables() {
  loadVariables();
}

function onDeleted(name) {
  if (selected.value === name) {
    selected.value = "";
  }
  loadVariables();
}

onMounted(loadVariables);
</script>
