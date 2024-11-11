document.getElementById('promptForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const prompt = document.getElementById('prompt').value;
    const submitButton = document.querySelector('.submit-button');
    
    // Disable button and show loading state
    submitButton.disabled = true;
    submitButton.textContent = 'Analyzing...';
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Show results
            document.getElementById('result').style.display = 'block';
            document.getElementById('strategy').textContent = data.prediction.strategy;
            document.getElementById('confidence').textContent = 
                `${(data.prediction.confidence * 100).toFixed(1)}%`;
            document.getElementById('explanation').textContent = data.prediction.explanation;
        } else {
            alert('Error: ' + data.message);
        }
    } catch (error) {
        alert('Error analyzing prompt. Please try again.');
    } finally {
        // Reset button state
        submitButton.disabled = false;
        submitButton.textContent = 'Analyze';
    }
}); 