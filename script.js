async function loadCrypto() {
  try {

    const response = await fetch(
      "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,ripple&vs_currencies=inr&include_24hr_change=true"
    );

    const data = await response.json();

    document.getElementById("btc").textContent =
      "₹ " + data.bitcoin.inr.toLocaleString();

    document.getElementById("eth").textContent =
      "₹ " + data.ethereum.inr.toLocaleString();

    document.getElementById("sol").textContent =
      "₹ " + data.solana.inr.toLocaleString();

    document.getElementById("xrp").textContent =
      "₹ " + data.ripple.inr.toLocaleString();

    const change = data.bitcoin.inr_24h_change || 0;

    let signal = "🟡 HOLD";
    if (change > 3) {
      signal = "🟢 BUY";
    } else if (change < -3) {
      signal = "🔴 SELL";
    }

    document.getElementById("signal").textContent =
      `${signal} (${change.toFixed(2)}%)`;

    document.getElementById("updated").textContent =
      new Date().toLocaleTimeString();

    const market = await fetch(
      "https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&order=market_cap_desc&per_page=10&page=1"
    );

    const coins = await market.json();

    const list = document.getElementById("topCoins");
    list.innerHTML = "";

    coins.forEach((coin) => {
      const li = document.createElement("li");
      li.textContent = `${coin.name} - ₹${coin.current_price.toLocaleString()}`;
      list.appendChild(li);
    });

  } catch (err) {
    console.error(err);

    document.getElementById("btc").textContent = "API Error";
    document.getElementById("eth").textContent = "API Error";
    document.getElementById("sol").textContent = "API Error";
    document.getElementById("xrp").textContent = "API Error";
    document.getElementById("signal").textContent = "API Error";
    document.getElementById("updated").textContent = "--";
  }
}

loadCrypto();
setInterval(loadCrypto, 30000);
const chartResponse = await fetch(
  "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=inr&days=7"
);

const chartData = await chartResponse.json();

const labels = chartData.prices.map(item =>
  new Date(item[0]).toLocaleDateString()
);

const prices = chartData.prices.map(item => item[1]);

new Chart(document.getElementById("btcChart"), {
  type: "line",
  data: {
    labels,
    datasets: [{
      label: "Bitcoin Price",
      data: prices,
      borderColor: "#22c55e",
      fill: false
    }]
  }
});