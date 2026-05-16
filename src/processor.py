"""
This file would hold the main logic for the sentiment analysis clasification.
"""

#imports
from datetime import datetime
import random #samples tweets randomly
#import constants and the utils.py helper function
from src.bedrock_client import bedrock_client
from src.rate_limiter import RateLimiter
from src.utils import save_results_to_s3

from src.utils import load_tweets_from_s3





def process_tweets(bucket: str,key: str,rate_limit: int = 10):
    """
    This one will process the tweets and make sure that there is rate limiting. It will also save the results back to S3. The rate limit is set to 10 tweets per second by default, but it can be adjusted as needed (and can also be dynamically adjusted using the set_rate function in the RateLimiter class, but thatts just for extra credit for the homework).
    """
    print(f"Analyzing tweets for {key} at max {rate_limit} tweets/sec\n")



    # this will load the data from the utils function in utils.py
    tweets = load_tweets_from_s3(bucket, key)
    


    # 
    #  just making sure it has text column and that there are no missing values in the text column, because we can't analyze sentiment if there is no text, so we will just filter those out and only process the tweets that have text.
    available_tweets = [t for t in tweets if t.get('text') and t['text'].strip()]


    #Randomly selecting 
    n_to_process = 100 #threshold is max 100
    sample_size = min(n_to_process, len(available_tweets))  # just in case there are less than 100 available, we will just process all of them
    
    if sample_size < len(available_tweets):
        selected_tweets = random.sample(available_tweets, sample_size)
    else:
        selected_tweets = available_tweets

    print(f"Currently processing {len(selected_tweets)} tweets... \n") 







    bedrock = bedrock_client()
    rate_limiter = RateLimiter(rate_limit)
    results = []

    for idx, row in enumerate(selected_tweets):   #iterate through the rows and send to bedrock for analysis of sentiment, and then save the results to a list, and then save the results to s3 at the end of the procesing


        tweet_text = row['text']
        tweet_id = row.get('tweet_id', idx)
        result = bedrock.analyze_sentiment(tweet_text)

        processed_result = {
            "tweet_id":str(tweet_id),
            "text":tweet_text,
            "predicted_sentiment":result["sentiment"],
            "confidence":result["confidence"],
            # adding timestamp could be useful for figuring out when i was done and tracking sentiment over time (progressi0n)
            "timestamp":datetime.now().isoformat()
        }
        



        results.append(processed_result)
      

        rate_limiter.wait()
 
        if (idx + 1) % 20 == 0:
            print(f"Right now processing {idx + 1}/{len(selected_tweets)} tweets...")
 
    # This will save the results to s3 using the utils function in utils.py
    save_results_to_s3( results, key.split('/')[-1] )
    print("Processing completed successfully! WTG!")
    return results

