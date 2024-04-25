#!pip install spotipy --upgrade
#!pip install python-dotenv
#!pip install python-dotenv
#!pip install sqlalchemy
#!pip install pymysql
#!pip install mysql-connector-python

#################### Sprint 02 | ETL - Dataset Collection #################### 

### Import Libraries ### CONSOLIDATE IMPORTS
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from sqlalchemy import create_engine
import pymysql

### Set Spotify API credentials ###

# Load environment variables from .env file
#load_dotenv('config.env')

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.environ.get('71ffd2a8db564881bd87cb36b3d59e0d')
SPOTIPY_CLIENT_SECRET = os.environ.get('41df7974594b4bf99cd65bab9793c8c5')

# initialize Spotipy with client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                      client_secret=SPOTIPY_CLIENT_SECRET)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

### Get Spotify API Data ###
# https://everynoise.com/worldbrowser.cgi
def get_playlist_features(playlist_ids):
    
    playlist = spotify.playlist(playlist_ids)
    playlist_id = playlist_ids
    playlist_name = playlist['name']
    playlist_description = playlist['description']
    playlist_followers = playlist['followers']['total']
    playlist_owner = playlist['owner']['display_name']
    playlist_public = playlist['public']
    playlist_snapshot_id = playlist['snapshot_id']
    
    tracks = playlist['tracks']['items']
    
    playlist_features = []
    
    for track in tracks:
        track_info = {
            'track_id': track['track']['id'],
            'track_name': track['track']['name'],
            'track_album': track['track']['album']['name'],
            'track_release_date': track['track']['album']['release_date'],
            'track_popularity': track['track']['popularity'],
            'track_duration_sec': track['track']['duration_ms'] * 0.001,
            #'track_preview_url': track['track']['preview_url'],
            #'track_cover_art_url': track['track']['album']['images'][0]['url'],
            #'track_external_url': track['track']['external_urls']['spotify'],
            #'track_album_number': track['track']['track_number'],
            'track_explicit': track['track']['explicit'],
            #'track_available_markets': track['track']['available_markets'],
            #'track_album_type': track['track']['album']['album_type'],
            #'track_added_on_playlist_date': datetime.strptime(track['added_at'], "%Y-%m-%d"),
            #'track_added_on_playlist_by': track['added_by'],
            #'artist_name': track['track']['artists'][0]['name'],
            'track_all_artists': [artist['name'] for artist in track['track']['artists']],
        }
        
        # Get audio features of the track
        track_id = track['track']['id']  # Extract track ID from the dictionary
        audio_features = spotify.audio_features([track_id])[0]  # Pass track ID as a list
        if audio_features is not None:
            track_info.update(audio_features)  # Use update instead of append to merge dictionaries
        else:
            # Handle the case where audio features are not available for the track
            # For example, you can set default values or skip appending this track_info
            pass
        
        # Getting genres and followers for the main artist of the track
        artist_info = spotify.artist(track['track']['artists'][0]['id'])
        track_info['artist_id'] = artist_info['id']
        track_info['artist_name'] = artist_info['name']
        track_info['artist_genres'] = artist_info['genres']
        track_info['artist_followers'] = artist_info['followers']['total']
        #track_info['artist_external_urls'] = artist_info['external_urls']['spotify']
        #track_info['artist_images'] = artist_info['images']['url']
        track_info['artist_popularity'] = artist_info['popularity']

        # Getting additional playlist information
        track_info['playlist_id'] = playlist_id
        track_info['playlist_name'] = playlist_name
        track_info['playlist_description'] = playlist_description
        track_info['playlist_followers'] = playlist_followers
        #track_info['playlist_owner'] = playlist_owner
        #track_info['playlist_public'] = playlist_public
        track_info['playlist_snapshot_id'] = playlist_snapshot_id
        
        playlist_features.append(track_info)
    
    return playlist_features

