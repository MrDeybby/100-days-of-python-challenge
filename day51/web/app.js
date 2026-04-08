const API_URL = "";
let categoryChart;
let monthlyChart;

const form = document.getElementById("expense-form");
const messageEl = document.getElementById("form-message");
const rowsEl = document.getElementById("expense-rows");
const totalCountEl = document.getElementById("total-count");
const totalSpentEl = document.getElementById("total-spent");

const formatCurrency = (value) =>
  new Intl.NumberFormat("es-ES", { style: "currency", currency: "USD" }).format(
    value
  );

async function fetchJSON(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.error || "Error de servidor");
  }
  return res.json();
}

async function loadExpenses() {
  const data = await fetchJSON("/api/expenses?limit=50");
  const expenses = data.expenses || [];
  rowsEl.innerHTML = "";
  if (!expenses.length) {
    rowsEl.innerHTML = "<tr><td colspan='4'>Sin datos aún</td></tr>";
  } else {
    expenses
      .slice()
      .reverse()
      .forEach((e) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${e.date}</td>
          <td>${e.category}</td>
          <td>${e.description || "—"}</td>
          <td class="num">${formatCurrency(Number(e.amount))}</td>
        `;
        rowsEl.appendChild(tr);
      });
  }
  totalCountEl.textContent = `${expenses.length} movimientos`;
}

function buildChart(ctx, config) {
  if (config.type === "doughnut" && categoryChart) categoryChart.destroy();
  if (config.type === "line" && monthlyChart) monthlyChart.destroy();

  const chart = new Chart(ctx, {
    ...config,
    options: {
      plugins: { legend: { labels: { color: "#e8ecff" } } },
      scales: {
        x: { ticks: { color: "#9aa5c4" }, grid: { color: "#1e2743" } },
        y: { ticks: { color: "#9aa5c4" }, grid: { color: "#1e2743" } },
      },
    },
  });
  if (config.type === "doughnut") categoryChart = chart;
  if (config.type === "line") monthlyChart = chart;
}

async function loadSummary() {
  const data = await fetchJSON("/api/summary");
  totalSpentEl.textContent = `Total: ${formatCurrency(data.total_spent || 0)}`;

  const categories = data.by_category || [];
  buildChart(document.getElementById("category-chart"), {
    type: "doughnut",
    data: {
      labels: categories.map((c) => c.label),
      datasets: [
        {
          data: categories.map((c) => c.total),
          backgroundColor: [
            "#6cf0c2",
            "#8aa7ff",
            "#ffd166",
            "#ef476f",
            "#06d6a0",
            "#118ab2",
          ],
        },
      ],
    },
  });

  const months = data.by_month || [];
  buildChart(document.getElementById("monthly-chart"), {
    type: "line",
    data: {
      labels: months.map((m) => m.label),
      datasets: [
        {
          label: "Gasto mensual",
          data: months.map((m) => m.total),
          borderColor: "#8aa7ff",
          backgroundColor: "rgba(138, 167, 255, 0.25)",
          tension: 0.2,
          fill: true,
        },
      ],
    },
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  messageEl.textContent = "";
  const payload = {
    date: document.getElementById("date").value,
    category: document.getElementById("category").value,
    description: document.getElementById("description").value,
    amount: document.getElementById("amount").value,
  };
  try {
    await fetchJSON("/api/expenses", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    messageEl.textContent = "Guardado ✓";
    form.reset();
    loadExpenses();
    loadSummary();
  } catch (err) {
    messageEl.textContent = err.message;
  }
});

async function init() {
  try {
    await loadExpenses();
    await loadSummary();
  } catch (err) {
    messageEl.textContent = "No se pudo conectar al servidor Flask.";
  }
}

init();
