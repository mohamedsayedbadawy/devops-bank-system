/**
 * app.js
 * Talks to the Flask backend and updates the page.
 *
 * For local development (Phase 1-5) the frontend is opened directly
 * (or served by a simple static server) and the Flask API runs on
 * port 5000, so we call it directly. Once Nginx is introduced
 * (Phase 6/7) this can become a relative path like "/api" that
 * nginx.conf forwards to the backend container.
 */

const API_BASE = "/api";

const statusEl = document.getElementById("status");
const tabsEl = document.getElementById("tabs");
const views = {
  login: document.getElementById("view-login"),
  register: document.getElementById("view-register"),
  balance: document.getElementById("view-balance"),
};

let currentUser = null;

// ---------- View / tab handling ----------

function showView(name) {
  Object.values(views).forEach((v) => v.classList.remove("is-active"));
  views[name].classList.add("is-active");

  tabsEl.querySelectorAll(".tabs__btn").forEach((btn) => {
    btn.classList.toggle("is-active", btn.dataset.view === name);
  });
  tabsEl.style.display = name === "balance" ? "none" : "flex";

  setStatus("");
}

function setStatus(message, isOk = false) {
  statusEl.textContent = message || "";
  statusEl.classList.toggle("is-ok", isOk);
}

tabsEl.addEventListener("click", (e) => {
  const btn = e.target.closest(".tabs__btn");
  if (!btn) return;
  showView(btn.dataset.view);
});

// ---------- API helpers ----------

async function apiPost(path, body) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.message || `Request failed (${res.status})`);
  }
  return data;
}

async function apiGet(path) {
  const res = await fetch(`${API_BASE}${path}`);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.message || `Request failed (${res.status})`);
  }
  return data;
}

// ---------- Register ----------

document.getElementById("form-register").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const username = form.username.value.trim();
  const password = form.password.value;
  const balance = parseFloat(form.balance.value || "0");

  try {
    setStatus("Opening account…");
    const data = await apiPost("/register", { username, password, balance });
    setStatus(data.message + " — you can sign in now.", true);
    form.reset();
    showView("login");
    document.querySelector('[data-view="login"]').classList.add("is-active");
  } catch (err) {
    setStatus(err.message);
  }
});

// ---------- Login ----------

document.getElementById("form-login").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const username = form.username.value.trim();
  const password = form.password.value;

  try {
    setStatus("Signing in…");
    const data = await apiPost("/login", { username, password });
    setStatus(data.message, true);
    currentUser = username;
    form.reset();
    await loadBalance();
    showView("balance");
  } catch (err) {
    setStatus(err.message);
  }
});

// ---------- Balance ----------

async function loadBalance() {
  if (!currentUser) return;
  try {
    const data = await apiGet(`/balance/${encodeURIComponent(currentUser)}`);
    document.getElementById("balance-username").textContent = currentUser;
    document.getElementById("balance-amount").textContent = Number(data.balance).toFixed(2);
  } catch (err) {
    setStatus(err.message);
  }
}

document.getElementById("btn-refresh").addEventListener("click", loadBalance);

document.getElementById("btn-signout").addEventListener("click", () => {
  currentUser = null;
  showView("login");
});

// ---------- Initial view ----------
showView("login");
