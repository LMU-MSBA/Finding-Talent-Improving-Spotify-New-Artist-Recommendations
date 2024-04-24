# -*- coding: utf-8 -*-
"""Sprint 02 _ ETL - Dataset Collection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1urCCMPDRDxq6R-ysz3hHBEx6ouloT3fE

# Sprint 02 | ETL - Dataset Collection

## Dependencies
"""

!pip install spotipy --upgrade

!pip install python-dotenv

### Import Libraries
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

### Set pandas settings
pd.set_option('display.max_columns', None)

"""## Spotify API connection"""

### Set Spotify API credentials

# Load environment variables from .env file
load_dotenv('config.env')

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

# initialize Spotipy with client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                      client_secret=SPOTIPY_CLIENT_SECRET)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""## Get Spotify API data"""

# https://everynoise.com/worldbrowser.cgi

# Replace 'your_client_id' and 'your_client_secret' with your own credentials
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

"""## Dictionary of Spotify playlists"""

### Create dictionary for Spotify Playlists
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
sorted_dict_by_keys = sorted(playlists.items())
# Create a new dictionary from the sorted list of tuples
sorted_playlists = dict(sorted_dict_by_keys)

"""## Append Spotify playlist data to `final_df`"""

### Create empty final dataframe
final_df = pd.DataFrame()

### Get current date and time
current_datetime = datetime.now()
month_day_year = current_datetime.strftime('%m-%d-%Y')

