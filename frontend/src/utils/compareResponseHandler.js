export default async function compareResponseHandler(payload) {
  const response = await fetch("/api/compare/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    console.error("Response error:", response.status, response.statusText);

    throw new Error("Response handler failed");
  }
  return await response.json();
}
