### Library Imports ###
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import plotly.express as px
import humanize

### Load Images ###
def load_image(image_path):
    with open(image_path, 'rb') as f:
        image = f.read()
    return image

### Configure Web App ###
uvicorn_image = load_image('uvicorn.png')
st.set_page_config(
    page_title="Spotifind Your Sound",
    page_icon=uvicorn_image#,
    #layout='wide'
)

### Database Connection ###
def connect_to_database():
    username = 'bsan6060'  # os.environ.get('RDS_USERNAME')
    password = 'awsBSAN6060'  # os.environ.get('RDS_PASSWORD')
    host = 'j-lavender-bsan.clw6q2u2kfpj.us-west-1.rds.amazonaws.com'  # os.environ.get('RDS_HOST')
    port = '3306'  # os.environ.get('RDS_HOST')
    database_name = 'spotify_6080_sprint02'  # os.environ.get('RDS_DATABASE2')

    url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}"
    engine = create_engine(url)
    return engine

@st.cache_resource
def fetch_data_from_database(_engine):
    try:
        with _engine.connect() as conn:
            with st.spinner(text="Connecting to database..."):
                dim_track_df = pd.read_sql_table("dim_track", conn)
                dim_artist_df = pd.read_sql_table("dim_artist", conn)
                fact_playlist_df = pd.read_sql_table("fact_playlist", conn)
                intermediate_table_df = pd.read_sql_table("intermediate_table", conn)
    except Exception as e:
        print(f"Error fetching data: {e}")
        st.error("Database Connection: Unsuccessful")
        return None, None, None, None

    return dim_track_df, dim_artist_df, fact_playlist_df, intermediate_table_df

### Spotify API ###
def get_spotify_data(song_url):
    try:
        if song_url:
            # Initialize Spotipy client
            client_credentials_manager = SpotifyClientCredentials(client_id='71ffd2a8db564881bd87cb36b3d59e0d',
                                                                  client_secret='41df7974594b4bf99cd65bab9793c8c5')
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            # Extract the song ID from the Spotify URL
            song_id = song_url.split('/')[-1]

            # Retrieve track information
            track_info = sp.track(song_id)

            # Extract desired features
            song_name = track_info['name']
            main_artist = track_info['artists'][0]['name']
            main_artist_id = track_info['artists'][0]['id']
            
            # Retrieve artist information
            artist_info = sp.artist(main_artist_id)
            main_artist_followers = artist_info['followers']['total']

            # Retrieve audio features
            audio_features = sp.audio_features(song_id)[0]
            danceability = audio_features['danceability']
            energy = audio_features['energy']
            loudness = audio_features['loudness']
            speechiness = audio_features['speechiness']
            acousticness = audio_features['acousticness']
            instrumentalness = audio_features['instrumentalness']
            liveness = audio_features['liveness']
            valence = audio_features['valence']
            tempo = audio_features['tempo']
            track_popularity = track_info['popularity']
            track_duration = track_info['duration_ms']

            # Retrieve artist popularity
            artist_popularity = artist_info['popularity']

            spotify_data = {
                'song_name': song_name,
                'main_artist': main_artist,
                'main_artist_followers': main_artist_followers,
                'danceability': danceability,
                'energy': energy,
                'loudness': loudness,
                'speechiness': speechiness,
                'acousticness': acousticness,
                'instrumentalness': instrumentalness,
                'liveness': liveness,
                'valence': valence,
                'tempo': tempo,
                'track_popularity': track_popularity,
                'track_duration_ms': track_duration,
                'artist_popularity': artist_popularity
            }
            spotify_df = pd.DataFrame([spotify_data])
            st.write(f"Here is the data for {song_name}:")
            st.write(spotify_df)
            
            return spotify_data
        else:
            return None
    except spotipy.SpotifyException as e:
        st.error("Error: Spotify API request failed. Please try again later.")
        st.error(e)
    except Exception as e:
        st.error("An unexpected error occurred. Please try again later.")
        st.error(e)

