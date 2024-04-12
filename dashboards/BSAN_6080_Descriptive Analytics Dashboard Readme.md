# Descriptive Analytics Dashboard Readme

## Title
Artist Team Dashboard
	
### Purpose
This dashboard is designed to display a detailed descriptive analysis of track attributes    occupying the Billboard Top 100 chart to provide insights on fostering emerging artists on Spotify. 

### Audience
Spotify internal artist team, which typically consists of individuals who work directly with musicians, bands, and other creators to optimize their presence on the platform.
Their primary focus revolves around fostering relationships with artists, their management teams, and record labels. They also serve as a liaison between Spotify and the artist community, addressing inquiries, and offering guidance and support.

	
### How does the dashboard address the business problem?
Our goal is to utilize the 4 tiles of dashboards, along with the genre, quarter, and track attribute slicers, to dynamically showcase music trends and attributes that align with chart-topping success, then transforming these insights into actionable strategies. We want to equip the Spotify artist team with the at-a-glance tool to assist small artists with data-driven guidance to produce their songs with the qualities that resonate with the current chart dynamics and increase their opportunity for success.

### Identify the business process that utilizes the dashboard for decision making. 
Operational process. This dashboard will be utilized to assist the artist team to strategize and foster emerging talent effectively. 

### Which decisions are influenced by the dashboard?
The dashboard is a critical tool for shaping a variety of strategic decisions aimed at increasing the presence and success of small and emerging artists on Spotify. This includes selecting track attributes that are imperative for future music production with the potential for high listener appeal and chart impact, guiding the analysis of successful artist strategies that can be adopted, and optimizing music release schedule that aligns with seasonal trends.

## Access
https://github.com/LMU-MSBA/Finding-Talent-Improving-Spotify-New-Artist-Recommendations/blob/main/dashboards/v2%20Descriptive%20Analytics%20Dashboard.twbx

## Data Source:
Spotify_6080 MySQL Database.

It consists of 6 tables:
- fact_table: contains track attributes
- dim_song: contains song attributes 
- dim_artist: contains artist information 
- dim_album: contains album information
- dim_chart_month: contains the month the song was charted 
- dim_pitch_class: contains pitch information

## Key Metrics
	
- Tile 1: 
Average Popularity: Average popularity of all the charting songs using the average measure on Tableau.
Average Weeks on Chart: Average chart lifespan of songs using number of weeks as the unit. Calculated using the average measure on Tableau.

- Tile 2:
Average Popularity: Average popularity of all the charting songs by artist using the average measure on Tableau.
Number of followers: The number of followers of the charting artists on Spotify.

- Tile 3: 
Top Track Features on Average: Average score of the top track features we have identified using the average measure on Tableau. The top track feature includes: energy, danceability, valence, acousticness, instrumentalness. 

- Tile 4:
Changes in Avg Track Attributes Over Time: Plotting the average score of all track attributes over time using the average measure on Tableau.
	
## How to Use the Dashboard
	
This dashboard is consisted of a “download PDF” button and 3 slicers on the top as well as 4 tiles. 

- Download PDF button: Click to download a PDF version of the dashboard page. 

- Slicer 1 – Quarter: 
Click the drop-down arrow to reveal a list of 5 options for the quarter slicers, namely (All), Q1, Q2, Q3, and Q4. This filters all 4 tiles of the dashboard to the selected quarter for further analysis. 

-  Slicer 2 – Genre: 
Click the drop-down arrow to reveal a list of 318 options for music genre. This filters all 4 tiles of the dashboard to the selected genre for further analysis. 

-  Slicer 3 – Track Attributes: 
Click the drop-down arrow to reveal a list of 11 options for track attributes. It is a parameter list that is only applicable to tile 4: Changes in Avg Track Attributes Over Time. 

- Tile 1 – Avg Popularity and Avg Weeks on Chart: 
This chart dynamically changes with the slicers 1 and 2 to showcase the average popularity level needed for a track in a particular genre to break into the Billboard 100 chart and their chart lifespan using the number of weeks. 

- Tile 2 - Artist with Avg Song Popularity Within Top 10%: 
This chart dynamically changes with the slicers 1 and 2 to showcase the number of followers of artists with songs that has the popularity levels within the top 10% of their genre. The bars show their number of followers, and the circles show the average popularity of their songs. 

- Tile 3 - Top Track Features on Avg: 
This chart dynamically changes with the slicers 1 and 2 to showcase the average score of the top 5 track attributes of charting music. The top 5 attributes are selected based on market research – energy, danceability, valence, acousticness, and instrumentalness. 

- Tile 4 - Changes in Avg Track Attributes Over Time:
This chart dynamically changes with the slicers 1, 2 and 3 to showcase the trend of selected track attribute of charting music over time. 
 
## How to Refresh the Data

1.	Open one of the worksheets
2.	In the data pane on the left, locate “spotify_6080” and right click. 
3.	Click refresh. 
	
