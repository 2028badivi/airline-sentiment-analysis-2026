"""
I need this for the lambda 
"""
import json
from src.processor import process_tweets
from src.rate_limiter import RateLimiter






def lambda_handler(event,context):
    """
    
    This would be triggered when a CSV file is uploaded to the input S3 bucket.
    """
    
    

    
    try:
        print("Lambda triggered by some kind of S3 event")
        
        # i asked AI to help explain how to access the file info from the s3 event
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"Processing file for {key}: s3://{bucket}/{key}")
        



        
        results = process_tweets(bucket,key,rate_limit=10) #teh default rate limit
        



        return {
            'statusCode':200,
            'body':json.dumps({
                'message':'Sentiment analysis has completed successfully! WTG!',
                'tweets_processed':len(results)
            })}
        


    except Exception as e:

        
        print(f"Error: {str(e)}")
        
        
        return { 
            'statusCode':500,
            'body':json.dumps({'error':str(e)}) #turn the error into json
        }   