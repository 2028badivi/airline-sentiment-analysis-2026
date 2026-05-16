import json
import csv
import io


from src.bedrock_client import bedrock_client
from src.rate_limiter import RateLimiter


import boto3
from datetime import datetime





#the boto client to pull the data csv from s3 and to save the results back to s3
s3_client = boto3.client('s3')






def lambda_handler(event, context):
    
    
    #i added the try catch for better error handling cuz there are a bunch of errors that are happening currently in s3
    try:
        print("The Lambda has been triggered by some kind of S3 event")
        
        record=event['Records'][0]
        
        bucket=record['s3']['bucket']['name']
        key  = record['s3']['object']['key']
        
        print(f"Currently Processing the file: s3://{bucket}/{key}")
        


        
        response = s3_client.get_object( Bucket=bucket,Key=key)
        
        
        
        
        csv_content = response['Body'].read().decode('utf-8')
        



        reader = csv.DictReader(io.StringIO(csv_content))
        
        
        tweets = list(reader)
        
        print(f"!!!! Found {len(tweets)} tweets")
        







        bedrock = bedrock_client()
       
        rate_limiter = RateLimiter(10)
      
        results = []
        
        for idx, row in enumerate(tweets[:100]):  # Process max 100
            
            
            
            if 'text' not in row or not row['text'].strip():
                continue
                
          
          
          
          
            tweet_text = row['text']
       
       
       
            tweet_id = row.get('tweet_id', idx)
            
            result = bedrock.analyze_sentiment(tweet_text)


            processed_result = {
                "tweet_id": str(tweet_id),
                "text": tweet_text,
           
                "predicted_sentiment": result["sentiment"],
                "confidence": result["confidence"],
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(processed_result)
            
            rate_limiter.wait()
            
            if (idx + 1) % 20 == 0: print(f"Processed {idx + 1}/{len(tweets)} tweets")

        # Use the utility function to save results (this includes debug logging)
        from src.utils import save_results_to_s3
        save_results_to_s3(results, key.split('/')[-1])

        print(f"SUCCESS!!!!!! Sentiment analysis completed!")
        



        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'SUCCESS!!!!!! Sentiment analysis completed!',
                'tweets_processed': len(results)
            })
        }
        


    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }