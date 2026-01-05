import { ref } from "vue";
import { getVariables } from "../services/variable.service";

// Estado reactivo compartido
const variables = ref([]);
const loading = ref(false);

// Cargar variables desde backend
async function loadVariables(deviceCode) {
  loading.value = true;
  try {
    const data = await getVariables(deviceCode);
    variables.value = data; // RAW + DERIVED
  } finally {
    loading.value = false;
  }
}

// Composable
export function useVariablesStore() {
  return {
    variables,
    loading,
    loadVariables,
  };
}
