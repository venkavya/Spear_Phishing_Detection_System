import os
import base64
import joblib
import smtplib
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Load trained phishing detection model
model = joblib.load("phishing_detector.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Gmail Authentication
def authenticate_gmail():
    """Load saved Gmail authentication token."""
    creds = None
    if os.path.exists("token.json"):
        creds = joblib.load("token.json")

    if not creds or not creds.valid:
        creds.refresh(Request())

    return build("gmail", "v1", credentials=creds)

# Function to fetch unread emails
def fetch_unread_emails():
    """Fetch unread emails from Gmail inbox."""
    service = authenticate_gmail()
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get("messages", [])

    if not messages:
        print("✅ No unread emails found.")
        return []

    emails = []
    for msg in messages[:5]:  # Fetch latest 5 unread emails
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        email_body = msg_data.get("snippet", "No content")  # Extract email snippet
        emails.append(email_body)
        print(f"📩 Email Snippet: {email_body[:100]}...")

    return emails

# Function to detect phishing
def detect_phishing(email_text):
    """Predict if an email is phishing or safe."""
    email_vector = vectorizer.transform([email_text]).toarray()
    prediction = model.predict(email_vector)[0]
    return "🚨 Phishing Email!" if prediction == 1 else "✅ Safe Email"

# Function to send alert emails
def send_email_alert(phishing_email):
    """Send an email alert when phishing is detected."""
    sender_email = "your-email@gmail.com"  # Replace with your email
    receiver_email = "alert-receiver@gmail.com"  # Replace with recipient email
    sender_password = "your-email-password"  # Replace with app password

    subject = "⚠️ Phishing Email Detected!"
    body = f"🚨 WARNING! A phishing email was detected:\n\n{phishing_email}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("📩 Alert Sent Successfully!")
    except Exception as e:
        print(f"❌ Failed to send email alert: {e}")

# Run the script
if __name__ == "__main__":
    emails = fetch_unread_emails()
    for email in emails:
        result = detect_phishing(email)
        print(f"🔍 Checking Email: {email[:100]}... \n🛑 Detection Result: {result}\n")
        
        if "Phishing" in result:
            send_email_alert(email)  # Send an alert if phishing is detected
