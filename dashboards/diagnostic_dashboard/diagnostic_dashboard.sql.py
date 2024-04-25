'''
Important Note:
We won't be providing SQL code to fulfill this requirement. The reason is that we're not connecting to the data warehouse through tools like Tableau or Power BI. Instead, our Python code generates the Streamlit web app and connects directly to the data warehouse.

Current Approach:
In our code, we retrieve the entire contents of the data warehouse tables without any restrictions. This is because, at present, the app requires all records given the recent nature of the data pull.

Future Considerations:
However, as we continue to update our warehouse with fresh playlist data on a monthly basis, we anticipate a need for more refined querying. To achieve this, there's a playlist_date field in the intermediate_table that we can leverage. For instance, looking ahead 10 years from now, we wouldn't want to load a decade's worth of monthly playlists into our dataframes. Instead, we'd want to restrict the data retrieval to, say, just the past 5 years.

Implementation Detail:
Below is a snippet directly from final_web_app.py, where the Streamlit web app is being created:
'''

### Database Connection ###
def connect_to_database():
    username = os.environ.get('RDS_USERNAME')
    password = os.environ.get('RDS_PASSWORD')
    host = os.environ.get('RDS_HOST')
    port = os.environ.get('RDS_HOST')
    database_name = os.environ.get('RDS_DATABASE2')

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