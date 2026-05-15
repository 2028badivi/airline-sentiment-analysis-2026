"""
I made this file to contain the BedrockClient class, which will be responsible for calling the Bedrock model endpoint and getting the sentiment analysis result. This will be used in the processor.py file when I call the model endpoint, and I will pass the system prompt and the user prompt as part of the body of the request to the model endpoint. I based this request off of the Bedrock documentation: https://aws.amazon.com/blogs/aws/anthropics-claude-3-haiku-model-is-now-available-in-amazon-bedrock/.    I did not know how to use this initially so I checked the docs
"""

# imports for aws sdk and fetching the config vars
import boto3
import json
from src.config import BEDROCK_MODEL_ID_NUMBER
from src.config import AWS_REGION_ID



class bedrock_client:
    def __init__(self):
        """
        each instance of bedrock_client should have an instance variable for 
        """
        self.client = boto3.client("bedrock-runtime",region_name=AWS_REGION_ID)    
        #initialized the client runtime and sets the boto client as an instance variable



    def analyze_sentiment(self, tweetTextContent: str) -> dict:   #returns dictionary since that's the bedrock model output
        """
        this method will make a request to send a tweet to Bedrock and then return the Sentiment Analysis Results
        """
        try: #I added a try-catch block because of potential  errors, and I think it's important to log that.  


            the_prompt = f"Tweet: {tweetTextContent}" #The user prompt will bui ld off of this f-string. 

            response = self.client.converse(
                modelId=BEDROCK_MODEL_ID_NUMBER,
                messages=[{"role":"user","content":[{"text": the_prompt}]}],  #user (role) prompt
                system=[{"text":get_system_prompt()}],                       #this will just now add the system prompt to the request
                inferenceConfig={"maxTokens":10, "temperature":0.0}   # setting the max tokens to 10 since we only need a simple classification of positive, negative, or neutral, and setting the temperature to 0 to reduce randomness and increase the likelihood of getting a consistent response (since we want the same input to always yield the same output for sentiment analysis cuz consistency is imoportant especially in cases like this).
            )
            the_raw_output=response['output']['message']['content'][0]['text'].strip().lower()

            # # processing the output
            # sentiment=the_raw_output.replace(".", "").replace(",", "").strip() #strip # just in case there is any punctuation or extra whitespace, just cuz we want to remove that to get a simple and clean classification for sentiment.
            # if sentiment not in ["positive", "negative", "neutral"]:
            #     sentiment = "neutral"  # this would be the default/fallback just to be safe


            #note: I am utilizing  ternary encoding of the qualitative observations (postiive negative neutral) into numerical represenetations to minimize token usage and maximize efficiency in processing/parsing

            sentiment = the_raw_output.strip()
            if len(the_raw_output) != 1 or sentiment not in ["1", "-1", "0"]:
                sentiment = "neutral"  # ASSUMPTION: defaulting to neutral if the output is not exactly one character (which shouldn't ever be the case if the model follows instructions correctly)
            elif sentiment == "1":
                sentiment = "positive"
            elif sentiment == "-1":
                sentiment = "negative"
            else:
                sentiment = "neutral"



        #

           
 
#
            return {"sentiment": sentiment, "raw_response": the_raw_output, "confidence": 0.85}  # im just going to assume that Claude would probably get too confident (and hallucinate unnecesary indicators) with temperature closer to 0 but im not sure and I might need to adjust this accordingly.
            

        except Exception as e:
            print(f"There was an ERROR whille attempting to call Claude Haiku (via Bedrock): \n{e}\n Returning default neutral sentiment with confidence 0.0 as a default fallback due to error.")
            return {"sentiment":"neutral","raw_response":"error", "confidence":0.0}


# fetching  the system prompt from prompt.py
from src.prompt import get_system_prompt




"""
a thought for the future:
ask ai to return float instead of just -1, 0, 1 for sentiment, which would be more useful and would give us more granularity in the sentiment analysis results. for example, it could return a float between -1 and 1, where -1 is very negative, 0 is neutral, and 1 is very positive. this would allow us to capture more nuance in the sentiment of the tweets, rather than just categorizing them into three buckets. We could also set a threshold for what we consider to be positive or negative sentiment based on the float value (e.g., anything above 0.5 is positive, anything below -0.5 is negative, and anything in between is neutral). This would be a more sophisticated approach to sentiment analysis and could provide more insights from the data. it could also open doors to another column in the output s3 df for sentiment "confidence" score or something, which could be interesting to analyze in addition to the predicted sentiment category.
"""