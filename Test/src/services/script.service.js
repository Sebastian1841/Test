const API_URL = "http://localhost:5000";


export async function saveScript(payload) {
  const res = await fetch(`${API_URL}/scripts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error("Error saving script");
}
