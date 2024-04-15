// script.js

// Define a global constant variable for the server port
const SERVER_PORT = 5500;

document.addEventListener("DOMContentLoaded", function () {
  const signupForm = document.getElementById("signupForm");

  signupForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Hash the password using SHA-256 (or any other secure hash function)
    const hashedPassword = await hashPassword(password);

    try {
      const response = await fetch(`http://localhost:${SERVER_PORT}/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password: hashedPassword }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.Success) {
          console.log("User registration successful!");
        } else {
          console.error("User registration failed.");
        }
      } else {
        console.error("Network error:", response.status, response.statusText);
      }
    } catch (error) {
      console.error("An error occurred:", error.message);
    }
  });
});

// Function to hash the password using SHA-256
async function hashPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashedPassword = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  return hashedPassword;
}
