chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "trackJob") {
    // Forward the job data to your API
    fetch('http://localhost:8000/api/track-job', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request.data)
    })
    .then(response => response.json())
    .then(data => sendResponse({success: true, data}))
    .catch(error => sendResponse({success: false, error: error.message}));
    
    return true; // Required for async response
  }
});
