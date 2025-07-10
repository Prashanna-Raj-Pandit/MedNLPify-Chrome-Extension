document.addEventListener('DOMContentLoaded', function() {
  const analyzeBtn = document.getElementById('analyzeBtn');
  const medicalText = document.getElementById('medicalText');
  const resultsDiv = document.getElementById('results');
  const apiUrl = 'http://localhost:5000/classify';

  // Load saved text if available
  chrome.storage.local.get(['savedText'], function(result) {
    if (result.savedText) {
      medicalText.value = result.savedText;
    }
  });
  analyzeBtn.addEventListener('click', async function() {
    const text = medicalText.value.trim();

    if (text) {
      resultsDiv.innerHTML = '<p>Analyzing medical text... Please wait.</p>';

      try {
        const response = await callNLPModel(text);
        displayResults(response);
      } catch (error) {
        console.error('Error:', error);
        resultsDiv.innerHTML = `
          <p>Error analyzing text: ${error.message}</p>
          <p>Make sure your Flask server is running at ${apiUrl}</p>
        `;
      }
    } else {
      resultsDiv.innerHTML = '<p>Please enter some medical text to analyze.</p>';
    }
  });

  async function callNLPModel(text) {
    const formData = new URLSearchParams();
    formData.append('abstract', text);

    const response = await fetch(apiUrl, {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  function displayResults(results) {
       if (!results || !results.result) {
      resultsDiv.innerHTML = '<p>No results returned from analysis.</p>';
      return;
    }

    let html = '<div class="results-container">';
    html += '<h4>Medical Text Classification Results:</h4>';
    html += '<div class="legend">';
    html += '<span class="label-OBJECTIVE">OBJECTIVE</span>';
    html += '<span class="label-METHODS">METHODS</span>';
    html += '<span class="label-RESULTS">RESULTS</span>';
    html += '<span class="label-CONCLUSIONS">CONCLUSIONS</span>';
    html += '<span class="label-BACKGROUND">BACKGROUND</span>';
    html += '</div>';
    html += '<ul class="results-list">';

    results.result.forEach(item => {
      html += `<li class="${item.class}">`;
      html += `<strong>${item.label}:</strong> ${item.text}`;
      html += '</li>';
    });

    html += '</ul></div>';
    resultsDiv.innerHTML = html;
  }
});