### Dictionary of Spotify Playlists ###
playlists = {
    # https://everynoise.com/worldbrowser.cgi
    "Top 50 - Global": "37i9dQZEVXbMDoHDwVN2tF",
    "Top 50 - USA": "37i9dQZEVXbLRQDuF5jeBp",
    "Viral 50 - Global": "37i9dQZEVXbLiRSasKsNU9",
    "Viral 50 - USA": "37i9dQZEVXbKuaTI1Z1Afx",
    "Billboard Hot 100": "6UeSakyzhiEt4NB3UAd6NQ",
    "Signed XOXO": "37i9dQZF1DX2A29LI7xHn1",
    "RapCaviar": "37i9dQZF1DX0XUsuxWHRQd",
    "Viva Latino": "37i9dQZF1DX10zKzsJ2jva",
    "Baila Reggaeton": "37i9dQZF1DWY7IeIP1cdjF",
    "Pop Rising": "37i9dQZF1DWUa8ZRTfalHk",
    "MARROW": "37i9dQZF1DXcF6B6QPhFDv",
    "All New Rock": "37i9dQZF1DWZryfp6NSvtz",
    "mint": "37i9dQZF1DX4dyzvuaRJ0n",
    "Front Page Indie": "37i9dQZF1DX2Nc3B70tvx0",
    "Chill Pop": "37i9dQZF1DX0MLFaUdXnjA",
    "Fresh Finds Country": "37i9dQZF1DWYUfsq4hxHWP",
    "RNB X": "37i9dQZF1DX4SBhb3fqCJd",
    "African Heat": "37i9dQZF1DWYkaDif7Ztbp",
    "K-Pop Rising": "37i9dQZF1DX4FcAKI5Nhzq",
    "Yalla": "37i9dQZF1DX5cO1uP1XC1g",
    "Hot Hits USA": "37i9dQZF1DX0kbJZpiYdZl",
    "Dance Rising": "37i9dQZF1DX8tZsk68tuDw",
    "Feelin' Myself": "37i9dQZF1DX6GwdWRQMQpq",
    #"Most Necessary": "37i9dQZF1DX2RxBh64BHjQ",
    "Alternative Hip-Hop": "37i9dQZF1DWTggY0yqBxES",
    "CST": "37i9dQZF1DX91gZ5XTbTPm",
    "Westside Story": "37i9dQZF1DWSvKsRPPnv5o",
    "New Joints": "37i9dQZF1DX4SrOBCjlfVi",
    "Hot Hits USA": "37i9dQZF1DX0kbJZpiYdZl",
    "sad hour": "37i9dQZF1DWSqBruwoIXkA",
    "Homegrown + Heavy": "37i9dQZF1DXdO9cVSlXgg6",
    "Fuego #052 - Regina's Fan Mixtape": "37i9dQZF1DWTwf6UlOz1Hs",
    "Fuego": "37i9dQZF1DX8sljIJzI0oo",
    "ALT NOW": "37i9dQZF1DWVqJMsgEN0F4",
    "The New Alt": "37i9dQZF1DX82GYcclJ3Ug",
    "New Noise": "37i9dQZF1DWT2jS7NwYPVI",
    "Today's Indie Rock": "37i9dQZF1DX30HHrCAl4ZG",
    "bossa pop": "37i9dQZF1DXcUY9O5yRihK",
    "Spring Pop 🌸": "37i9dQZF1DX9nkam6FKfgM",
    "New Pop Picks": "37i9dQZF1DX11otjJ7crqp",
    "Gulf & Western": "37i9dQZF1DWUPRADzDnbMq",
    "Country Rocks": "37i9dQZF1DWWH0izG4erma",
    "Country Rap": "37i9dQZF1DWXbiccytJ5L7",
    #"Cosmic Country": "37i9dQZF1DX6sc3Xn6L2DK",
    "Hot Country": "37i9dQZF1DX1lVhptIYRda",
    #"Dancehall Official": "37i9dQZF1DXan38dNVDdl4",
    "it's alt good": "37i9dQZF1DX2SK4ytI2KAZ",
    "The Scene": "37i9dQZF1DWZkHEX2YHpDV",
    "Alternative Beats": "37i9dQZF1DWXMg4uP5o3dm",
    "Soak Up The Sun": "37i9dQZF1DX6ALfRKlHn1t",
    "K-Pop ON! (온)": "37i9dQZF1DX9tPFwDMOaN1"
}