### Cluster Analysis ###
def cluster_analysis(df):
    # Set user-defined audio features using Streamlit sliders
    st.markdown("## Find Your Song")
    song_url = st.text_input("Paste your song URL here")
    
    if song_url is not None:
        
        spotify_data = get_spotify_data(song_url)
        
        if spotify_data is not None:
            
            song_name = spotify_data['song_name']
            danceability = spotify_data['danceability']
            energy = spotify_data['energy']
            loudness = spotify_data['loudness']
            speechiness = spotify_data['speechiness']
            instrumentalness = spotify_data['instrumentalness']
            liveness = spotify_data['liveness']
            valence = spotify_data['valence']
            tempo = spotify_data['tempo']
            
            main_artist_followers=spotify_data['main_artist_followers']
            main_artist=spotify_data['main_artist']
            track_popularity=spotify_data['track_popularity']
            artist_popularity=spotify_data['artist_popularity']
            track_duration_ms=spotify_data['track_duration_ms']
            
            
            user_song = ['',song_name, '', '', '', '', '', danceability, energy,
                         loudness, speechiness, '', instrumentalness,
                         liveness, valence, tempo, '', '']
            df = df.append(pd.Series(user_song, index=df.columns), ignore_index=True)
        else:
            song_name = None
            danceability = None
            energy = None
            loudness = None
            speechiness = None
            instrumentalness = None
            liveness = None
            valence = None
            tempo = None
            main_artist_followers=None
            main_artist=None
            track_popularity=None
            artist_popularity=None
            track_duration_ms=None
            
            user_song = ['',song_name, '', '', '', '', '', danceability, energy,
                         loudness, speechiness, '', instrumentalness,
                         liveness, valence, tempo, '', '']
    #st.write("Set your audio features")
    #clucol1, clucol2, clucol3, clucol4 = st.columns([1,1,1,1])
    #with clucol1: danceability = st.slider("Set danceability", 0.0, 1.0, step=0.001)
    #with clucol2: energy = st.slider("Set energy", 0.0, 1.0, step=0.001)
    #with clucol3: loudness = st.slider("Set loudness (dB)", -60.0, 0.0, step=0.001)
    #with clucol4: speechiness = st.slider("Set speechiness", 0.0, 1.0, step=0.0001)
    
    #cluclo5, cluclo6, cluclo7, cluclo8 = st.columns([1,1,1,1])
    #with cluclo5: instrumentallness = st.slider("Set instrumentalness", 0.0, 1.0, step=0.00001)
    #with cluclo6: liveness = st.slider("Set liveness", 0.0, 1.0, step=0.0001)
    #with cluclo7: valence = st.slider("Set valence", 0.0, 1.0, step=0.001)
    #with cluclo8: tempo = st.slider("Set tempo", 0.0, 300.0, step=1.000)
        
    #if spotify_data is not None:

    
    # Slice audio feature columns
    audio_features = df.iloc[:, 7:16]

    # Remove the "_by_playlist" suffix from column names
    audio_features.columns = audio_features.columns.str.replace('_by_playlist', '')

    # Drop AVG_accousticness because it's NaN
    audio_features.drop(columns=['AVG_accousticness'], inplace=True)

    # Use MinMaxScaler to normalize the data
    scaler = MinMaxScaler()
    features_normal = scaler.fit_transform(audio_features)
    features_normal = pd.DataFrame(features_normal, columns=audio_features.columns)
    
    #features_with_playlist = pd.concat([features_normal, df['playlist_name']], axis=1)
    #st.write(features_with_playlist)
    
    #my_song_df = features_with_playlist[features_with_playlist['playlist_name'] == 'mysong']
    #st.write(my_song_df)
    
    #features_with_playlist = features_with_playlist[features_with_playlist['playlist_name'] != 'mysong']
    #st.write(features_with_playlist)
    #features_normal = features_with_playlist.drop('playlist_name', axis=1)
    
    # Run KMeans clustering
    kmeans = KMeans(n_clusters=4, random_state=99)
    labels = kmeans.fit_predict(features_normal)
    features_normal['cluster'] = labels

    # Merge playlist_name column back to features_normal DataFrame
    #df = df[df['playlist_name'] != 'mysong']
    features_with_playlist = pd.concat([features_normal, df['playlist_name']], axis=1)

    if song_name is not None:
        user_features_with_playlist = features_with_playlist[features_with_playlist['playlist_name']==song_name]
        user_features_without_playlist = user_features_with_playlist.drop('playlist_name', axis=1)
        features_with_playlist = features_with_playlist[features_with_playlist['playlist_name']!=song_name]
    else:
        user_features_with_playlist = None
        user_features_without_playlist = None
    
    # Perform PCA to reduce dimensionality to 2 components
    pca = PCA(n_components=2)
    features_pca = pca.fit_transform(features_with_playlist.drop('playlist_name', axis=1))

    # Transform mysongdf with PCA
    if user_features_without_playlist is not None: 
        my_song_df_features_pca = pca.transform(user_features_without_playlist)
    else: my_song_df_features_pca = None

    # Create a figure
    fig = go.Figure()

    # Plot clusters
    fig.add_trace(go.Scatter(x=features_pca[:, 0], y=features_pca[:, 1], mode='markers',
                             marker=dict(color=labels, colorscale='Tealgrn', opacity=0.7, size=10),
                             name='Playlist',
                             text=features_with_playlist['playlist_name'],  # Set text to playlist_name
                             showlegend=False))

    if my_song_df_features_pca is not None:
        # Add a single point for user's song
        fig.add_trace(go.Scatter(x=[my_song_df_features_pca[0][0]], y=[my_song_df_features_pca[0][1]],
                                 mode='markers',
                                 marker=dict(color='#f037a5', size=15),  # Set color to hex f037a5 and size as desired
                                 name=song_name))

    # Customize plot
    fig.update_layout(
        title='Audio Features Clustered by Playlist',
        xaxis_title='Audio Features',
        yaxis_title='Audio Features'
    )

    return danceability, energy, loudness, speechiness, instrumentalness, liveness, valence, tempo, fig, main_artist_followers, main_artist, track_popularity, artist_popularity, track_duration_ms

