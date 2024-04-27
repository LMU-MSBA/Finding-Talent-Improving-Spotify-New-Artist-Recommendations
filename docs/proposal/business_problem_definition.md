# Determine Business Objectives

## Background
Spotify, as a leading music and podcast streaming platform, faces several challenges in its ecosystem. While it boasts an extensive catalog of music from established artists, it also hosts a multitude of smaller, independent artists who struggle to gain visibility and reach wider audiences. These emerging artists often face the following issues:
- Lack of Exposure: Smaller artists find it challenging to compete for attention in a sea of content. Their songs may get lost amidst popular tracks, limiting their chances of being discovered by listeners.
- Data-Driven Decision Making: In today’s digital age, data plays a crucial role in decision-making. However, many independent artists lack the resources or expertise to analyze their streaming data effectively. They miss out on valuable insights that could help them tailor their strategies and grow their audience.
- Monetization and Sustainability: For independent artists, streaming revenue is a significant source of income. Maximizing their monthly streams directly impacts their financial sustainability. Yet, without data-driven guidance, they may struggle to optimize their music for better performance.

## Business Activity & Category
### Category
Improve Strategy: Allows the Artist’s Team at Spotify to optimize artists’ presence and improve popularity.
### Activity
D03: Improve identification of opportunities

## OKR (Objectives and Key Results)
### Objective
Empower independent artists at Spotify to increase their popularity on the platform
### Key Result
- At least 50% of artists who work with the Artist Team at Spotify will achieve a 20% increase, on average, in popularity by the end of Q4

## OMTM
Popularity

## OKR Initiatives
- Develop and deploy a descriptive analytics dashboard to recommend music attributes based on current popular trends.
- Implement a diagnostic analytics dashboard to identify areas for improvement for artists.
- Build and automate a data pipeline to extract, transform, and load data from Spotify's API.
- Develop a predictive model to surface growing artists, genres, and music trends.

# Assess Situation
## Inventory of Resources
### Personnel
- Christy - Data Analyst
- Jada - Data Engineer
- Sebastian - Data Scientist
- Leia - Legal Manager
- Brenda - Data Governance
- Christian - Artist Team Consultant (sales)
- Lily - Machine Learning Engineer
- Keith - Privacy and Audit Manager
### Data
- Billboard 100 API
- Spotify Web API through Spotipy library
- Billboard charts data through billboard-charts
### Computing Resources
- AWS RDS
### Software
- MySQL
- Tableau Desktop
- Python (Jupyter Notebook)

## Requirements, Assumptions, and Constraints
- Access to Spotify API is reliable
- Access to Billboard 100 API is reliable
- Data quality from the API is consistent
- No budget for additional software or resources

## Risks and Contingencies
- API changes affecting data access
- Limit to the number of requests to Spotify’s API
- Legal concerns around training data that will be used to train models and support competitor artists
- Skill gaps within the team
- Storage restraints with AWS RDS

## Terminology
- ETL: Extract, Transform, Load
- API
