chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "correctText",
    title: "Correct Grammar with LexiScan",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "correctText") {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: () => {
        const selected = window.getSelection().toString();
        window.postMessage({ type: "LEXISCAN_CORRECT", text: selected }, "*");
      }
    });
  }
});
