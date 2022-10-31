# Import base streamlit dependency
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime

# Import pandas to load the analytics data
import pandas as pd

# Import subprocess and os to run the tiktok script from command line
from subprocess import call
import os

# Import plotly for visualization
import plotly.express as px

# Import system
import sys
import time

# Set page width to wide
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Set CSS style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():

    # Create sidebar
    st.sidebar.markdown(
        '<div style="text-align:center;display:block;"><img src="https://pngimg.com/uploads/tiktok/tiktok_PNG8.png" width=230> </div>',
        unsafe_allow_html=True)
    st.sidebar.markdown('<div> <h1 style="text-align:center;">TikTok Analytics</h1> </div>', unsafe_allow_html=True)
    st.sidebar.markdown("This dashboard allows you to analyse trending 📈 tiktoks using Python and Streamlit.")
    st.sidebar.markdown(
        "To get started <ol><li>Enter the <i>hashtag</i> you wish to analyse</li> <li>Hit <i>Get Data</i>.</li> <li>Get analyzing</li></ol>",
        unsafe_allow_html=True)
    # Input
    hashtag = st.text_input(label="Search for a hashtag here to analyze (E.g. leeziijia):", value="", placeholder='leeziijia')

    # Button
    if st.button(label='Get Data'):
        # Run get data function here
        os.system(command=f'python tiktok.py {hashtag}')  # call(['python', 'tiktok.py', hashtag])
        time.sleep(7)

        # Load in existing data to test it out
        df = pd.read_csv('TikTokVideo.csv')
        df.sort_values(by='vid_created_time', inplace=True)

        # Process the data
        # https://betterprogramming.pub/visualize-charts-using-groupby-and-aggregate-python-functions-56454820a25c
        df2 = df.loc[:, ['vid_created_time', 'vid_likes', 'vid_plays', 'vid_shares']]
        df2['vid_created_time'] = pd.to_datetime(df2["vid_created_time"])
        df2['vid_created_time_year'] = df2['vid_created_time'].apply(lambda x: x.year)
        df2['vid_created_time_month'] = df2['vid_created_time'].apply(lambda x: x.month)
        df2_grouped_year = df2.groupby('vid_created_time_year')[['vid_likes', 'vid_plays', 'vid_shares']].sum()
        df2_grouped_year = df2_grouped_year.reset_index()

        # Split columns
        st.markdown('### Metrics')
        left_col, mid_col, right_col = st.columns(3)

        # First Chart - Total Plays
        left_col.metric(label="Total Plays", value=f"{sum(df2_grouped_year.loc[:, 'vid_plays'])}")

        # Second Chart - Total Likes
        mid_col.metric(label="Total Likes", value=f"{sum(df2_grouped_year.loc[:, 'vid_likes'])}")

        # Third Chart - Total Shares
        right_col.metric(label="Total Shares", value=f"{sum(df2_grouped_year.loc[:, 'vid_shares'])}")

        # Plotly visualization here
        df2_grouped_year['vid_created_time_year'] = df2_grouped_year['vid_created_time_year'].apply(str)
        st.markdown('### Bar Chart')
        fig = px.bar(data_frame=df2_grouped_year, x='vid_created_time_year', y=['vid_plays', 'vid_likes', 'vid_shares'], barmode='group')
        fig.update_layout(title_text=f'Number of Plays, Likes & Shares over Years', title_x=0.5, font_size=12, legend_title_text='Types')
        fig.update_yaxes(title_text='Count')
        fig.update_xaxes(title_text='Years')
        fig.update_traces(hovertemplate="<br>".join(["Year: %{x}", "Count: %{y}"]))
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

        st.markdown('### Line Chart')
        fig = px.line(data_frame=df2_grouped_year, x='vid_created_time_year', y=['vid_plays', 'vid_likes', 'vid_shares'], markers=True)
        fig.update_layout(title_text=f'Number of Plays, Likes & Shares over Years', title_x=0.5, font_size=12, legend_title_text='Types')
        fig.update_yaxes(title_text='Count')
        fig.update_xaxes(title_text='Years')
        fig.update_traces(hovertemplate="<br>".join(["Year: %{x}", "Count: %{y}"]))
        st.plotly_chart(figure_or_data=fig, use_container_width=True)

        # Show tabular dataframe in streamlit
        st.markdown('### Original DataFrame')
        st.dataframe(data=df)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
