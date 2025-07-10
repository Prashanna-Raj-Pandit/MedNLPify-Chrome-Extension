// Set up context menu item
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "mednlpify",
    title: "Analyze with MedNLPify",
    contexts: ["selection"]
  });
});

// Add listener for context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "mednlpify" && info.selectionText) {
    // Store the selected text
    chrome.storage.local.set({ selectedText: info.selectionText });

    // Open the popup
    chrome.action.openPopup();
  }
});

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getSelectedText") {
    chrome.storage.local.get(['selectedText'], function(result) {
      sendResponse({ text: result.selectedText || '' });
    });
    return true; // Required for async response
  }
});