// public/contentScript.js

// Function to extract email content
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.message === 'getGmailEmailContent') {
    const emailContent = {
      subject: document.querySelector('h2.hP')?.innerText.trim() || 'Hello',
      sender: document.querySelector('.gD')?.innerText.trim() || 'Not',
      date: document.querySelector('.g3')?.innerText.trim() || 'me',
    };

    // Send the extracted content back to the background script or popup
    sendResponse(emailContent);
  }
});