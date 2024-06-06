async function sendRequest(action) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/${action}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        if (response.ok) {
            const result = await response.json();
            alert(`Success: ${result.message}`);
        } else {
            const errorData = await response.json();
            alert('Error: ' + (errorData.detail || response.statusText));
        }
    } catch (error) {
        alert('Network Error: ' + error.message);
    }
}
