const API_BASE = ["localhost", "127.0.0.1"].includes(window.location.hostname)
  ? "https://gen-ai-rewrite-studio-doom.netlify.app"
  : "";

const source = document.querySelector("#source");
const charCount = document.querySelector("#charCount");
const rewriteButton = document.querySelector("#rewriteButton");
const rewriteButtonText = document.querySelector("#rewriteButtonText");
const formError = document.querySelector("#formError");
const emptyState = document.querySelector("#emptyState");
const resultsContent = document.querySelector("#resultsContent");
const serviceStatus = document.querySelector("#serviceStatus");
const serviceStatusText = document.querySelector("#serviceStatusText");

const state = { style: "clear", output: null };

function setServiceStatus(status, label) {
  serviceStatus.dataset.state = status;
  serviceStatusText.textContent = label;
}

function showError(message) {
  formError.textContent = message;
  formError.hidden = false;
}

function clearError() {
  formError.textContent = "";
  formError.hidden = true;
}

function updateCount() {
  charCount.textContent = String(source.value.length);
}

function setBusy(busy) {
  rewriteButton.disabled = busy;
  rewriteButton.classList.toggle("is-loading", busy);
  rewriteButton.setAttribute("aria-busy", String(busy));
  rewriteButtonText.textContent = busy ? "Rewriting your text…" : "Rewrite my text";
}

function setText(id, value) {
  document.getElementById(id).textContent = value || "";
}

function renderFacts(facts) {
  const list = document.querySelector("#factsList");
  list.replaceChildren();
  for (const fact of facts) {
    const item = document.createElement("li");
    item.textContent = fact;
    list.append(item);
  }
}

function renderResult(result) {
  state.output = result;
  setText("originalText", source.value.trim());
  setText("primaryText", result.primary);
  setText("primaryTitle", result.primaryTitle || "Your selected style");
  setText("primaryLabel", result.primaryLabel || "REWRITE");
  setText("secondaryTitle", result.secondaryTitle || "Another option");
  setText("secondaryLabel", result.secondaryLabel || "ANOTHER OPTION");
  setText("secondaryText", result.secondary);
  setText("interpretationText", result.interpretation || "No additional interpretation was generated.");
  setText("modelLabel", result.model ? "Model: " + result.model : "");
  renderFacts(Array.isArray(result.facts) ? result.facts : []);
  document.querySelector("#secondaryCard").hidden = !result.secondary;
  emptyState.hidden = true;
  resultsContent.hidden = false;
}

async function checkService() {
  try {
    const response = await fetch(`${API_BASE}/api/status`, { headers: { Accept: "application/json" } });
    const data = await response.json();
    if (!response.ok) throw new Error("Status request failed");
    if (data.ready) {
      setServiceStatus("ready", "AI ready");
    } else {
      setServiceStatus("missing", "AI unavailable");
    }
  } catch {
    setServiceStatus("error", "Service unavailable");
  }
}

async function rewrite() {
  clearError();
  const text = source.value.trim();
  if (!text) {
    showError("Add a draft first. Even a couple of sentences is enough to get started.");
    source.focus();
    return;
  }
  if (text.length > 5000) {
    showError("Keep your draft under 5,000 characters.");
    return;
  }

  setBusy(true);
  try {
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 55_000);
    let response;
    try {
      response = await fetch(`${API_BASE}/api/rewrite`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ text, style: state.style, both: document.querySelector("#bothStyles").checked }),
        signal: controller.signal,
      });
    } finally {
      window.clearTimeout(timeout);
    }

    const result = await response.json().catch(() => ({}));
    if (!response.ok) {
      const message = result.error || "The rewrite could not be completed. Please try again.";
      if (result.code === "AI_NOT_CONFIGURED") setServiceStatus("missing", "AI unavailable");
      throw new Error(message);
    }

    renderResult(result);
    setServiceStatus("ready", "AI ready");
  } catch (error) {
    if (error.name === "AbortError") {
      showError("This rewrite took too long. Check your connection and try again.");
    } else {
      showError(error.message || "The service could not be reached. Please try again in a moment.");
    }
  } finally {
    setBusy(false);
  }
}

source.addEventListener("input", () => {
  updateCount();
  clearError();
});

document.querySelectorAll(".style-option").forEach((button) => {
  button.addEventListener("click", () => {
    state.style = button.dataset.style;
    document.querySelectorAll(".style-option").forEach((option) => {
      const selected = option === button;
      option.classList.toggle("is-selected", selected);
      option.setAttribute("aria-pressed", String(selected));
    });
  });
});

rewriteButton.addEventListener("click", rewrite);
source.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") rewrite();
});

document.querySelector("#exampleButton").addEventListener("click", () => {
  source.value = "i have been working on our project and we need to improve the writing before we share it with the team. the presentation is done but the report still need edits.";
  updateCount();
  clearError();
  source.focus();
});

document.querySelector("#clearButton").addEventListener("click", () => {
  source.value = "";
  updateCount();
  clearError();
  state.output = null;
  resultsContent.hidden = true;
  emptyState.hidden = false;
  source.focus();
});

document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    if (!state.output) return;
    const key = button.dataset.copy;
    const value = key === "original" ? source.value.trim() : state.output[key];
    if (!value) return;
    try {
      await navigator.clipboard.writeText(value);
      const label = button.querySelector("span");
      const previous = label.textContent;
      label.textContent = "Copied";
      button.classList.add("is-copied");
      window.setTimeout(() => {
        label.textContent = previous;
        button.classList.remove("is-copied");
      }, 1300);
    } catch {
      showError("Clipboard access was blocked. Select the text and copy it manually.");
    }
  });
});

updateCount();
checkService();
