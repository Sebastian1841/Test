const API_URL = "http://localhost:5000";

export async function getVariables(device) {
  const res = await fetch(`${API_URL}/variables/${device}`);
  return await res.json();
}

export async function deleteVariable(device, variable) {
  await fetch(
    `http://localhost:5000/variables/${device}/${variable}`,
    { method: "DELETE" }
  );
}
