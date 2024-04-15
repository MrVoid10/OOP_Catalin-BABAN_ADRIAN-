# server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
PORT = 5500
import random
import smtplib
from email.mime.text import MIMEText
#my libraries
from DB import *
from Email import *

app = Flask(__name__)
CORS(app)

# Initialize user data list
user_data = [
    {"username": "adrytimus", "email": "adrytimus@gmail.com", "hashed_password": "12345"},
]
recovery_codes = {}

def generate_recovery_code():
    return str(random.randint(100000, 999999))

def send_recovery_email(email, code):
    # Replace with your SMTP server details
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_username'
    smtp_password = 'your_password'

    msg = MIMEText(f"Your recovery code: {code}")
    msg['Subject'] = 'Password Recovery Code'
    msg['From'] = 'noreply@example.com'
    msg['To'] = email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
            return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        hashed_password = data.get("password")  # Assuming the client sends the hashed password

        # Create a new User instance
        new_user = User(username, email, hashed_password)

        # Add the user to the database
        if add_user(new_user):
            # Respond with success
            return jsonify({"Success": True}), 200
        else:
            # Respond with failure
            return jsonify({"Success": False, "Error": "Failed to add user to the database"}), 500

    except Exception as e:
        # Respond with failure
        return jsonify({"Success": False, "Error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()  # Parse the request data as JSON
        email = data.get("email")
        password = data.get("password")

        # Retrieve the user from the database
        user_from_db = get_user_by_email(email)

        if user_from_db and user_from_db.hashed_password == password:
            # Successful login
            response_data = {
                "success": True,
                "Token": 12345  # Replace with an actual token
            }
            return jsonify(response_data)

        # Invalid login
        response_data = {
            "success": False,
            "message": "Invalid email or password"
        }
        return jsonify(response_data), 401

    except Exception as e:
        # Handle any other exceptions 
        print(f"An error occurred: {str(e)}")
        return jsonify({"success": False, "error": "Invalid request data"}), 400


# new
@app.route('/send-verification-email', methods=['POST'])
def send_verification_email():
    data = request.get_json()
    email = data.get('email')

    # Check if the user exists in your user database (replace with your actual logic)
    user = get_user_by_email(email)

    if user:

        #verification_code = '123456' #for debug if the mail doesnt work
        
        verification_code = str(generate_recovery_code())
        print(f"the code for debugging or if the email doesnt work{verification_code}")
        success = send_email("Password recovery code", verification_code, email)
        if success:
            print("Email sent successfully.")
        else:
            print("Failed to send email.")
        

        # Store the code in the recovery_codes dictionary
        recovery_codes[email] = verification_code

        return jsonify({'message': 'Verification code sent'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404
    
#new new

@app.route('/recover-password', methods=['POST'])
def recover_password():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    new_password = data.get('newPassword')

    # Check if the email exists 
    user = get_user_by_email(email)

    if user and recovery_codes.get(email) == code:
        # Update the password in your user database 
        update_user_password(email,new_password)
        #user.hashed_password = new_password

        # Remove the code from the temporary storage
        del recovery_codes[email]

        # Save changes to the database 

        return jsonify({'message': 'Password changed successfully'}), 200
    else:
        return jsonify({'message': 'Invalid email or code'}), 400

if __name__ == "__main__":
    app.run(host="localhost", port=PORT)
