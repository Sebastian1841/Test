<template>
  <div class="flex gap-2 items-center">

    <!-- SELECT -->
    <select
      :value="modelValue"
      @change="onChange"
      class="flex-1 px-3 py-2 border rounded-lg text-sm
             focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option disabled value="">
        Selecciona variable
      </option>

      <option
        v-for="v in variables"
        :key="v.name"
        :value="v.name"
      >
        {{ v.name }}{{ v.is_raw ? " (raw)" : "" }}
      </option>
    </select>

    <!-- BOTÓN ELIMINAR -->
    <button
      v-if="selectedVar && !selectedVar.is_raw"
      @click="showConfirm = true"
      class="px-3 py-2 bg-red-600 hover:bg-red-500
             text-white rounded-lg text-sm"
      title="Eliminar variable derivada"
    >
      🗑️
    </button>

    <!-- MODAL CONFIRMACIÓN -->
    <div
      v-if="showConfirm"
      class="fixed inset-0 bg-black/40
             flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-[300px] text-center">

        <h3 class="font-semibold text-gray-800 mb-2">
          Eliminar variable
        </h3>

        <p class="text-sm text-gray-600 mb-4">
          ¿Seguro que deseas eliminar
          <b>{{ modelValue }}</b>?
        </p>

        <div class="flex justify-center gap-3">
          <button
            @click="remove"
            class="px-4 py-2 bg-red-600 text-white rounded text-sm"
          >
            Eliminar
          </button>

          <button
            @click="showConfirm = false"
            class="px-4 py-2 bg-gray-300 rounded text-sm"
          >
            Cancelar
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { deleteVariable } from "../../services/variable.service";

/* =====================================================
   PROPS
===================================================== */
const props = defineProps({
  variables: {
    type: Array,
    required: true, // [{ name, is_raw }]
  },
  modelValue: String,
});

/* =====================================================
   EMITS
===================================================== */
const emit = defineEmits([
  "update:modelValue",
  "deleted",
]);

/* =====================================================
   STATE
===================================================== */
const showConfirm = ref(false);

/* =====================================================
   COMPUTED
===================================================== */
const selectedVar = computed(() =>
  props.variables.find(v => v.name === props.modelValue)
);

/* =====================================================
   METHODS
===================================================== */
function onChange(e) {
  emit("update:modelValue", e.target.value);
}

async function remove() {
  await deleteVariable("DEV-01", props.modelValue);

  emit("deleted", props.modelValue);
  emit("update:modelValue", "");

  showConfirm.value = false;
}
</script>