# Sort by keys and create a list of tuples
#sorted_dict_by_keys = sorted(playlists.items())

# Create a new dictionary from the sorted list of tuples
#sorted_playlists = dict(sorted_dict_by_keys)

### Append Spotify playlist data to `final_df` ###

# Create empty final dataframe
final_df = pd.DataFrame()

# Get current date and time
current_datetime = datetime.now()
month_day_year = current_datetime.strftime('%m-%d-%Y')

# Gather playlist data one by one and append to `final_df` 
try:
    features = get_playlist_features(playlists['Top 50 - Global'])
    df_1 = pd.DataFrame(features) 
    df_1['playlist_date'] = month_day_year
    final_df = final_df.append(df_1)
    print(final_df.playlist_name.unique())
except Exception as e:
    print(f"Error processing playlist 'Top 50 - Global': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Top 50 - USA'])
    df_2 = pd.DataFrame(features) 
    df_2['playlist_date'] = month_day_year
    final_df = final_df.append(df_2)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Top 50 - USA': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Viral 50 - Global'])
    df_3 = pd.DataFrame(features) 
    df_3['playlist_date'] = month_day_year
    final_df = final_df.append(df_3)
    print(final_df.playlist_name.unique())
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Viral 50 - Global': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Viral 50 - USA'])
    df_4 = pd.DataFrame(features) 
    df_4['playlist_date'] = month_day_year
    final_df = final_df.append(df_4)
    print(final_df.playlist_name.unique())
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Viral 50 - USA': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Billboard Hot 100'])
    df_5 = pd.DataFrame(features) 
    df_5['playlist_date'] = month_day_year
    final_df = final_df.append(df_5)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Billboard Hot 100': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['RapCaviar'])
    df_6 = pd.DataFrame(features) 
    df_6['playlist_date'] = month_day_year
    final_df = final_df.append(df_6)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'RapCaviar': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Signed XOXO'])
    df_7 = pd.DataFrame(features) 
    df_7['playlist_date'] = month_day_year
    final_df = final_df.append(df_7)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Signed XOXO': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

    
try:
    features = get_playlist_features(playlists['Viva Latino'])
    df_8 = pd.DataFrame(features) 
    df_8['playlist_date'] = month_day_year
    final_df = final_df.append(df_8)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Viva Latino': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Baila Reggaeton'])
    df_9 = pd.DataFrame(features) 
    df_9['playlist_date'] = month_day_year
    final_df = final_df.append(df_9)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Baila Reggaeton': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Pop Rising'])
    df_10 = pd.DataFrame(features) 
    df_10['playlist_date'] = month_day_year
    final_df = final_df.append(df_10)
    print(final_df.playlist_name.unique())
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Pop Rising': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['MARROW'])
    df_11 = pd.DataFrame(features) 
    df_11['playlist_date'] = month_day_year
    final_df = final_df.append(df_11)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'MARROW': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['All New Rock'])
    df_12 = pd.DataFrame(features) 
    df_12['playlist_date'] = month_day_year
    final_df = final_df.append(df_12)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'All New Rock': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['mint'])
    df_13 = pd.DataFrame(features) 
    df_13['playlist_date'] = month_day_year
    final_df = final_df.append(df_13)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'mint': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Front Page Indie'])
    df_14 = pd.DataFrame(features) 
    df_14['playlist_date'] = month_day_year
    final_df = final_df.append(df_14)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Front Page Indie': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

