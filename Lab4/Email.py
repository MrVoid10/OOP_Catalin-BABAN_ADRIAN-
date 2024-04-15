# Email.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, recipient_email):
    """
    Sends an email with the specified subject and body to the recipient.

    Args:
        subject (str): Subject of the email.
        body (str): Content of the email.
        recipient_email (str): Email address of the recipient.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        # Set up the SMTP server (e.g., Gmail's SMTP server)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log in to your email account (replace with your credentials)
        #sender_email = "your_email@gmail.com"
        #sender_password = "your_password"
        sender_email = ""
        sender_password = ""
        
        
        server.login(sender_email, sender_password)

        # Create the message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Quit the server
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
