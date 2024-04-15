// recovery.js

// Set the port number (adjust as needed)
const port = 5500;

// Function to send a POST request
async function sendRequest(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Request failed');
        }
    } catch (error) {
        console.error('An error occurred:', error);
        throw error;
    }
}

// Function to hash the password using SHA-256
async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashedPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashedPassword;
}

// Handle email form submission
document.getElementById('emailForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;

    try {
        const response = await sendRequest(`http://localhost:${port}/send-verification-email`, { email });

        // Show the code/password form
        document.getElementById('emailForm').style.display = 'none';
        document.getElementById('codeForm').style.display = 'block';
    } catch (error) {
        alert('Error sending verification email. Please try again.');
    }
});

// Handle code/password form submission
document.getElementById('codeForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const code = document.getElementById('code').value;
    const newPassword = document.getElementById('newPassword').value;

    // Hash the new password
    const hashedNewPassword = await hashPassword(newPassword);

    try {
        const response = await sendRequest(`http://localhost:${port}/recover-password`, {
            email: document.getElementById('email').value,
            code,
            newPassword: hashedNewPassword, // Send hashed password
        });

        if (response.message === 'Password changed successfully') {
            alert('Password changed successfully!');
            window.location.href = 'main.html'; // Redirect to main.html
        } else {
            alert('Error changing password. Please try again.');
        }
    } catch (error) {
        console.error('An error occurred:', error.message);
    }
});
