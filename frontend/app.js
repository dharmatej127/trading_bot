/**
 * Trading Bot Frontend — Application Logic
 */

const state = {
  symbol: "BTCUSDT",
  side: "BUY",
  type: "MARKET",
  quantity: "",
  price: "",
};

// ------- DOM References -------
const orderForm       = document.getElementById("orderForm");
const inputQuantity   = document.getElementById("inputQuantity");
const inputPrice      = document.getElementById("inputPrice");
const priceField      = document.getElementById("priceField");
const customSymbolField = document.getElementById("customSymbolField");
const customSymbolInput = document.getElementById("customSymbol");
const validationMsg   = document.getElementById("validationMsg");
const submitBtn       = document.getElementById("submitBtn");
const btnText         = document.getElementById("btnText");
const btnLoader       = document.getElementById("btnLoader");
const resultsList     = document.getElementById("resultsList");
const emptyState      = document.getElementById("emptyState");
const clearBtn        = document.getElementById("clearBtn");
const successToast    = document.getElementById("successToast");
const errorToast      = document.getElementById("errorToast");
const toastMsg        = document.getElementById("toastMsg");
const errorToastMsg   = document.getElementById("errorToastMsg");
const statusIndicator = document.getElementById("statusIndicator");
const statusDot       = statusIndicator.querySelector(".status-dot");
const statusText      = statusIndicator.querySelector(".status-text");

// Summary Elements
const summarySymbol   = document.getElementById("summarySymbol");
const summarySide     = document.getElementById("summarySide");
const summaryType     = document.getElementById("summaryType");
const summaryQty      = document.getElementById("summaryQty");
const summaryPrice    = document.getElementById("summaryPrice");
const summaryPriceRow = document.getElementById("summaryPriceRow");

// ------- Symbol Tab Handling -------
document.querySelectorAll(".symbol-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".symbol-tab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");

    const sym = tab.dataset.symbol;
    if (sym === "custom") {
      customSymbolField.classList.remove("hidden");
      customSymbolInput.focus();
      state.symbol = customSymbolInput.value.trim().toUpperCase() || "BTCUSDT";
    } else {
      customSymbolField.classList.add("hidden");
      state.symbol = sym;
    }

    // Update quantity suffix based on base asset
    const base = state.symbol.replace("USDT", "");
    document.getElementById("quantitySuffix").textContent = base;

    updateSummary();
  });
});

customSymbolInput.addEventListener("input", () => {
  state.symbol = customSymbolInput.value.trim().toUpperCase() || "BTCUSDT";
  const base = state.symbol.replace("USDT", "");
  document.getElementById("quantitySuffix").textContent = base;
  updateSummary();
});

// ------- Side Toggle -------
document.querySelectorAll(".side-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".side-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    state.side = btn.dataset.side;
    updateSubmitButton();
    updateSummary();
  });
});

// ------- Type Toggle -------
document.querySelectorAll(".type-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".type-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    state.type = btn.dataset.type;

    if (state.type === "LIMIT") {
      priceField.style.display = "flex";
      priceField.style.flexDirection = "column";
      priceField.style.gap = "8px";
    } else {
      priceField.style.display = "none";
      inputPrice.value = "";
      state.price = "";
      summaryPriceRow.style.display = "none";
    }

    updateSummary();
  });
});

// ------- Quick Quantity Buttons -------
document.querySelectorAll(".qty-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    inputQuantity.value = btn.dataset.qty;
    state.quantity = btn.dataset.qty;
    updateSummary();
  });
});

// ------- Live Summary Update -------
inputQuantity.addEventListener("input", () => {
  state.quantity = inputQuantity.value;
  updateSummary();
});
inputPrice.addEventListener("input", () => {
  state.price = inputPrice.value;
  updateSummary();
});

function updateSummary() {
  summarySymbol.textContent = state.symbol || "—";
  summarySide.textContent   = state.side;
  summarySide.className = `summary-value ${state.side === "BUY" ? "buy-color" : "sell-color"}`;
  summaryType.textContent   = state.type;
  summaryQty.textContent    = state.quantity ? `${state.quantity}` : "—";

  if (state.type === "LIMIT" && state.price) {
    summaryPriceRow.style.display = "flex";
    summaryPrice.textContent = `$${parseFloat(state.price).toLocaleString()}`;
  } else {
    summaryPriceRow.style.display = "none";
  }
}

function updateSubmitButton() {
  if (state.side === "BUY") {
    submitBtn.className = "submit-btn buy-submit";
    btnText.textContent = "Place BUY Order";
  } else {
    submitBtn.className = "submit-btn sell-submit";
    btnText.textContent = "Place SELL Order";
  }
}

// ------- Local Validation -------
function validateInputs() {
  const qty   = parseFloat(inputQuantity.value);
  const price = parseFloat(inputPrice.value);

  if (!inputQuantity.value || isNaN(qty)) {
    return "Quantity is required.";
  }
  if (qty <= 0) {
    return "Quantity must be greater than zero.";
  }
  if (state.type === "LIMIT") {
    if (!inputPrice.value || isNaN(price)) {
      return "Price is required for LIMIT orders.";
    }
    if (price <= 0) {
      return "Price must be greater than zero.";
    }
  }
  if (state.type === "MARKET" && inputPrice.value) {
    return "Price cannot be specified for MARKET orders.";
  }
  return null;
}

