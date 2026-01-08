window.addEventListener("message", async (event) => {
  if (event.data.type === "LEXISCAN_CORRECT") {
    const selectedText = event.data.text;
    if (document.getElementById("lexiscan-panel")) return;

    const panel = document.createElement("div");
    panel.id = "lexiscan-panel";
    panel.innerHTML = `
      <div class="lexiscan-box">
        <label><input type="checkbox" id="autoCorrect" checked> Enable Grammar Correction</label>
        <div class="lexiscan-columns">
          <div class="column">
            <h4>Raw Text</h4>
            <textarea id="rawText" readonly>${selectedText}</textarea>
            <button onclick="copyToClipboard('rawText')">📋 Copy</button>
            <button onclick="downloadText('rawText', 'raw_text.txt')">⬇️ Export</button>
          </div>
          <div class="column">
            <h4>Corrected Text</h4>
            <textarea id="correctedText" readonly>Loading...</textarea>
            <button onclick="copyToClipboard('correctedText')">📋 Copy</button>
            <button onclick="downloadText('correctedText', 'corrected_text.txt')">⬇️ Export</button>
          </div>
        </div>
        <div id="lexiscan-status"></div>
      </div>
    `;
    document.body.appendChild(panel);

    if (document.getElementById("autoCorrect").checked) {
      try {
        const res = await fetch("http://localhost:5000/correct", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: selectedText })
        });
        const data = await res.json();
        document.getElementById("correctedText").value = data.corrected;
      } catch (e) {
        document.getElementById("correctedText").value = "❌ Error connecting to backend.";
      }
    } else {
      document.getElementById("correctedText").value = "Grammar correction disabled.";
    }
  }
});

// Global functions (to make them available in injected context)
window.copyToClipboard = function (id) {
  const el = document.getElementById(id);
  el.select();
  document.execCommand("copy");
};

window.downloadText = function (id, filename) {
  const text = document.getElementById(id).value;
  const blob = new Blob([text], { type: "text/plain" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
};
