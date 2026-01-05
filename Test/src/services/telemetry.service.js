const API_URL = "http://localhost:5000";


export async function getLastTelemetry(deviceId) {
  const res = await fetch(`${API_URL}/telemetry/${deviceId}`);
  if (!res.ok) throw new Error("Error fetching telemetry");
  return res.json();
}
