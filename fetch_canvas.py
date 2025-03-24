import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import json
import re

# Load environment variables
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
print(f"Client ID: {client_id}, Client Secret: {client_secret}")  # Debug

# Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def extract_track_id(spotify_value):
    match = re.search(r'track/([a-zA-Z0-9]+)', spotify_value)
    if match:
        return match.group(1)
    return re.sub(r'\?si=.*', '', spotify_value).strip()

def get_canvas_url(track_id):
    print(f"Go to https://www.canvasdownloader.com/canvas?link=https://open.spotify.com/track/{track_id}")
    print("Solve the CAPTCHA, right-click the video, select 'Copy video address', and paste the URL below.")
    canvas_url = input(f"Paste Canvas URL for {track_id} (or press Enter to skip): ").strip()
    
    if not canvas_url:
        print(f"Skipping Canvas URL for {track_id}")
        return None
    
    if "canvaz.scdn.co" in canvas_url:
        print(f"Valid Canvas URL provided: {canvas_url}")
        response = requests.head(canvas_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            return canvas_url
        else:
            print(f"Canvas URL inaccessible: {response.status_code}")
    else:
        print(f"Invalid URL provided for {track_id}: {canvas_url}")
    return None

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\s]', '', filename).strip()

def fetch_tunebat_data(track_id, title, artist):
    """Prompt user to fetch BPM, release year, and duration from Tunebat.com."""
    clean_artist = re.sub(r'\s*\(Feat\..*?\)', '', artist).strip()
    tunebat_url = f"https://tunebat.com/Info/{title.replace(' ', '-')}-{clean_artist.replace(' ', '-')}/{track_id}"
    print(f"Go to {tunebat_url} to find BPM, Release Year, and Duration.")
    print("Enter the values below (or press Enter to skip each one).")
    
    bpm = input(f"Paste BPM for {title} by {artist} (e.g., 132): ").strip()
    bpm = int(bpm) if bpm else None
    
    releaseYear = input(f"Paste Release Year for {title} by {artist} (e.g., 2024): ").strip()
    releaseYear = releaseYear if releaseYear else None
    
    duration = input(f"Paste Duration for {title} by {artist} (e.g., 3m 01s): ").strip()
    duration = duration if duration else None  # Expecting "0m 00s" format
    
    print(f"Tunebat manual input - BPM: {bpm}, Release Year: {releaseYear}, Duration: {duration}")
    return bpm, releaseYear, duration

def fetch_spotify_metadata(track_id, entry):
    clean_track_id = extract_track_id(track_id)
    print(f"Fetching Spotify metadata for track_id: {clean_track_id}")
    
    # Initialize variables to avoid UnboundLocalError
    title = entry.get("title", "UnknownTitle")
    artist = entry.get("artist", "UnknownArtist")
    preview_url = None
    
    # Skip API call if previewUrl exists and is valid
    existing_preview = entry.get("previewUrl")
    if existing_preview and existing_preview != "null":
        print(f"Existing previewUrl found: {existing_preview}. Skipping Spotify API fetch.")
        preview_url = existing_preview
    else:
        try:
            track = sp.track(clean_track_id, market="US")
            title = track.get("name", "UnknownTitle")
            artist = track["artists"][0].get("name", "UnknownArtist")
            preview_url = track.get("preview_url")
            print(f"Spotify response - Title: {title}, Artist: {artist}, Preview URL: {preview_url}")
            if preview_url is None:
                print(f"Warning: No preview URL in API for {clean_track_id}. You can manually provide one.")
                manual_url = input(f"Paste preview URL for {clean_track_id} (e.g., from https://p.scdn.co/mp3-preview/...) or press Enter to skip: ").strip()
                preview_url = manual_url if manual_url else None
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API error for {clean_track_id}: {e}. Using JSON metadata.")
    
    # Fetch Tunebat data manually
    bpm, releaseYear, duration = fetch_tunebat_data(clean_track_id, title, artist)
    
    return title, artist, preview_url, bpm, releaseYear, duration

def download_video(track_id, url, entry):
    title, artist, preview_url, bpm, releaseYear, duration = fetch_spotify_metadata(track_id, entry)
    entry["previewUrl"] = preview_url
    entry["bpm"] = bpm
    entry["releaseYear"] = releaseYear
    entry["duration"] = duration
    
    if not url:
        print(f"No Canvas URL for {track_id}, skipping download but updated metadata")
        return None
    
    video_filename_base = f"{title}.mp4"
    sanitized_filename = sanitize_filename(video_filename_base)
    video_path = f"assets/preview/{sanitized_filename}"
    response = requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.canvasdownloader.com/"})
    if response.status_code == 200:
        os.makedirs("assets/preview", exist_ok=True)
        with open(video_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded video to {video_path}")
        return sanitized_filename
    print(f"Failed to download {url}: {response.status_code}")
    return None

def update_jam_tracks(track_id, video_filename, data):
    if video_filename:
        data[track_id]["videoUrl"] = video_filename

def save_jam_tracks(data, json_path):
    os.makedirs("data", exist_ok=True)
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved updated jam_tracks.json with original object format")

def process_jam_tracks():
    json_path = "data/jam_tracks.json"
    
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
    else:
        print(f"Error: {json_path} not found. Creating an empty object structure.")
        data = {}
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Created {json_path}. Add tracks (e.g., {'24XihnoVPWXlKJ4BgXqjVM': {'spotify': '24XihnoVPWXlKJ4BgXqjVM', 'title': 'Song'}}) and rerun.")
        return
    
    if not isinstance(data, dict):
        print(f"Error: {json_path} must be a JSON object with track IDs as keys.")
        return
    
    print(f"Loaded data: {json.dumps(data, indent=2)}")
    
    # Process tracks missing videoUrl, previewUrl, bpm, releaseYear, or duration
    tracks_to_process = {track_id: entry for track_id, entry in data.items() 
                         if "spotify" in entry and (
                             "videoUrl" not in entry or not entry["videoUrl"] or 
                             "previewUrl" not in entry or entry["previewUrl"] is None or 
                             "bpm" not in entry or "releaseYear" not in entry or "duration" not in entry
                         )}
    
    if not tracks_to_process:
        print("All tracks in jam_tracks.json already have complete metadata.")
        save_jam_tracks(data, json_path)
        return
    
    print(f"Found {len(tracks_to_process)} tracks needing updates.")
    
    for track_id, entry in tracks_to_process.items():
        spotify_id = entry["spotify"]
        clean_spotify_id = extract_track_id(spotify_id)
        print(f"\nProcessing {track_id} (Spotify ID: {spotify_id}, Cleaned ID: {clean_spotify_id})")
        canvas_url = get_canvas_url(clean_spotify_id)
        video_filename = download_video(spotify_id, canvas_url, entry)
        if video_filename:
            update_jam_tracks(track_id, video_filename, data)
        else:
            print(f"No video downloaded for {track_id}, but metadata may have been updated")
    
    save_jam_tracks(data, json_path)

if __name__ == "__main__":
    process_jam_tracks()