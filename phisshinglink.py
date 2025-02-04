import requests
import json

# SMTP2GO API URL
url = "https://api.smtp2go.com/v3/email/send"

# Your SMTP2GO API key
api_key = "api-B0709E71534F437F9D51290561BE726E"

# Prompt the user for input
sender_email = "bemoh77219@halbov.com"  # Your email address (sender)
recipient_email = input("Enter the recipient's email address: ")
subject = input("Enter the subject of the email: ")
body = input("Enter the body of the email: ")

# Prepare the email data
data = {
    "api_key": api_key,
    "to": [recipient_email],
    "sender": sender_email,
    "subject": subject,
    "text_body": body,  # Plain text body (use "html_body" for HTML emails)
}

# Set headers for JSON content type
headers = {
    "Content-Type": "application/json"
}

# Send the email via POST request
response = requests.post(url, data=json.dumps(data), headers=headers)

# Check the response
if response.status_code == 200:
    print("Email sent successfully!")
else:
    print(f"Failed to send email. Status code: {response.status_code}, Error: {response.text}")

