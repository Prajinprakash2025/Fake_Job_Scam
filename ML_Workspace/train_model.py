import pandas as pd
from preprocess import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from preprocess import clean_text

# 1. Load dataset
df = pd.read_csv("dataset/job_scam.csv")

# 2. Clean text
df["text"] = df["text"].apply(clean_text)

X = df["text"]
y = df["label"]

# 3. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# 4. TF-IDF vectorization
vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1, 2)
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5. Train model
model = LogisticRegression(max_iter=1000, class_weight="balanced")

model.fit(X_train_vec, y_train)

# 6. Save model and vectorizer
pickle.dump(model, open("scam_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model training completed")
print("✅ scam_model.pkl and vectorizer.pkl saved")
