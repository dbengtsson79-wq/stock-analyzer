let priceChart = null;
let rsiChart = null;

async function fetchStock() {
    const ticker = document.getElementById("ticker").value.trim().toUpperCase();
    const errorEl = document.getElementById("error");
    errorEl.textContent = "";

    if (!ticker) {
        errorEl.textContent = "Skriv in en aktie först!";
        return;
    }

    try {
        const response = await fetch(`/api/stock/${ticker}`);
        const json = await response.json();

        if (!json.data || json.data.length === 0) {
            errorEl.textContent = "Hittade ingen data för " + ticker;
            return;
        }

        const dates = json.data.map(d => d.date);
        const closes = json.data.map(d => d.close);
        const ma20 = json.data.map(d => d.ma20);
        const ma50 = json.data.map(d => d.ma50);
        const rsi = json.data.map(d => d.rsi);

        // Plocka ut köp/sälj-punkter
        const buyPoints = json.data.map(d => d.signal === "buy" ? d.close : null);
        const sellPoints = json.data.map(d => d.signal === "sell" ? d.close : null);

        drawPriceChart(dates, closes, ma20, ma50, buyPoints, sellPoints, ticker);
        drawRsiChart(dates, rsi);

    } catch (err) {
        errorEl.textContent = "Något gick fel. Kontrollera aktiesymbolen.";
    }
}

function drawPriceChart(dates, closes, ma20, ma50, buyPoints, sellPoints, ticker) {
    const ctx = document.getElementById("priceChart").getContext("2d");
    if (priceChart) priceChart.destroy();

    priceChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [
                {
                    label: ticker + " Kurs",
                    data: closes,
                    borderColor: "#2196F3",
                    borderWidth: 2,
                    pointRadius: 0
                },
                {
                    label: "MA20",
                    data: ma20,
                    borderColor: "#FF9800",
                    borderWidth: 1.5,
                    pointRadius: 0
                },
                {
                    label: "MA50",
                    data: ma50,
                    borderColor: "#4CAF50",
                    borderWidth: 1.5,
                    pointRadius: 0
                },
                {
                    label: "Köpsignal 🟢",
                    data: buyPoints,
                    borderColor: "green",
                    backgroundColor: "green",
                    pointRadius: 8,
                    pointStyle: "triangle",
                    showLine: false
                },
                {
                    label: "Säljsignal 🔴",
                    data: sellPoints,
                    borderColor: "red",
                    backgroundColor: "red",
                    pointRadius: 8,
                    pointStyle: "triangle",
                    rotation: 180,
                    showLine: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: "Kursutveckling & Signaler" }
            }
        }
    });
}

function drawRsiChart(dates, rsi) {
    const ctx = document.getElementById("rsiChart").getContext("2d");
    if (rsiChart) rsiChart.destroy();

    rsiChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: dates,
            datasets: [
                {
                    label: "RSI (14)",
                    data: rsi,
                    borderColor: "#9C27B0",
                    borderWidth: 2,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: { display: true, text: "RSI – Relativ Styrkeindex" },
                annotation: {}
            },
            scales: {
                y: {
                    min: 0,
                    max: 100,
                    grid: {
                        color: (ctx) => {
                            if (ctx.tick.value === 30 || ctx.tick.value === 70) return "rgba(255,0,0,0.3)";
                            return "rgba(0,0,0,0.05)";
                        }
                    }
                }
            }
        }
    });
}