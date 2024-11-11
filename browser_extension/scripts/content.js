function extractPageContent() {
    const content = {
        raw_content: document.body.innerText || '',
        html_content: document.body.innerHTML || '',
        url: window.location.href
    };
    
    console.log('Sending to backend:', content);
    return content;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "trackJob") {
        const content = extractPageContent();
        
        fetch('http://localhost:8000/api/parse-job', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(content)
        })
        .then(async response => {
            const text = await response.text();
            console.log('Response text:', text);
            return text ? JSON.parse(text) : {};
        })
        .then(data => {
            console.log('Parsed response:', data);
            sendResponse({ success: true, data });
        })
        .catch(error => {
            console.error('Error:', error);
            sendResponse({ success: false, error: error.message });
        });
        
        return true;
    }
}); 