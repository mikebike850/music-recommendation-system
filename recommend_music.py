import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv('songs.csv')

# Combine features into a single string
df['combined'] = df['artist'] + ' ' + df['genre']

# Vectorize the combined text
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['combined'])

# Calculate cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations
def recommend(song_title):
    if song_title not in df['title'].values:
        return "Song not found. Try another title."

    idx = df[df['title'] == song_title].index[0]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:6]
    recommended_songs = [df.iloc[i[0]]['title'] for i in similarity_scores]
    return recommended_songs

# Test the recommender
user_input = input("Enter a song title: ")
recommendations = recommend(user_input)
print("\nRecommended songs:")
for song in recommendations:
    print("-", song)
