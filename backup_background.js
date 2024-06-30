// public/background.js

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  
    if (request.message === 'extractGmailEmailContent') {
      const emailContent = request.content;
  
      // Post the email content to your model or handle as needed
      const requestBody = {
        subject: emailContent.subject,
        sender: emailContent.sender,
        body: emailContent.body,
        date: emailContent.date,
      };
  
      // Example: Post the email content to your model
      fetch('http://your-model-api-url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      })
        .then(response => response.json())
        .then(data => {
          // Process the response from your model
          console.log('Model response:', data);
        })
        .catch(error => {
          console.error('Error posting email content to model:', error);
        });
  
      // Respond to the content script
      sendResponse({ success: true });
    }
    if (request.message === 'getGmailEmailContent') {
      // Simulate or fetch Gmail email content
      const gmailEmailContent = {
        subject: 'Gmail Subject',
        sender: 'example@gmail.com',
        date: '2023-01-01',
        // Add any other necessary properties
      };
  
      // Respond to the content script with Gmail email content
      sendResponse(gmailEmailContent);
    }
  });

