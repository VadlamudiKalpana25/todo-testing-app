const API = "http://127.0.0.1:8000";
let token = "";

const $ = (id) => document.getElementById(id);

function setAuthStatus(text) {
  $("authStatus").innerText = text;
}

function authHeaders() {
  return token ? { "Authorization": `Bearer ${token}` } : {};
}

async function request(path, options = {}) {
  const res = await fetch(`${API}${path}`, options);
  if (!res.ok) {
    let msg = `${res.status} ${res.statusText}`;
    try {
      const j = await res.json();
      if (j.detail) msg = `${msg} - ${j.detail}`;
    } catch {}
    throw new Error(msg);
  }
  if (res.status === 204) return null;
  return res.json();
}

async function register() {
  const email = $("email").value.trim();
  const password = $("password").value;
  await request("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  alert("Registered! Now login.");
}

async function login() {
  const email = $("email").value.trim();
  const password = $("password").value;

  const data = await request("/auth/login-json", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  token = data.access_token;
  setAuthStatus(`Logged in as ${email}`);
  await refresh();
}

function logout() {
  token = "";
  setAuthStatus("Not logged in");
  $("todos").innerHTML = "";
}

async function addTodo() {
  const title = $("newTitle").value.trim();
  if (!title) return alert("Title required");
  await request("/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ title })
  });
  $("newTitle").value = "";
  await refresh();
}

async function toggle(todo) {
  await request(`/todos/${todo.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ completed: !todo.completed })
  });
  await refresh();
}

async function edit(todo) {
  const newTitle = prompt("New title:", todo.title);
  if (newTitle === null) return;
  await request(`/todos/${todo.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ title: newTitle })
  });
  await refresh();
}

async function remove(todo) {
  await request(`/todos/${todo.id}`, {
    method: "DELETE",
    headers: { ...authHeaders() }
  });
  await refresh();
}

function render(todos) {
  const container = $("todos");
  container.innerHTML = "";
  todos.forEach(todo => {
    const div = document.createElement("div");
    div.className = "todo";
    const left = document.createElement("div");
    const title = document.createElement("span");
    title.textContent = todo.title;
    if (todo.completed) title.className = "done";
    left.appendChild(title);

    const actions = document.createElement("div");
    const btnToggle = document.createElement("button");
    btnToggle.textContent = todo.completed ? "Undo" : "Done";
    btnToggle.onclick = () => toggle(todo);

    const btnEdit = document.createElement("button");
    btnEdit.textContent = "Edit";
    btnEdit.onclick = () => edit(todo);

    const btnDel = document.createElement("button");
    btnDel.textContent = "Delete";
    btnDel.onclick = () => remove(todo);

    actions.appendChild(btnToggle);
    actions.appendChild(btnEdit);
    actions.appendChild(btnDel);

    div.appendChild(left);
    div.appendChild(actions);
    container.appendChild(div);
  });
}

async function refresh() {
  if (!token) return alert("Login first");
  const todos = await request("/todos", { headers: { ...authHeaders() } });
  render(todos);
}

async function search() {
  if (!token) return alert("Login first");
  const q = encodeURIComponent($("search").value.trim());
  const todos = await request(`/todos?q=${q}`, { headers: { ...authHeaders() } });
  render(todos);
}

$("btnRegister").onclick = () => register().catch(e => alert(e.message));
$("btnLogin").onclick = () => login().catch(e => alert(e.message));
$("btnLogout").onclick = () => logout();
$("btnAdd").onclick = () => addTodo().catch(e => alert(e.message));
$("btnRefresh").onclick = () => refresh().catch(e => alert(e.message));
$("btnSearch").onclick = () => search().catch(e => alert(e.message));
