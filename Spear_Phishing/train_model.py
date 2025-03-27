import pandas as pd
import joblib
import re
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Download NLTK stopwords
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

# Load phishing dataset
df = pd.read_csv("spearphishing.csv")  # Ensure your dataset is in the same directory

# Preprocess the email text
def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'http\\S+', '', text)  # Remove URLs
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = " ".join([word for word in text.split() if word not in STOPWORDS])  # Remove stopwords
    return text

df['cleaned_text'] = df['subject'] + " " + df['body']  # Combine subject & body
df['cleaned_text'] = df['cleaned_text'].apply(clean_text)  # Apply cleaning function

# Convert text into numerical format
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['cleaned_text']).toarray()
y = df['label']

# Split into training & testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "phishing_detector.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

# Evaluate the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
