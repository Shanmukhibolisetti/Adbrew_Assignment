const url = "http://localhost:8000/todos/";

export async function fetchTasks() {
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch todos");
  return res.json();
}

export async function addTask(task) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task }),
  });
  if (!res.ok) throw new Error("Failed to add todo");
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${url}${id}/`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete todo");
  return res.json();
}