### Beautify Large Numbers ###
def custom_intword(value):
    """
    Custom function to format large numbers with 'K' for thousands and 'M' for millions.
    """
    if value >= 1000000:
        return "{:.1f}M".format(value / 1000000)
    elif value >= 1000:
        return "{:.1f}K".format(value / 1000)
    else:
        return str(value)

# Override the intword function in the humanize library with the custom function
humanize.intword = custom_intword

### Display Playlist Metrics ###
def display_playlist_metrics(playlist_selector, filtered_df, danceability, energy, loudness, speechiness, instrumentalness, liveness, valence, tempo, main_artist_followers, track_popularity, artist_popularity, track_duration_ms):
    
    if danceability is not None: danceability = danceability
    else: danceability = 0
    if energy is not None: energy = energy
    else: energy = 0
    if speechiness is not None: speechiness = speechiness
    else: speechiness = 0
    if instrumentalness is not None: instrumentalness = instrumentalness
    else: instrumentalness = 0
    if liveness is not None: liveness = liveness
    else: liveness = 0
    if valence is not None: valence = valence
    else: valence = 0
    if tempo is not None: tempo = tempo
    else: tempo = 0
    if main_artist_followers is not None: main_artist_followers = main_artist_followers
    else: main_artist_followers = 0
    if track_popularity is not None: track_popularity = track_popularity
    else: track_popularity = 0
    if artist_popularity is not None: artist_popularity = artist_popularity
    else: artist_popularity = 0
    if track_duration_ms is not None: track_duration_ms = track_duration_ms
    else: track_duration_ms = 0
   
    
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1: st.metric("Playlist Followers", humanize.intword(filtered_df.playlist_followers.mean()), humanize.intword(main_artist_followers))
    with col2: st.metric("Avg. Track Popularity", format(filtered_df.AVG_track_popularity_by_playlist.mean(), ".2f"), track_popularity)
    with col3: 
        minutes = int(filtered_df.AVG_track_duration_sec_by_playlist.mean() // 60)
        remaining_seconds = int(filtered_df.AVG_track_duration_sec_by_playlist.mean() % 60)
        st.metric("Avg. Track Duration", f"{minutes}:{remaining_seconds:02d}")
    with col4:
        explicit_percentage = str(int(filtered_df.RATIO_track_explicit_by_playlist.mean()*100)) + "%"
        st.metric("% of Explicit Tracks", explicit_percentage)
    with col5: st.metric("Avg. Danceability", format(filtered_df.AVG_danceability_by_playlist.mean(), ".2f"), danceability)
    
    col6, col7, col8, col9, col10 = st.columns([1,1,1,1,1])
    with col6: st.metric("Avg. Energy", format(filtered_df.AVG_energy_by_playlist.mean(), ".2f"), energy)
    with col7: st.metric("Avg. Loudness", format(filtered_df.AVG_loudness_by_playlist.mean(), ".2f"), loudness)
    with col8: st.metric("Avg. Speechiness", format(filtered_df.AVG_speechiness_by_playlist.mean(), ".2f"), speechiness)
    with col9: st.metric("Avg. Acousticness", format(filtered_df.AVG_accousticness_by_playlist.mean(), ".2f"))
    with col10: st.metric("Avg. Instrumentalness", format(filtered_df.AVG_instrumentalness_by_playlist.mean(), ".5f"), instrumentalness)

    col11, col12, col13, col14, col15 = st.columns([1,1,1,1,1])
    with col11: st.metric("Avg. Liveness", format(filtered_df.AVG_liveness_by_playlist.mean(), ".2f"), liveness)
    with col12: st.metric("Avg. Valence", format(filtered_df.AVG_valence_by_playlist.mean(), ".2f"), valence)
    with col13: st.metric("Avg. Tempo", format(filtered_df.AVG_tempo_by_playlist.mean(), ".2f"), tempo)
    with col14: st.metric("Avg. Artist Followers", humanize.intword(filtered_df.AVG_artist_followers_by_playlist.mean()), humanize.intword(main_artist_followers))
    with col15: st.metric("Avg. Artist Popularity", format(filtered_df.AVG_artist_popularity_by_playlist.mean(), ".2f"), track_popularity)

### Visualize Bottom Artists ###
def display_bottom_artists(result_df, playlist_selector):
    
    # Define colors for the bars
    color1 = '#1ED760'
    color2 = '#f037a5'

    # Create the bar chart using Plotly Express
    fig1 = px.bar(result_df, 
                  x='artist_name', 
                  y='artist_followers', 
                  title=f"{playlist_selector}: Up & Coming Artists",
                  color_discrete_sequence=[color1])

    # Update the layout to add axis labels and a secondary y-axis
    fig1.update_layout(
        xaxis=dict(title="Artist"),
        yaxis=dict(title="Artist Followers"),
        legend_title="Artist Metrics"
    )
    
    result_df_sorted = result_df.sort_values(by='artist_popularity', ascending=True)
    
    # Create the bar chart using Plotly Express
    fig2 = px.bar(result_df_sorted, 
                  x='artist_name', 
                  y='artist_popularity', 
                  title=f"{playlist_selector}: Up & Coming Artists",
                  color_discrete_sequence=[color1])

    # Update the layout to add axis labels and a secondary y-axis
    fig2.update_layout(
        xaxis=dict(title="Artist"),
        yaxis=dict(title="Artist Popularity"),
        legend_title="Artist Metrics"
    )
    

    # Show the chart using st.plotly_chart()
    return fig1, fig2

### Process Data ###
def process_data(playlist_selector, fact_playlist_df, intermediate_table_df, dim_artist_df):
    if len(playlist_selector) > 0:
        filtered_df = fact_playlist_df[fact_playlist_df['playlist_name'] == playlist_selector].reset_index(drop=True)
        # Additional processing to generate result_df
        playlist_id = filtered_df.loc[0, 'playlist_id']
        distinct_artist_ids = intermediate_table_df.loc[intermediate_table_df['playlist_id'] == playlist_id, 'artist_id'].unique()
        filtered_artists_df = dim_artist_df[dim_artist_df['artist_id'].isin(distinct_artist_ids)]
        selected_columns = ['artist_name', 'artist_followers', 'artist_popularity', 'artist_genres']
        result_df = filtered_artists_df[selected_columns].sort_values(by=['artist_followers', 'artist_popularity'], ascending=[True, True]).head(5)
        return result_df
    else:
        return None

### ###
def main():
    st.markdown("<h1 style='text-align: center; color: #1ED760;'>Spotifind Your Sound</h1>",
                unsafe_allow_html=True)
    st.write("Discover your unique sound in the world of emerging artists. Our web app allows you to compare your music to to curated and algorithmic playlists by Spotify. Through visual displays, explore playlists with similar audio features and metrics, gaining deeper insights into your musical identity.")
    st.markdown("<hr>", unsafe_allow_html=True)

    engine = connect_to_database()
    dim_track_df, dim_artist_df, fact_playlist_df, intermediate_table_df = fetch_data_from_database(engine)

    #song_url = "https://open.spotify.com/track/43SMQMC2X2fAOuTPRnSGrG" #st.text_input("Paste your song URL here")
    #spotify_data = get_spotify_data(song_url)
    
    danceability, energy, loudness, speechiness, instrumentalness, liveness, valence, tempo, fig, main_artist_followers, main_artist, track_popularity, artist_popularity, track_duration_ms = cluster_analysis(fact_playlist_df)#, song_url)
    st.plotly_chart(fig)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## Find Your Playlist")
    
    # Get user input
    playlist_selector = st.selectbox("Select a Spotify Playlist", sorted(fact_playlist_df['playlist_name'].unique()))

    # Process data and display results
    if len(playlist_selector) > 0:
        filtered_df = fact_playlist_df[fact_playlist_df['playlist_name'] == playlist_selector].reset_index(drop=True)
        display_playlist_metrics(playlist_selector, filtered_df, danceability, energy, loudness, speechiness, instrumentalness, liveness, valence, tempo, main_artist_followers, track_popularity, artist_popularity, track_duration_ms)
        
        # Process data and get result_df
        result_df = process_data(playlist_selector, fact_playlist_df, intermediate_table_df, dim_artist_df)
        if result_df is not None:
            # Display top artists
            fig1, fig2 = display_bottom_artists(result_df, playlist_selector)
            
            tab1, tab2 = st.tabs(["Artist Followers", "Avg. Artist Popularity"])
            with tab1: fig1
            with tab2: fig2
            
            # Assuming 'artist_name' is the common column in both DataFrames
            artist_url_df = result_df.merge(dim_artist_df[['artist_name', 'artist_id']], on='artist_name', how='left')
            artist_url_df.rename(columns={'artist_id': 'result_artist_id'}, inplace=True)

            # Iterate over the merged DataFrame to generate URLs
            st.markdown("### Artist Profiles")
            colart1, colart2 = st.columns([1,1])
            with colart1:
                for index, row in artist_url_df.iterrows():
                    artist_url = f"https://open.spotify.com/artist/{row['result_artist_id']}"
                    st.link_button(row['artist_name'],f"{artist_url}")
            with colart2: st.image("https://media.giphy.com/media/7x15gKDB9sEs4KRbdZ/giphy.gif", width=250)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.link_button("Spotify","https://open.spotify.com/")
    st.link_button("🐱 GitHub","https://github.com/LMU-MSBA/Finding-Talent-Improving-Spotify-New-Artist-Recommendations")
    
if __name__ == "__main__":
    main()
