import pandas as pd
import spacy

nlp = spacy.load("en_core_web_md")

# Load dataset
df = pd.read_csv("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv", encoding="utf-8")

# Remove missing values
clean_data = df.dropna(subset=["reviews.text"]).copy()

# Clean data and remove stop words ect.
def preprocess_text(text):
    doc = nlp(str(text).lower().strip())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and token.is_alpha
    ]
    return " ".join(tokens)

# Process data
clean_data["cleaned_reviews"] = clean_data["reviews.text"].apply(preprocess_text)

print(clean_data[["reviews.text", "cleaned_reviews"]].head())
