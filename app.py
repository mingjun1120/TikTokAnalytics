# Import base streamlit dependency
import streamlit as st

# Import pandas to load the analytics data
import pandas as pd

# Import subprocess and os to run the tiktok script from command line
from subprocess import call
import os

# Import plotly for visualization
import plotly.express as px

# Set page width to wide
st.set_page_config(layout='wide')

# Create sidebar
st.sidebar.markdown('<div style="text-align:center;display:block;"><img src="https://pngimg.com/uploads/tiktok/tiktok_PNG8.png" width=230> </div>', unsafe_allow_html=True)
st.sidebar.markdown('<div> <h1 style="text-align:center;">TikTok Analytics</h1> </div>', unsafe_allow_html=True)
st.sidebar.markdown("This dashboard allows you to analyse trending 📈 tiktoks using Python and Streamlit.")
st.sidebar.markdown("To get started <ol><li>Enter the <i>hashtag</i> you wish to analyse</li> <li>Hit <i>Get Data</i>.</li> <li>Get analyzing</li></ol>", unsafe_allow_html=True)


# Input
hashtag = st.text_input(label = "Search for a hashtag here to analyze (E.g. leechongwei):", value = "")

# Button
if st.button(label = 'Get Data'):
    # Run get data function here
    os.system(command=f'python tiktok.py {hashtag}') # call(['python', 'tiktok.py', hashtag])

    # Load in existing data to test it out
    df = pd.read_csv('tiktokdata.csv')
    
    # Plotly visualization here
    fig = px.histogram(data_frame=df, x='desc', y='stats_diggCount', hover_data=['desc'], height=300)
    st.plotly_chart(figure_or_data=fig, use_container_width=True)

    # Split columns
    left_col, right_col = st.columns(2)
    
    # First Chart - video stats
    scatter1 = px.scatter(df, x='stats_shareCount', y='stats_commentCount', hover_data=['desc'], size='stats_playCount', color='stats_playCount')
    left_col.plotly_chart(scatter1, use_container_width=True)
    
    # Second Chart
    scatter2 = px.scatter(df, x='authorStats_videoCount', y='authorStats_heartCount', hover_data=['author_nickname'], size='authorStats_followerCount', color='authorStats_followerCount')
    right_col.plotly_chart(scatter2, use_container_width=True)
    
    # Show tabular dataframe in streamlit
    st.dataframe(data=df)
    