try:
    features = get_playlist_features(playlists['Chill Pop'])
    df_15 = pd.DataFrame(features) 
    df_15['playlist_date'] = month_day_year
    final_df = final_df.append(df_15)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Chill Pop': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Fresh Finds Country'])
    df_16 = pd.DataFrame(features) 
    df_16['playlist_date'] = month_day_year
    final_df = final_df.append(df_16)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Fresh Finds Country': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['RNB X'])
    df_17 = pd.DataFrame(features) 
    df_17['playlist_date'] = month_day_year
    final_df = final_df.append(df_17)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'RNB X': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['African Heat'])
    df_18 = pd.DataFrame(features) 
    df_18['playlist_date'] = month_day_year
    final_df = final_df.append(df_18)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'African Heat': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['K-Pop Rising'])
    df_19 = pd.DataFrame(features) 
    df_19['playlist_date'] = month_day_year
    final_df = final_df.append(df_19)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'K-Pop Rising': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Yalla'])
    df_20 = pd.DataFrame(features) 
    df_20['playlist_date'] = month_day_year
    final_df = final_df.append(df_20)
    print(final_df.playlist_name.unique())
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Yalla': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

try:
    features = get_playlist_features(playlists['Dance Rising'])
    df_21 = pd.DataFrame(features) 
    df_21['playlist_date'] = month_day_year
    final_df = final_df.append(df_21)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Dance Rising': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['sad hour'])
    df_22 = pd.DataFrame(features) 
    df_22['playlist_date'] = month_day_year
    final_df = final_df.append(df_22)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'sad hour': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Alternative Hip-Hop'])
    df_23 = pd.DataFrame(features) 
    df_23['playlist_date'] = month_day_year
    final_df = final_df.append(df_23)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Alternative Hip-Hop': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['K-Pop ON! (온)'])
    df_24 = pd.DataFrame(features) 
    df_24['playlist_date'] = month_day_year
    final_df = final_df.append(df_24)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'K-Pop ON! (온)': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists['Hot Hits USA'])
    df_25 = pd.DataFrame(features) 
    df_25['playlist_date'] = month_day_year
    final_df = final_df.append(df_25)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Hot Hits USA': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["it's alt good"])
    df_26 = pd.DataFrame(features) 
    df_26['playlist_date'] = month_day_year
    final_df = final_df.append(df_26)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist it's alt good: {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds) 
    
try:
    features = get_playlist_features(playlists["Spring Pop 🌸"])
    df_27 = pd.DataFrame(features) 
    df_27['playlist_date'] = month_day_year
    final_df = final_df.append(df_27)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist Spring Pop 🌸: {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["Fuego"])
    df_28 = pd.DataFrame(features) 
    df_28['playlist_date'] = month_day_year
    final_df = final_df.append(df_28)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Fuego': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

try:
    features = get_playlist_features(playlists["Today's Indie Rock"])
    df_29 = pd.DataFrame(features) 
    df_29['playlist_date'] = month_day_year
    final_df = final_df.append(df_29)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Today's Indie Rock': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

try:
    features = get_playlist_features(playlists["The Scene"])
    df_30 = pd.DataFrame(features) 
    df_30['playlist_date'] = month_day_year
    final_df = final_df.append(df_30)
    print(final_df.playlist_name.unique())
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'The Scene': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["Feelin' Myself"])
    df_31 = pd.DataFrame(features) 
    df_31['playlist_date'] = month_day_year
    final_df = final_df.append(df_31)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Feelin' Myself': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["ALT NOW"])
    df_32 = pd.DataFrame(features) 
    df_32['playlist_date'] = month_day_year
    final_df = final_df.append(df_32)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'ALT NOW': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

try:
    features = get_playlist_features(playlists["New Joints"])
    df_33 = pd.DataFrame(features) 
    df_33['playlist_date'] = month_day_year
    final_df = final_df.append(df_33)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'New Joints': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

try:
    features = get_playlist_features(playlists["Soak Up The Sun"])
    df_34 = pd.DataFrame(features) 
    df_34['playlist_date'] = month_day_year
    final_df = final_df.append(df_34)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Soak Up The Sun': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["Hot Country"])
    df_35 = pd.DataFrame(features) 
    df_35['playlist_date'] = month_day_year
    final_df = final_df.append(df_35)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Hot Country': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

