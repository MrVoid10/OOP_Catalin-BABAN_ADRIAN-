// login.js

// Define the server port (adjust as needed)
const SERVER_PORT = 5500;

document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Hash the password using SHA-256
    const hashedPassword = await hashPassword(password);

    // Send a POST request to the server
    try {
        const response = await fetch(`http://localhost:${SERVER_PORT}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password: hashedPassword }),
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                console.log('Login successful!');
                alert(`Token: ${data.Token}`);
                window.location.href = 'main.html'; // Redirect to main.html
            } else {
                // Handle specific error cases
                if (data.email) {
                    alert('Invalid email. Please try again.');
                } else if (data.login) {
                    alert('Invalid login credentials. Please try again.');
                } else {
                    alert('Unknown error. Please try again.');
                }
            }
        } else {
            console.error('Network error:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('An error occurred:', error.message);
    }
});

// Function to hash the password using SHA-256
async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashedPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashedPassword;
}
