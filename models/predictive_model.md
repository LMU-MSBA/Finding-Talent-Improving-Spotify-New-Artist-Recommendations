## Our Cluster Model Analysis

The objective for this model was to group playlists and tracks within playlists based on audio features. It aids new and upcoming artists in understanding where their song should be uploaded or has a chance to be successful. This model serves as the backend algorithm for when a user submits their track. As it is a clustering model, there isn't a specific target variable, but the goal is to group playlists based on audio features.

### Input Features Used in Our Model

The features used for clustering:

- **AVG_danceability**: The average suitability of a track for dancing.
- **AVG_energy**: The average intensity and activity of a track.
- **AVG_loudness**: The average overall loudness of a track.
- **AVG_speechiness**: The average presence of spoken words in a track.
- **AVG_instrumentalness**: The average likelihood that a track contains no vocals.
- **AVG_liveness**: The average presence of an audience in the recording.
- **AVG_valence**: The average musical positiveness conveyed by a track.
- **AVG_tempo**: The average estimated tempo of a track.
- **Cluster**: The label of clusters to which each playlist belongs.
- **Playlist_name**: The name of the playlist per row/cluster.

## Our Model’s Output in Terms of Helping New Artists

The model outputs four clusters, which help understand how different playlists can be grouped based on audio features. This understanding aids the artist team in assisting new and upcoming artists by providing insights into where their songs would fit best. The goal is to help artists increase their popularity by strategizing their music career based on playlist grouping.

### Performance Metrics

The elbow method was used to determine the optimal number of clusters. Inertia, the sum of squared distances of data points from their cluster centers, was calculated for a range of clusters (1 to 10). The number of clusters was selected based on the point where the "elbow" in the inertia plot became evident.

## Instructions on How to Use the Model

### Instructions on How to Use Model in Jupyter Notebook

1. Access the `config.ev` file containing credential information for accessing the MySQL database.
2. Load the `fact_playlist` data.
3. Select key audio features for clustering.
4. Normalize data and create a new dataframe.
5. Create a correlation matrix and visualize it with a heatmap.
6. Use KMeans function to fit the data and plot inertia to select the optimal number of clusters.
7. After selecting the optimal number of clusters, fit KMeans on the normalized features dataframe.
8. Plot the model using PCA to reduce dimensionality.
9. Customize the plot for aesthetic and branding purposes.
10. Use a dictionary to place the end user's song on the plot based on their audio features.

### Instructions on How to Use Model in Graphic User Interface (GUI)

1. Copy the Spotify song URL.
2. Paste the URL into the text input field on the GUI.
3. Press 'Enter'.
4. The song will appear on the cluster visualization as a pink dot.

### Interactive Features:
- **Cluster Visualization**: Hover over different clusters and data points to see which playlists the song sounds most similar to.
- **Saving Model Output**: Plotly allows saving model output as PNG.
- **Zooming**: Zoom in and out for detailed analysis.
- **Selection Tools**: Utilize lasso select and box select for further exploration.
