# Import JSOn for the export of data
import json

# Importing the tiktok Python SDK
from TikTokApi import TikTokApi as tiktok

# Import data processing helper
from helpers import process_results

# Import pandas to create dataframes
import pandas as pd

# Import sys dependency to extract command line arguments
import sys

def get_data(hash_tag):
    
    # Get cookie data
    verifyFp = "92af990aa9d697d8558c3bac2050dce2"

    # Setup instance of tiktok
    api = tiktok.get_instance(custom_verify_fp=verifyFp, use_test_endpoints=True)

    # Get data by hashtag
    trending = api.by_hashtag(hashtag = hash_tag)
    
    # Process data
    flattened_data = process_results(trending)

    # # Export data to JSON
    # with open('export.json', 'w') as f:
    #     json.dump(flattened_data, f)

    # Convert heo preprocessed data to a dataframe
    df = pd.DataFrame.from_dict(data=flattened_data, orient='index')
    df.to_csv('tiktokdata.csv', index=False)

if __name__ == '__main__':
    get_data(sys.argv[1])
    print(sys.argv[1])