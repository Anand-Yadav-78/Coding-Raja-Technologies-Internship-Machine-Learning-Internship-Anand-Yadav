# -*- coding: utf-8 -*-
"""Anand-Yadav-CR-ML-Intern-T1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iesidQixfSoFNJk9wL3D_Twzwv_1KjDi

# Machine Learning model for Sentimental Analysis of socia media posts

# Step 1: Importing Libraries
"""

# Import important libraries
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

"""# Step 2: Loading data"""

# Load your dataset
df = pd.read_csv("/content/drive/MyDrive/Inter/Codingraja/ML Intern/Tasks/Task-1/sentiment_tweets3.csv")

"""# Step 3: Handling Missing Values"""

# Check for missing values in the entire dataframe
print("Missing values in each column:\n", df.isnull().sum())

# Drop rows with missing values in any column (if necessary)
df = df.dropna()

"""# Step 4: Data Preprocessing"""

# Mapping numerical labels to sentiment strings
df['label (depression result)'] = df['label (depression result)'].map({0: 'negative', 1: 'positive'})

# Display the distribution of labels
print(df['label (depression result)'].value_counts())

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# Function for text preprocessing
def preprocess_text(text):
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    text = text.lower()
    text = text.strip()
    # Tokenize the text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return " ".join(filtered_tokens)

# Apply text preprocessing to the dataset
df['cleaned_text'] = df['message to examine'].apply(preprocess_text)

"""# Step 5: Feature Extraction"""

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000)

# Transform the text data
X = tfidf_vectorizer.fit_transform(df['cleaned_text'])

# Convert sentiment labels to numerical values
y = df['label (depression result)'].map({'positive': 1, 'negative': 0})

# Ensure no NaN values remain
y = y.dropna()

# Ensure the data type of y is integer
y = y.astype(int)

# Ensure X and y are aligned
print(f"Shape of X: {X.shape}")
print(f"Shape of y: {y.shape}")

"""# Step 6: Model Selection"""

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the SVM classifier
svm_classifier = SVC(kernel='linear', probability=True)

"""# Step 7: Model Training"""

# Train the SVM classifier
svm_classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = svm_classifier.predict(X_test)

"""# Step 8: Model Evaluation and Analysis

---


"""

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")
print("\nClassification Report:\n", classification_report(y_test, y_pred))