function showValidationError(msg) {
  validationMsg.textContent = msg;
  validationMsg.classList.remove("hidden");
}
function clearValidationError() {
  validationMsg.classList.add("hidden");
  validationMsg.textContent = "";
}

// ------- Set Status -------
function setStatus(type, text) {
  statusDot.className = "status-dot";
  if (type === "loading") statusDot.classList.add("loading");
  if (type === "error")   statusDot.classList.add("error");
  statusText.textContent = text;
}

// ------- Form Submit -------
orderForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearValidationError();

  const validationError = validateInputs();
  if (validationError) {
    showValidationError(validationError);
    return;
  }

  const payload = {
    symbol:   state.symbol,
    side:     state.side,
    type:     state.type,
    quantity: parseFloat(inputQuantity.value),
    price:    state.type === "LIMIT" ? parseFloat(inputPrice.value) : null,
  };

  // Loading state
  submitBtn.disabled = true;
  btnText.classList.add("hidden");
  btnLoader.classList.remove("hidden");
  setStatus("loading", "Placing order...");

  try {
    const response = await fetch("/api/place-order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (result.success) {
      addResultCard(payload, result.data, true);
      showToast("success", `Order placed! ID: ${result.data.order_id}`);
      setStatus("ready", "Ready");
      // Reset quantity field
      inputQuantity.value = "";
      state.quantity = "";
      updateSummary();
    } else {
      addResultCard(payload, null, false, result.error);
      showToast("error", result.error || "Order failed.");
      setStatus("error", "Error");
    }
  } catch (err) {
    addResultCard(payload, null, false, "Network error. Could not reach the server.");
    showToast("error", "Cannot reach the server. Is it running?");
    setStatus("error", "Offline");
  } finally {
    submitBtn.disabled = false;
    btnText.classList.remove("hidden");
    btnLoader.classList.add("hidden");
    setTimeout(() => setStatus("ready", "Ready"), 3000);
  }
});

// ------- Result Card -------
function addResultCard(payload, data, success, errorMsg = null) {
  emptyState.classList.add("hidden");

  const card = document.createElement("div");
  const isBuy = payload.side === "BUY";
  card.className = `result-card ${success ? (isBuy ? "success-card" : "sell-card") : "error-card"}`;

  const now = new Date();
  const timeStr = now.toLocaleTimeString();

  if (success && data) {
    const statusClass =
      data.status === "FILLED" ? "status-filled" :
      data.status === "NEW"    ? "status-new" : "";

    card.innerHTML = `
      <div class="card-header">
        <div class="card-badge">
          <span>${payload.symbol}</span>
          <span class="side-pill ${isBuy ? "buy-pill" : "sell-pill"}">${payload.side}</span>
          <span style="color:var(--text-secondary); font-weight:500;">${payload.type}</span>
        </div>
        <span class="card-time">${timeStr}</span>
      </div>
      <div class="card-grid">
        <div class="card-field">
          <span class="card-field-label">Order ID</span>
          <span class="card-field-value">${data.order_id}</span>
        </div>
        <div class="card-field">
          <span class="card-field-label">Status</span>
          <span class="card-field-value ${statusClass}">${data.status}</span>
        </div>
        <div class="card-field">
          <span class="card-field-label">Executed Qty</span>
          <span class="card-field-value">${data.executed_qty}</span>
        </div>
        <div class="card-field">
          <span class="card-field-label">Avg Price</span>
          <span class="card-field-value">${data.avg_price !== "0" && data.avg_price !== "0.00" ? "$" + parseFloat(data.avg_price).toLocaleString() : "—"}</span>
        </div>
        <div class="card-field">
          <span class="card-field-label">Client Order ID</span>
          <span class="card-field-value" style="font-size:0.75rem;">${data.client_order_id}</span>
        </div>
        <div class="card-field">
          <span class="card-field-label">Quantity</span>
          <span class="card-field-value">${payload.quantity}</span>
        </div>
      </div>
    `;
  } else {
    card.innerHTML = `
      <div class="card-header">
        <div class="card-badge">
          <span>${payload.symbol}</span>
          <span class="side-pill ${isBuy ? "buy-pill" : "sell-pill"}">${payload.side}</span>
          <span style="color:var(--text-secondary); font-weight:500;">${payload.type}</span>
        </div>
        <span class="card-time">${timeStr}</span>
      </div>
      <div class="error-message">⚠️ ${errorMsg || "Unknown error."}</div>
    `;
  }

  // Prepend so newest is on top
  resultsList.prepend(card);
}

// ------- Toast -------
let toastTimer;
function showToast(type, message) {
  clearTimeout(toastTimer);

  if (type === "success") {
    toastMsg.textContent = message;
    successToast.classList.remove("hidden");
    errorToast.classList.add("hidden");
  } else {
    errorToastMsg.textContent = message;
    errorToast.classList.remove("hidden");
    successToast.classList.add("hidden");
  }

  toastTimer = setTimeout(() => {
    successToast.classList.add("hidden");
    errorToast.classList.add("hidden");
  }, 4000);
}

// ------- Clear Results -------
clearBtn.addEventListener("click", () => {
  resultsList.innerHTML = "";
  emptyState.classList.remove("hidden");
});

// ------- Init -------
updateSummary();
updateSubmitButton();
