"""
These are just some functions I thought of adding to load the tweets from S3 and saving results back to S3.
"""
 
#imports

import json
import csv
import io
from datetime import datetime

#aws py sdk
import boto3

#config vars
from src.config import S3_OUTPUT_BUCKET, AWS_REGION_ID




##to initalize the S3 client, which will be used to load the tweets from S3 and save the results back to S3. I will be using this in the processor.py file when I call the functions to load the tweets and save the results.
the_s3=boto3.client("s3", region_name=AWS_REGION_ID)


def load_tweets_from_s3(bucket:str,key:str) -> list:
    """this will downlaod the csv from S3 and load into a list of dictionaries"""
    res=the_s3.get_object(Bucket=bucket,Key=key)
    csv_content = res['Body'].read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(csv_content))
    return list(reader)



"""

"""





def save_results_to_s3(results:list,original_filename:str):  #planning on making it "sentiment_results" or something like that, but for now just keeping it as the original filename with a json extension just to keep it simple, and also to make it easier to track which results correspond to which input file.
    """this will save the processing results to S3 in JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_key = f"processed/{timestamp}_{original_filename.replace('.csv', '.json')}" # to convert to json from csv and to save in the processed folder in the output bucket, and to include a timestamp in the filename to avoid overwriting any existing files in S3.
    
    print(f"Attempting to save results to s3://{S3_OUTPUT_BUCKET}/{json_key}")
    the_s3.put_object(Bucket=S3_OUTPUT_BUCKET,Key=json_key,Body=json.dumps(results, indent=2),ContentType="application/json"
    )
    print(f"Results saved to s3://{S3_OUTPUT_BUCKET}/{json_key}")


