<template>
  <div class="bg-[#1e1e1e] rounded-lg border border-gray-700 overflow-visible">

    <!-- HEADER -->
    <div class="flex items-center justify-between px-3 py-2 bg-[#252526] text-gray-300 text-sm">
      <span class="font-mono">
        Script · {{ variable }}
      </span>

      <button
        @click="save"
        class="px-3 py-1 bg-green-600 hover:bg-green-500 text-white rounded text-xs"
      >
        Guardar
      </button>
    </div>

    <!-- PLANTILLAS -->
    <div class="px-3 py-2 bg-[#252526] flex gap-2 flex-wrap">
      <button
        v-for="tpl in templates"
        :key="tpl.label"
        @click="insertTemplate(tpl.code)"
        class="px-2 py-1 bg-gray-700 hover:bg-gray-600
               text-gray-200 text-xs rounded"
      >
        {{ tpl.label }}
      </button>
    </div>

    <!-- EDITOR -->
    <MonacoEditor
      :value="script"
      @update:value="script = $event"
      language="python"
      theme="vs-dark"
      :options="options"
      class="h-[300px] min-h-[300px]"
    />

    <!-- FOOTER AYUDA -->
    <div class="px-3 py-2 bg-[#1e1e1e] text-gray-400 text-xs font-mono">
      Disponibles:
      <span class="ml-2">var["value"]</span> ·
      <span>var["name"]</span> ·
      <span>var["source"]</span> ·
      <span>out["nueva_var"]</span>
    </div>

    <!-- MODAL OK -->
    <div
      v-if="showSavedModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg shadow-xl p-6 w-[320px] text-center">
        <h3 class="text-lg font-semibold text-gray-800 mb-2">
          Script guardado
        </h3>

        <p class="text-sm text-gray-600 mb-4">
          El script se aplicó correctamente a la variable.
        </p>

        <button
          @click="closeModal"
          class="px-4 py-2 bg-green-600 text-white rounded
                 hover:bg-green-500 text-sm"
        >
          Aceptar
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
/* =====================================================
   IMPORTS
===================================================== */
import { ref, watch } from "vue";
import MonacoEditor from "@guolao/vue-monaco-editor";
import * as monaco from "monaco-editor";
import { saveScript } from "../../services/script.service";

/* =====================================================
   EMITS
===================================================== */
const emit = defineEmits(["saved"]);

/* =====================================================
   PROPS
===================================================== */
const props = defineProps({
  device: String,
  variable: String,
});

/* =====================================================
   SCRIPT BASE (RESET)
===================================================== */
function getInitialScript(variable) {
  return `# Script para ${variable}
# Ejemplos:
# var["value"] = var["value"] / 1000
# var["name"] = "${variable}_new"
# out["${variable}_avg"] = var["value"]
`;
}

/* =====================================================
   STATE
===================================================== */
const script = ref(getInitialScript(props.variable));
const showSavedModal = ref(false);

/* =====================================================
   RESET AL CAMBIAR VARIABLE
===================================================== */
watch(
  () => props.variable,
  (newVar) => {
    script.value = getInitialScript(newVar);
  }
);

/* =====================================================
   OPCIONES MONACO
===================================================== */
const options = {
  fontSize: 14,
  fontFamily: "Fira Code, monospace",
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
  wordWrap: "on",
  automaticLayout: true,
};

/* =====================================================
   AUTOCOMPLETADO (UNA SOLA VEZ)
===================================================== */
let autocompleteRegistered = false;

if (!autocompleteRegistered) {
  monaco.languages.registerCompletionItemProvider("python", {
    provideCompletionItems() {
      return {
        suggestions: [
          {
            label: 'var["value"]',
            kind: monaco.languages.CompletionItemKind.Variable,
            insertText: 'var["value"]',
          },
          {
            label: 'var["name"]',
            kind: monaco.languages.CompletionItemKind.Variable,
            insertText: 'var["name"]',
          },
          {
            label: 'var["source"]',
            kind: monaco.languages.CompletionItemKind.Variable,
            insertText: 'var["source"]',
          },
          {
            label: 'out["nueva_var"]',
            kind: monaco.languages.CompletionItemKind.Variable,
            insertText: 'out["nueva_var"] = ',
          },
        ],
      };
    },
  });

  autocompleteRegistered = true;
}

/* =====================================================
   PLANTILLAS
===================================================== */
const templates = [
  {
    label: "Dividir por 1000",
    code: 'var["value"] = var["value"] / 1000',
  },
  {
    label: "Cambiar nombre",
    code: 'var["name"] = "flow_m3"',
  },
  {
    label: "Crear nueva variable",
    code: 'out["flow_avg"] = var["value"]',
  },
];

/* =====================================================
   ACCIONES
===================================================== */
function insertTemplate(code) {
  script.value += "\n" + code;
}

async function save() {
  await saveScript({
    device_code: props.device,
    variable: props.variable,
    order: 1,
    code: script.value,
  });

  showSavedModal.value = true;
  emit("saved");
}

function closeModal() {
  showSavedModal.value = false;
}
</script>