features = get_playlist_features(playlists['Top 50 - Global'])
df_1 = pd.DataFrame(features)
df_1['playlist_date'] = month_day_year
final_df = final_df.append(df_1)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Top 50 - USA'])
df_2 = pd.DataFrame(features)
df_2['playlist_date'] = month_day_year
final_df = final_df.append(df_2)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Viral 50 - Global'])
df_3 = pd.DataFrame(features)
df_3['playlist_date'] = month_day_year
final_df = final_df.append(df_3)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Viral 50 - USA'])
df_4 = pd.DataFrame(features)
df_4['playlist_date'] = month_day_year
final_df = final_df.append(df_4)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Billboard Hot 100'])
df_5 = pd.DataFrame(features)
df_5['playlist_date'] = month_day_year
final_df = final_df.append(df_5)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['RapCaviar'])
df_6 = pd.DataFrame(features)
df_6['playlist_date'] = month_day_year
final_df = final_df.append(df_6)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Signed XOXO'])
df_7 = pd.DataFrame(features)
df_7['playlist_date'] = month_day_year
final_df = final_df.append(df_7)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Viva Latino'])
df_8 = pd.DataFrame(features)
df_8['playlist_date'] = month_day_year
final_df = final_df.append(df_8)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Baila Reggaeton'])
df_9 = pd.DataFrame(features)
df_9['playlist_date'] = month_day_year
final_df = final_df.append(df_9)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Pop Rising'])
df_10 = pd.DataFrame(features)
df_10['playlist_date'] = month_day_year
final_df = final_df.append(df_10)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['MARROW'])
df_11 = pd.DataFrame(features)
df_11['playlist_date'] = month_day_year
final_df = final_df.append(df_11)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['All New Rock'])
df_12 = pd.DataFrame(features)
df_12['playlist_date'] = month_day_year
final_df = final_df.append(df_12)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['mint'])
df_13 = pd.DataFrame(features)
df_13['playlist_date'] = month_day_year
final_df = final_df.append(df_13)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Front Page Indie'])
df_14 = pd.DataFrame(features)
df_14['playlist_date'] = month_day_year
final_df = final_df.append(df_14)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Chill Pop'])
df_15 = pd.DataFrame(features)
df_15['playlist_date'] = month_day_year
final_df = final_df.append(df_15)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Fresh Finds Country'])
df_16 = pd.DataFrame(features)
df_16['playlist_date'] = month_day_year
final_df = final_df.append(df_16)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['RNB X'])
df_17 = pd.DataFrame(features)
df_17['playlist_date'] = month_day_year
final_df = final_df.append(df_17)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['African Heat'])
df_18 = pd.DataFrame(features)
df_18['playlist_date'] = month_day_year
final_df = final_df.append(df_18)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['K-Pop Rising'])
df_19 = pd.DataFrame(features)
df_19['playlist_date'] = month_day_year
final_df = final_df.append(df_19)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Yalla'])
df_20 = pd.DataFrame(features)
df_20['playlist_date'] = month_day_year
final_df = final_df.append(df_20)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Dance Rising'])
df_21 = pd.DataFrame(features)
df_21['playlist_date'] = month_day_year
final_df = final_df.append(df_21)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['sad hour'])
df_22 = pd.DataFrame(features)
df_22['playlist_date'] = month_day_year
final_df = final_df.append(df_22)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Alternative Hip-Hop'])
df_23 = pd.DataFrame(features)
df_23['playlist_date'] = month_day_year
final_df = final_df.append(df_23)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['K-Pop ON! (온)'])
df_24 = pd.DataFrame(features)
df_24['playlist_date'] = month_day_year
final_df = final_df.append(df_24)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists['Hot Hits USA'])
df_25 = pd.DataFrame(features)
df_25['playlist_date'] = month_day_year
final_df = final_df.append(df_25)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["it's alt good"])
df_26 = pd.DataFrame(features)
df_26['playlist_date'] = month_day_year
final_df = final_df.append(df_26)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Spring Pop 🌸"])
df_27 = pd.DataFrame(features)
df_27['playlist_date'] = month_day_year
final_df = final_df.append(df_27)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Fuego"])
df_28 = pd.DataFrame(features)
df_28['playlist_date'] = month_day_year
final_df = final_df.append(df_28)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Today's Indie Rock"])
df_29 = pd.DataFrame(features)
df_29['playlist_date'] = month_day_year
final_df = final_df.append(df_29)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["The Scene"])
df_30 = pd.DataFrame(features)
df_30['playlist_date'] = month_day_year
final_df = final_df.append(df_30)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Feelin' Myself"])
df_31 = pd.DataFrame(features)
df_31['playlist_date'] = month_day_year
final_df = final_df.append(df_31)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["ALT NOW"])
df_32 = pd.DataFrame(features)
df_32['playlist_date'] = month_day_year
final_df = final_df.append(df_32)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["New Joints"])
df_33 = pd.DataFrame(features)
df_33['playlist_date'] = month_day_year
final_df = final_df.append(df_33)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Soak Up The Sun"])
df_34 = pd.DataFrame(features)
df_34['playlist_date'] = month_day_year
final_df = final_df.append(df_34)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Hot Country"])
df_35 = pd.DataFrame(features)
df_35['playlist_date'] = month_day_year
final_df = final_df.append(df_35)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Alternative Beats"])
df_36 = pd.DataFrame(features)
df_36['playlist_date'] = month_day_year
final_df = final_df.append(df_36)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Homegrown + Heavy"])
df_37 = pd.DataFrame(features)
df_37['playlist_date'] = month_day_year
final_df = final_df.append(df_37)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["New Pop Picks"])
df_38 = pd.DataFrame(features)
df_38['playlist_date'] = month_day_year
final_df = final_df.append(df_38)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Westside Story"])
df_39 = pd.DataFrame(features)
df_39['playlist_date'] = month_day_year
final_df = final_df.append(df_39)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Fuego #052 - Regina's Fan Mixtape"])
df_40 = pd.DataFrame(features)
df_40['playlist_date'] = month_day_year
final_df = final_df.append(df_40)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Gulf & Western"])
df_41 = pd.DataFrame(features)
df_41['playlist_date'] = month_day_year
final_df = final_df.append(df_41)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["New Noise"])
df_42 = pd.DataFrame(features)
df_42['playlist_date'] = month_day_year
final_df = final_df.append(df_42)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["The New Alt"])
df_43 = pd.DataFrame(features)
df_43['playlist_date'] = month_day_year
final_df = final_df.append(df_43)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["bossa pop"])
df_43 = pd.DataFrame(features)
df_43['playlist_date'] = month_day_year
final_df = final_df.append(df_43)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["CST"])
df_44 = pd.DataFrame(features)
df_44['playlist_date'] = month_day_year
final_df = final_df.append(df_44)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Country Rocks"])
df_45 = pd.DataFrame(features)
df_45['playlist_date'] = month_day_year
final_df = final_df.append(df_45)
print(final_df.playlist_name.unique())
final_df

features = get_playlist_features(playlists["Country Rap"])
df_46 = pd.DataFrame(features)
df_46['playlist_date'] = month_day_year
final_df = final_df.append(df_46)
print(final_df.playlist_name.unique())
final_df

"""## Review `final_df` before exporting"""

### Final changes to final_df before exporting
#final_df['mode'] = final_df['mode'].replace({0: 'minor', 1: 'major'})
final_df = final_df.drop(['mode', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)

### Show final_df before exporting
final_df

"""## Export `final_df`"""

### Save the DataFrame as a CSV file to directory

# Get current date and time
current_datetime = datetime.now()

# Format the date and time to include in the file name
timestamp = current_datetime.strftime("%Y%m%d_%H%M%S")

# Construct the file name with timestamp
file_name = f'bulk_data_{timestamp}.csv'

# Specify the path to the 'data' subfolder relative to the current directory
data_folder = os.path.join('data - Sprint 02')

# Ensure that the 'data' subfolder exists, create it if it doesn't
os.makedirs(data_folder, exist_ok=True)

# Construct the file path within the 'data' subfolder
file_path = os.path.join(data_folder, file_name)

# Save the DataFrame as a CSV file to the 'data' subfolder
final_df.to_csv(file_path, index=False)

# Print confirmation message
print(f"DataFrame saved as CSV file: {file_path}")