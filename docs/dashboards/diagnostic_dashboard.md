# Spotifind Your Sound

## Purpose
This dashboard allows users to input a Spotify song link for a comprehensive analysis of the song's audio features and comparing them to those of our curated Spotify playlists. It also displays detailed information about playlists and aims to help users identify potential opportunities for their tracks to be featured on similar playlists.

## Audience
Spotify Artist Team and emerging artists

## How does the dashboard address the business problem
This dashboard is designed to help the Spotify artist team and emerging artists identify opportunities to increase their exposure. It enables users to compare their music with selected curated and algorithmic Spotify playlists. Through visual displays, they can explore playlists with similar audio features and metrics while gaining deeper insights into their musical identity. This tool helps artists understand how they might adjust their tracks to align better with these playlists and increase their chances of being featured. Additionally, by analyzing the strategies of other small artists on these playlists, users can develop actionable strategies to grow their platform.

## Identify the business process that utilizes the dashboard for decision making
Operational process. This dashboard will be utilized by the artist team to gain better insights on their clients’ (artists) music to strategize and foster emerging talent effectively.

## Which decisions are influenced by the dashboard
A variety of strategic decisions which include:
- Track audio feature adjustment
- Marketing tactics
- Social media presence

## Access
[Spotifind Your Sound Dashboard](https://spotifind.streamlit.app/)

## Data Source(s)
- **Playlist Data:** Spotify Web API using Spotip
- **MySQL Data Warehouse:**
  - Schema: spotify_6080_sprint02
  - dim_track
  - dim_artist
  - intermediate_table
  - fact_playlist

## Key Metrics
- Sum of artist followers
- Average artist popularity

## How to Use the Dashboard
1. User inputs their Spotify song link into the “Find Your Song” text bar and hits enter.
2. The dashboard will display cluster analysis visualization populating the playlist data and inputted song audio features. The user's song is displayed as the pink circle which allows for easy comparison with the clusters. This visualization is dynamic and allows zooming in and out, lasso, box select, saving as png, etc.
3. After users explore the results, they can choose a specific playlist from the dropdown menu below which displays 15 metrics for the selected playlist as well as the user’s track audio feature in the smaller text.
4. Below the playlist metrics, users will find 2 bar charts that display 5 artists with the lowest amount of followers and 5 artists with the lowest avg. track popularity from the selected playlist. This helps users assess the strategies of other small artists as they have been featured.
5. Scroll down and users will find the name of the artists displayed on the bar charts. Navigate to them and users will be led to their Spotify profile links for easy access.

## How to Refresh the Data
The ETL automatic pipeline is scheduled to feed the database with fresh data monthly. Since the dashboard calls the database, results are updated on a monthly basis.
