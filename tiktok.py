# Import JSOn for the export of data
import json

# Import data processing helper
from helpers import process_results

# Importing the tiktok Python SDK
from TikTokApi import TikTokApi

# Import pandas to create dataframes
import pandas as pd

# Import sys dependency to extract command line arguments
import sys


def get_data(hash_tag):
    # # Get cookie data
    # verifyFp = "92af990aa9d697d8558c3bac2050dce2"

    # Setup TikTok API
    with TikTokApi() as api:

        # Count total videos scraped
        total_videos = 0

        # Empty dictionary for later dataframe forming
        author_list = []
        video_list = []

        # Get data by hashtag
        tag = api.hashtag(name=hash_tag)

        # Loop through each video
        for video in tag.videos(count=1500):
            # Get the video author data
            username = video.author.username
            nickname = video.as_dict.get('author').get('nickname')
            is_verified = video.as_dict.get('author').get('verified')
            is_privateAcc = video.as_dict.get('author').get('privateAccount')
            author_num_likes = video.as_dict.get('authorStats').get('diggCount')  # digg reveals the number of videos a user liked even when the privacy setting is implemented https://www.linkedin.com/pulse/tiktok-metadata-machine-brian-napierala?trk=articles_directory
            author_num_followers = video.as_dict.get('authorStats').get('followerCount')
            author_num_following = video.as_dict.get('authorStats').get('followingCount')
            author_num_hearts = video.as_dict.get('authorStats').get('heartCount')
            author_num_videos = video.as_dict.get('authorStats').get('videoCount')

            author_item = {
                'username': username,
                'nickname': nickname,
                'is_verified': is_verified,
                'is_privateAcc': is_privateAcc,
                'author_num_likes': author_num_likes,
                'author_num_followers': author_num_followers,
                'author_num_following': author_num_following,
                'author_num_hearts': author_num_hearts,
                'author_num_videos': author_num_videos
            }
            author_list.append(author_item)

            # Get the video data
            vid_created_time = video.create_time
            vid_desc = video.as_dict.get('desc')
            vid_likes = video.stats.get('diggCount')
            vid_plays = video.stats.get('playCount')
            vid_shares = video.stats.get('shareCount')
            vid_comments = video.stats.get('commentCount')
            vid_duration = video.as_dict.get('video').get('duration')
            video_playAddr = video.as_dict.get('video').get('playAddr')

            video_item = {
                'vid_created_time': vid_created_time,
                'vid_desc': vid_desc,
                'vid_likes': vid_likes,
                'vid_plays': vid_plays,
                'vid_shares': vid_shares,
                'vid_comments': vid_comments,
                'vid_duration': vid_duration,
                'video_playAddr': video_playAddr
            }
            video_list.append(video_item)

            total_videos += 1

    # Convert to dataframe
    author_df = pd.DataFrame(author_list)
    video_df = pd.DataFrame(video_list)

    # Merge 2 dataframes vertically
    df = pd.concat([author_df, video_df], axis=1, join='inner')
    df.sort_values(by='vid_created_time', inplace=True)

    # Save as CSV file
    author_df.to_csv('authors.csv', index=False)
    video_df.to_csv('TikTokVideo.csv', index=False)
    df.to_csv('tiktokdata.csv', index=False)  # Merge author_df and video_df

    # # Process data
    # flattened_data = process_results(trending)

    # # Export data to JSON
    # with open('export.json', 'w') as f:
    #     json.dump(flattened_data, f)

    # # Convert the preprocessed data to a dataframe
    # df = pd.DataFrame.from_dict(data=flattened_data, orient='index')
    # df.to_csv('tiktokdata.csv', index=False)


if __name__ == '__main__':
    get_data(sys.argv[1])
    print(f'sys.argv[1] is "{sys.argv[1]}"')
