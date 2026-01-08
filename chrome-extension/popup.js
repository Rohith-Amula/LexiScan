document.addEventListener("DOMContentLoaded", async () => {
  const rawTextarea = document.getElementById("raw");
  const correctedTextarea = document.getElementById("corrected");
  const autoCorrect = document.getElementById("autoCorrect");
  const status = document.getElementById("status");

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript(
      {
        target: { tabId: tab.id },
        function: () => window.getSelection().toString()
      },
      async (results) => {
        const rawText = results[0]?.result || "";
        rawTextarea.value = rawText;

        if (!rawText.trim()) {
          correctedTextarea.value = "⚠️ No text selected.";
          return;
        }

        if (autoCorrect.checked) {
          status.textContent = "⏳ Sending for correction...";
          try {
            const response = await fetch("http://localhost:5000/correct", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ text: rawText })
            });

            const data = await response.json();
            correctedTextarea.value = data.corrected;
            status.textContent = "✅ Correction complete.";
          } catch (error) {
            correctedTextarea.value = "❌ Error connecting to backend.";
            status.textContent = "❌ Failed to fetch correction.";
          }
        } else {
          correctedTextarea.value = "⚠️ Grammar correction disabled.";
          status.textContent = "";
        }
      }
    );
  } catch (e) {
    status.textContent = "❌ Could not access selected text.";
    rawTextarea.value = "";
    correctedTextarea.value = "";
  }
});