try:
    features = get_playlist_features(playlists["Alternative Beats"])
    df_36 = pd.DataFrame(features) 
    df_36['playlist_date'] = month_day_year
    final_df = final_df.append(df_36)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Alternative Beats': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["Homegrown + Heavy"])
    df_37 = pd.DataFrame(features) 
    df_37['playlist_date'] = month_day_year
    final_df = final_df.append(df_37)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Homegrown + Heavy': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["New Pop Picks"])
    df_38 = pd.DataFrame(features) 
    df_38['playlist_date'] = month_day_year
    final_df = final_df.append(df_38)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'New Pop Picks': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
        
try:
    features = get_playlist_features(playlists["Westside Story"])
    df_39 = pd.DataFrame(features) 
    df_39['playlist_date'] = month_day_year
    final_df = final_df.append(df_39)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Westside Story': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

try:
    features = get_playlist_features(playlists["Fuego #052 - Regina's Fan Mixtape"])
    df_40 = pd.DataFrame(features) 
    df_40['playlist_date'] = month_day_year
    final_df = final_df.append(df_40)
    print(final_df.playlist_name.unique())
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Fuego #052 - Regina's Fan Mixtape': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["Gulf & Western"])
    df_41 = pd.DataFrame(features) 
    df_41['playlist_date'] = month_day_year
    final_df = final_df.append(df_41)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Gulf & Western': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["New Noise"])
    df_42 = pd.DataFrame(features) 
    df_42['playlist_date'] = month_day_year
    final_df = final_df.append(df_42)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'New Noise': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["The New Alt"])
    df_43 = pd.DataFrame(features) 
    df_43['playlist_date'] = month_day_year
    final_df = final_df.append(df_43)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'The New Alt': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["bossa pop"])
    df_44 = pd.DataFrame(features) 
    df_44['playlist_date'] = month_day_year
    final_df = final_df.append(df_44)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'bossa pop': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["CST"])
    df_45 = pd.DataFrame(features) 
    df_45['playlist_date'] = month_day_year
    final_df = final_df.append(df_45)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'CST': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["Country Rocks"])
    df_46 = pd.DataFrame(features) 
    df_46['playlist_date'] = month_day_year
    final_df = final_df.append(df_46)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Country Rocks': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
    
try:
    features = get_playlist_features(playlists["Country Rap"])
    df_46 = pd.DataFrame(features) 
    df_46['playlist_date'] = month_day_year
    final_df = final_df.append(df_46)
    print(final_df.playlist_name.unique())
    minutes = 1
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)
except Exception as e:
    print(f"Error processing playlist 'Country Rap': {e}")
    minutes = 10
    seconds = minutes * 60
    print(f"Sleeping for {minutes} minutes...")
    time.sleep(seconds)

