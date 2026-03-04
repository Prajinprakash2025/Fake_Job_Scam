import pickle
from preprocess import clean_text
from sklearn.metrics import classification_report
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from preprocess import clean_text

# Load dataset
df = pd.read_csv("dataset/job_scam.csv")
df["text"] = df["text"].apply(clean_text)

X = df["text"]
y = df["label"]

# Same split as training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Load trained model
model = pickle.load(open("scam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Transform text
X_test_vec = vectorizer.transform(X_test)

# Predict
y_pred = model.predict(X_test_vec)

# Evaluation
print("\n📊 CLASSIFICATION REPORT\n")
print(classification_report(y_test, y_pred))

print("\n📌 CONFUSION MATRIX\n")
print(confusion_matrix(y_test, y_pred))




