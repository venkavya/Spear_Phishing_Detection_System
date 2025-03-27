import streamlit as st
import joblib
from fetch_emails import fetch_unread_emails

# Load trained model and vectorizer
model = joblib.load("phishing_detector.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def detect_phishing(email_subject, email_body):
    """Predict if an email is phishing or safe."""
    email_text = email_subject + " " + email_body
    email_vector = vectorizer.transform([email_text]).toarray()
    prediction = model.predict(email_vector)[0]
    return "🚨 Phishing Email!" if prediction == 1 else "✅ Safe Email"

# Streamlit UI
st.title("📧 Spear Phishing Detection System")
st.write("Enter email details below to check if it's phishing.")

email_subject = st.text_input("Email Subject")
email_body = st.text_area("Email Body")

if st.button("Check Email"):
    result = detect_phishing(email_subject, email_body)
    st.subheader(result)

if st.button("Fetch & Scan Unread Emails"):
    emails = fetch_unread_emails()
    for email in emails:
        st.write(f"🔍 Checking: {email[:100]}...")
        result = detect_phishing("Suspicious Email", email)
        st.write(f"🛑 Detection Result: {result}")

