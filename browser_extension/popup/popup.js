document.addEventListener('DOMContentLoaded', async () => {
  const jobDetails = document.getElementById('jobDetails');
  const jobContent = document.getElementById('jobContent');
  const loadingState = document.getElementById('loadingState');
  const errorState = document.getElementById('errorState');
  const trackButton = document.getElementById('trackButton');

  try {
    // Get current tab URL
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (!tab.url.includes('linkedin.com/jobs')) {
      throw new Error('Please open a LinkedIn job posting page');
    }
    
    loadingState.classList.remove('hidden');
    
    const response = await fetch('http://localhost:8000/api/parse-job', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: tab.url })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to parse job');
    }
    
    const jobData = await response.json();
    
    // Display job details
    jobContent.innerHTML = `
      <p><strong>Title:</strong> ${jobData.job_title || 'Not found'}</p>
      <p><strong>Company:</strong> ${jobData.company || 'Not found'}</p>
      <p><strong>Location:</strong> ${jobData.location || 'Not found'}</p>
      <p><strong>Salary:</strong> ${jobData.salary_range || 'Not mentioned'}</p>
      <p><strong>Keywords:</strong> ${jobData.keywords || 'Not found'}</p>
    `;
    
    loadingState.classList.add('hidden');
    jobDetails.classList.remove('hidden');
    
  } catch (error) {
    loadingState.classList.add('hidden');
    errorState.textContent = error.message;
    errorState.classList.remove('hidden');
  }
});

document.getElementById('trackButton').addEventListener('click', async () => {
    const button = document.getElementById('trackButton');
    button.disabled = true;
    button.textContent = 'Tracking...';
    
    try {
        const response = await fetch('http://localhost:8000/api/track-job', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_title: document.getElementById('jobTitle').textContent,
                company: document.getElementById('company').textContent,
                location: document.getElementById('location').textContent,
                job_link: document.getElementById('jobLink').value,
                keywords: document.getElementById('keywords').textContent,
                salary_range: document.getElementById('salary').textContent,
                notes: document.getElementById('notes').textContent
            })
        });
        
        if (!response.ok) throw new Error('Failed to track job');
        
        button.textContent = 'Job Tracked!';
        button.style.backgroundColor = '#4CAF50';
        
    } catch (error) {
        button.textContent = 'Error - Try Again';
        button.disabled = false;
        button.style.backgroundColor = '#f44336';
    }
});
