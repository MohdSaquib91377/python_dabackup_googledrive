import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_mail(to_email, subject, message, server='smtp.gmail.com', port=587, from_email=os.getenv('SENDER_EMAIL')):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    msg.set_content(message)

    try:
        server = smtplib.SMTP(server, port)
        server.set_debuglevel(1)  # Enable debugging output
        server.starttls()  # Enable TLS encryption
        # Use environment variables for credentials
        email_password = os.getenv('EMAIL_PASSWORD')  # Replace with your environment variable name
        server.login(from_email, email_password)
        server.send_message(msg)
        print('Successfully sent the mail.')
    except Exception as e:
        print(f'Failed to send email: {e}')
    finally:
        try:
            server.quit()
        except:
            pass

# Example usage
if __name__ == "__main__":
    print(os.getenv('SENDER_EMAIL'))
    
