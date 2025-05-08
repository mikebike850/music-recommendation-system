import os
import csv
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load credentials from .env file
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Authenticate with Spotify
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ---------------------------------------------
# Save song to CSV (with duplicate prevention)
def save_song_to_csv(track):
    file_path = 'songs.csv'
    new_title = track['name'].strip().lower()
    new_artist = track['artists'][0]['name'].strip().lower()

    # If the file doesn't exist, create it and write header
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'artist', 'genre'])  # CSV header

    # Check for duplicates
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 2 and row[0].strip().lower() == new_title and row[1].strip().lower() == new_artist:
                print(f"✅ Already in dataset: {track['name']} by {track['artists'][0]['name']}")
                return

    # 🔍 Get artist genre
    artist_id = track['artists'][0]['id']
    artist_info = sp.artist(artist_id)
    genres = artist_info.get('genres', [])
    genre_str = ', '.join(genres) if genres else 'Unknown'

    # 📝 Save to CSV
    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([track['name'], track['artists'][0]['name'], genre_str])
        print(f"🆕 Added to dataset: {track['name']} by {track['artists'][0]['name']} (Genre: {genre_str})")

# ---------------------------------------------
# Search for a song and display/save results
def search_song(song_name):
    results = sp.search(q=song_name, limit=5, type='track')
    tracks = results['tracks']['items']

    if not tracks:
        print("No results found.")
        return

    print(f"\nTop results for: {song_name}\n")
    for idx, track in enumerate(tracks, start=1):
        print(f"{idx}. {track['name']} by {track['artists'][0]['name']}")
        print(f"   Album: {track['album']['name']}")
        print(f"   Popularity: {track['popularity']}")
        print(f"   Preview: {track['preview_url']}")
        print()

        save_song_to_csv(track)

# ---------------------------------------------
# Ask user for a song title
if __name__ == "__main__":
    song_input = input("Enter a song title to search on Spotify: ")
    search_song(song_input)

