"""
I made this file to contain the BedrockClient class, which will be responsible for calling the Bedrock model endpoint and getting the sentiment analysis result. This will be used in the processor.py file when I call the model endpoint, and I will pass the system prompt and the user prompt as part of the body of the request to the model endpoint. I based this request off of the Bedrock documentation: https://aws.amazon.com/blogs/aws/anthropics-claude-3-haiku-model-is-now-available-in-amazon-bedrock/.    I did not know how to use this initially so I checked the documentation.
"""

# imports and fetching the config vars
import boto3
import json
from src.config import BEDROCK_MODEL_ID, AWS_REGION

class BedrockClient:
    def __init__(self):
        self.client = boto3.client("bedrock-runtime",region_name=AWS_REGION)

    def analyze_sentiment(self, tweet_text: str) -> dict:
        """
        This function will make a request to send a tweet to Bedrock and then return the Sentiment Analysis Results
        """
        try: #I added a try-catch block because of potential  errors, and I need to log that.  


            user_prompt = f"Tweet: {tweet_text}" #The user prompt will build off of this String. 

            response = self.client.converse(
                modelId=BEDROCK_MODEL_ID,
                messages=[{"role":"user","content":[{"text": user_prompt}]}],
                system=[{"text":get_system_prompt()}],
                inferenceConfig={"maxTokens": 10, "temperature": 0.0}
            )

            the_raw_output=response['output']['message']['content'][0]['text'].strip().lower()

            # # processing the output
            # sentiment=the_raw_output.replace(".", "").replace(",", "").strip() #strip # just in case there is any punctuation or extra whitespace, just cuz we want to remove that to get a simple and clean classification for sentiment.
            # if sentiment not in ["positive", "negative", "neutral"]:
            #     sentiment = "neutral"  # this would be the default/fallback just to be safe


            sentiment = the_raw_output.strip()
            if len(the_raw_output) != 1:
                sentiment = "neutral"  # default to neutral if the output is not exactly one character (which should be the case if the model follows instructions correctly)
            elif sentiment == "1":
                sentiment = "positive"
            elif sentiment == "-1":
                sentiment = "negative"
            else:
                sentiment = "neutral"



#
            return {
                "sentiment": sentiment,
                "raw_response": the_raw_output,
                "confidence": 0.85  # im going to assume that Claude would probably get too confident (and hallucinate unnecesary indicators) with temperature closer to 0
            }

        except Exception as e:
            print(f"There was an ERROR whille attempting to call Claude Haiku (via Bedrock): \n{e}\n Returning default neutral sentiment with confidence 0.0 as a default fallback due to error.")
            return {"sentiment":"neutral","raw_response":"error", "confidence":0.0}


# fetching the system prompt from prompt.py
from src.prompt import get_system_prompt