### Final Changes to Final_df before Exporting ##
#final_df['mode'] = final_df['mode'].replace({0: 'minor', 1: 'major'})
final_df = final_df.drop(['mode', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)

### Export the `final_df` DataFrame as a CSV file to directory ###

# Get current date and time
current_datetime = datetime.now()

# Format the date and time to include in the file name
timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")

# Construct the file name with timestamp
file_name = f'bulk_data_{timestamp}.csv'

# Specify the path to the 'data' subfolder relative to the current directory
data_folder = os.path.join('data')

# Ensure that the 'data' subfolder exists, create it if it doesn't
os.makedirs(data_folder, exist_ok=True)

# Construct the file path within the 'data' subfolder
file_path = os.path.join(data_folder, file_name)

# Save the DataFrame as a CSV file to the 'data' subfolder
final_df.to_csv(file_path, index=False)

# Print confirmation messages
print(f"DataFrame saved as CSV file: {file_path}")
print("Sprint 02 | ETL - Dataset Collection: Status: Completed")

#################### Sprint 02 | ETL - Database Connection #################### 
print("Sprint 02 | ETL - Database Connection: Status: Starting")

### Get latest data file from data - Sprint 02 folder in directory ### 

# Specify the path to the 'data' subfolder
data_folder = 'data'

# Get a list of all CSV files in the 'data' subfolder
csv_files = [os.path.join(data_folder, file) for file in os.listdir(data_folder) if file.endswith('.csv') and file.startswith('bulk_data_')]

# Check if any CSV files exist in the 'data' subfolder
if not csv_files:
    raise FileNotFoundError("No CSV files found in the 'data' subfolder with the specified prefix.")

# Sort CSV files by modification time (most recent first)
csv_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

# Select the most recent CSV file
latest_csv_file = csv_files[0]

# Read in the most recent CSV file
final_df = pd.read_csv(latest_csv_file)

# Print the name of the file being read
print(f"Reading DataFrame from CSV file: {latest_csv_file}")

### Connect to Database ###

# Load environment variables from .env file
#load_dotenv('config.env')

# Get database credentials from environment variables
username = 'bsan6060'
password = 'awsBSAN6060'
host = 'j-lavender-bsan.clw6q2u2kfpj.us-west-1.rds.amazonaws.com'
port = '3306'
database_name = 'spotify_6080_sprint02_test'

# Construct the database URL
url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"

def fetch_data_from_database():
    # Create the SQLAlchemy engine using the connection from connect_to_database()
    engine = create_engine(url)
    
    # Fetch data from tables
    try:
        with engine.connect() as conn:
            # Fetch data from dim_track table
            dim_track_df = pd.read_sql_table("dim_track", conn)
            # Fetch data from dim_artist table
            dim_artist_df = pd.read_sql_table("dim_artist", conn)
            # Fetch data from fact_playlist table
            fact_playlist_df = pd.read_sql_table("fact_playlist", conn)
            # Fetch data from intermediate_table table
            intermediate_table_df = pd.read_sql_table("intermediate_table", conn)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None, None, None

    return dim_track_df, dim_artist_df, fact_playlist_df, intermediate_table_df

dim_track_df, dim_artist_df, fact_playlist_df, intermediate_table_df = fetch_data_from_database()
print("Database Connection: Successful")

### Data Transformations ###
def fact_table_pre_aggregates(df):
    # Perform aggregation operations on a DataFrame containing playlist-related data
    # Group by playlist_id and calculate various aggregate metrics
    return df.groupby('playlist_id').agg(
        playlist_name=('playlist_name', 'last'),
        playlist_description=('playlist_description', 'last'),
        playlist_followers=('playlist_followers', 'last'),
        #playlist_date=('playlist_date', 'first'),
        #AVG_track_release_date_by_playlist=('track_release_date', 'mean'),
        AVG_track_popularity_by_playlist=('track_popularity', 'mean'),
        AVG_track_duration_sec_by_playlist=('track_duration_sec', 'mean'),
        RATIO_track_explicit_by_playlist=('track_explicit', lambda x: x.sum() / len(x)),
        AVG_danceability_by_playlist=('danceability', 'mean'),
        AVG_energy_by_playlist=('energy', 'mean'),
        AVG_loudness_by_playlist=('loudness', 'mean'),
        AVG_speechiness_by_playlist=('speechiness', 'mean'),
        AVG_acousticness_by_playlist=('acousticness', 'mean'),
        AVG_instrumentalness_by_playlist=('instrumentalness', 'mean'),
        AVG_liveness_by_playlist=('liveness', 'mean'),
        AVG_valence_by_playlist=('valence', 'mean'),
        AVG_tempo_by_playlist=('tempo', 'mean'),
        AVG_artist_followers_by_playlist=('artist_followers', 'mean'),
        AVG_artist_popularity_by_playlist=('artist_popularity', 'mean')
    ).reset_index()

def fact_table_aggregates(df):
    # Perform aggregation operations on a DataFrame containing playlist-related data
    # Group by playlist_id and calculate various aggregate metrics
    return df.groupby('playlist_id').agg(
        playlist_name=('playlist_name', 'last'),
        playlist_description=('playlist_description', 'last'),
        playlist_followers=('playlist_followers', 'last'),
        #playlist_date=('playlist_date', 'first'),
        #AVG_track_release_date_by_playlist=('track_release_date', 'mean'),
        AVG_track_popularity_by_playlist=('AVG_track_popularity_by_playlist', 'mean'),
        AVG_track_duration_sec_by_playlist=('AVG_track_duration_sec_by_playlist', 'mean'),
        RATIO_track_explicit_by_playlist=('RATIO_track_explicit_by_playlist', 'mean'),
        AVG_danceability_by_playlist=('AVG_danceability_by_playlist', 'mean'),
        AVG_energy_by_playlist=('AVG_energy_by_playlist', 'mean'),
        AVG_loudness_by_playlist=('AVG_loudness_by_playlist', 'mean'),
        AVG_speechiness_by_playlist=('AVG_speechiness_by_playlist', 'mean'),
        AVG_accousticness_by_playlist=('AVG_accousticness_by_playlist', 'mean'),
        AVG_instrumentalness_by_playlist=('AVG_instrumentalness_by_playlist', 'mean'),
        AVG_liveness_by_playlist=('AVG_liveness_by_playlist', 'mean'),
        AVG_valence_by_playlist=('AVG_valence_by_playlist', 'mean'),
        AVG_tempo_by_playlist=('AVG_tempo_by_playlist', 'mean'),
        AVG_artist_followers_by_playlist=('AVG_artist_followers_by_playlist', 'mean'),
        AVG_artist_popularity_by_playlist=('AVG_artist_popularity_by_playlist', 'mean')
    ).reset_index()

def ingest_new_data(dim_track_df, dim_artist_df, fact_playlist_df, intermediate_table_df, new_data_df):
    # Initialize DataFrames if they are None
    if dim_track_df is None:
        dim_track_df = pd.DataFrame(columns=[
            'track_id', 'track_name', 'track_album', 'track_release_date', 'track_popularity',
            'track_duration_sec', 'track_explicit', 'track_all_artists', 'danceability',
            'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'tempo', 'time_signature', 'playlist_date'
        ])
    if dim_artist_df is None:
        dim_artist_df = pd.DataFrame(columns=[
            'artist_id', 'artist_name', 'artist_genres', 
            'artist_followers', 'artist_popularity', 'playlist_date'
        ])
    if fact_playlist_df is None:
        fact_playlist_df = pd.DataFrame(columns=[
            'playlist_id', 'playlist_name', 'playlist_description','playlist_followers',
            'AVG_track_popularity_by_playlist', 'AVG_track_duration_sec_by_playlist',
            'RATIO_track_explicit_by_playlist', 'AVG_danceability_by_playlist',
            'AVG_energy_by_playlist','AVG_loudness_by_playlist', 'AVG_speechiness_by_playlist',
            'AVG_accousticness_by_playlist','AVG_instrumentalness_by_playlist',
            'AVG_liveness_by_playlist','AVG_valence_by_playlist','AVG_tempo_by_playlist',
            'AVG_artist_followers_by_playlist','AVG_artist_popularity_by_playlist',
        ])
        fact_playlist_df = fact_table_aggregates(new_data_df)
    
    if intermediate_table_df is None:
        intermediate_table_df = pd.DataFrame(columns=[
            'track_id', 'artist_id', 'playlist_id', 
            'playlist_snapshot_id', 'playlist_date'
        ])
    
    # Append new data to the existing DataFrames
    if not new_data_df.empty:
        
        # Append and convert playlist_date to datetime data type for dim_track_df
        dim_track_df = dim_track_df.append(new_data_df[[
            'track_id', 'track_name', 'track_album', 'track_release_date', 'track_popularity',
            'track_duration_sec', 'track_explicit', 'track_all_artists', 'danceability',
            'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'tempo', 'time_signature', 'playlist_date']])
        dim_track_df['playlist_date'] = pd.to_datetime(dim_track_df['playlist_date'])
        # Check if the DataFrame is not empty
        if not dim_track_df.empty:
            # Sort the DataFrame by playlist_date within each group of track_id
            dim_track_df = dim_track_df.sort_values(by=['track_id', 'playlist_date'], ascending=[True, False])
            # Select the first row of each group (corresponding to the most recent playlist_date)
            dim_track_df = dim_track_df.groupby('track_id').first().reset_index()
    
        # Append and convert playlist_date to datetime data type for dim_artist_df
        dim_artist_df = dim_artist_df.append(new_data_df[[
            'artist_id', 'artist_name', 'artist_genres', 
            'artist_followers', 'artist_popularity', 'playlist_date']])
        dim_artist_df['playlist_date'] = pd.to_datetime(dim_artist_df['playlist_date'])
        # Check if the DataFrame is not empty
        if not dim_artist_df.empty:
            # Sort the DataFrame by playlist_date within each group of artist_id
            dim_artist_df = dim_artist_df.sort_values(by=['artist_id', 'playlist_date'], ascending=[True, False])
            # Select the first row of each group (corresponding to the most recent playlist_date)
            dim_artist_df = dim_artist_df.groupby('artist_id').first().reset_index()
            
        # Append new data to fact_playlist_df
        aggregated_new_data_df = fact_table_pre_aggregates(new_data_df)
        fact_playlist_df = pd.concat([fact_playlist_df, aggregated_new_data_df], ignore_index=True)
        fact_playlist_df = fact_table_aggregates(fact_playlist_df)
        fact_playlist_df = fact_playlist_df.drop_duplicates(subset=['playlist_id']).reset_index(drop=True)

        # Append and convert playlist_date to datetime data type for intermediate_table_df
        intermediate_table_df = intermediate_table_df.append(new_data_df[[
            'track_id', 'artist_id', 'playlist_id', 'playlist_snapshot_id', 'playlist_date'
            ]]).drop_duplicates(subset=['track_id', 'playlist_date', 'playlist_id']).reset_index(drop=True)
        intermediate_table_df['playlist_date'] = pd.to_datetime(intermediate_table_df['playlist_date'])
    
    dim_track_df.drop(columns=['playlist_date'], inplace=True)
    dim_track_df.drop_duplicates(subset=['track_id'])
    dim_artist_df.drop(columns=['playlist_date'], inplace=True)
    dim_artist_df.drop_duplicates(subset=['artist_id'])
    intermediate_table_df.drop_duplicates(subset=['track_id', 'playlist_date', 'playlist_id'], inplace=True)
    
    return dim_track_df, dim_artist_df, fact_playlist_df, intermediate_table_df

dim_track_df, dim_artist_df, fact_playlist_df, intermediate_table_df = ingest_new_data(dim_track_df, dim_artist_df, fact_playlist_df, intermediate_table_df, final_df)

duplicate_rows = dim_track_df[dim_track_df.duplicated(subset=['track_id'], keep=False)]
print(duplicate_rows)

duplicate_rows = dim_artist_df[dim_artist_df.duplicated(subset=['artist_id'], keep=False)]
print(duplicate_rows)

duplicate_rows = fact_playlist_df[fact_playlist_df.duplicated(subset=['playlist_id'], keep=False)]
print(duplicate_rows)

duplicate_rows = intermediate_table_df[intermediate_table_df.duplicated(subset=['track_id', 'playlist_id', 'playlist_date'], keep=False)]
print(duplicate_rows)

### Ingest New Data to Database ###

# Connect to the database
engine = create_engine(url)
    
# Disable foreign key constraints
with engine.connect() as connection:
    connection.execute("SET foreign_key_checks = 0")
    
# Clear existing data from tables
with engine.connect() as connection:
    connection.execute("TRUNCATE TABLE dim_track")
    connection.execute("TRUNCATE TABLE dim_artist")
    connection.execute("TRUNCATE TABLE fact_playlist")
    connection.execute("TRUNCATE TABLE intermediate_table")
    
# Re-enable foreign key constraints
with engine.connect() as connection:
    connection.execute("SET foreign_key_checks = 1")
    
# Re-ingest updated data into tables
dim_track_df.to_sql('dim_track', con=engine, if_exists='append', index=False)
dim_artist_df.to_sql('dim_artist', con=engine, if_exists='append', index=False)
fact_playlist_df.to_sql('fact_playlist', con=engine, if_exists='append', index=False)
intermediate_table_df.to_sql('intermediate_table', con=engine, if_exists='append', index=False)