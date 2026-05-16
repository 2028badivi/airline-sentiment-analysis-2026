# this file contains the S3 bucket names, model ID, rate limit, etc. so that I can easily change it later


import os
from dotenv import load_dotenv

load_dotenv()



AWS_REGION_ID = os.getenv("AWS_REGION_ID", "us-east-1")
S3_INPUT_BUCKET = os.getenv("S3_INPUT_BUCKET", "airline-sentiment-input-bhavesh")
S3_OUTPUT_BUCKET = os.getenv("S3_OUTPUT_BUCKET", "airline-sentiment-output-bhavesh")



BEDROCK_MODEL_ID_NUMBER = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

MIN_TWEETS_TO_PROCESS = 100
DEFAULT_RATE_LIMIT = 10
MAX_RATE_LIMIT = 20            #need to adjust this later





"""
I was searching for a potential model endpoint for the AI that AWS Bedrock offers,
and I chose to use Claude Haiku because it's fast and cheap and made for quick responses. 
This takes out the problems of not getting the result in time, which allows for us to comfortably
control the time it takes and any kind of rate limiting under the 10 requests/second requirement.

this is a sample bash command for how to call the model endpoint using the AWS CLI, which I will be doing in the processor.py file:


aws bedrock-runtime invoke-model \
     --model-id anthropic.claude-3-haiku-20240307-v1:0 \
     --body "{\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"text\",\"text\":\"Write the test case for uploading the image to Amazon S3 bucket\\n\"}]}],\"anthropic_version\":\"bedrock-2023-05-31\",\"max_tokens\":2000,\"temperature\":1,\"top_k\":250,\"top_p\":0.999,\"stop_sequences\":[\"\\n\\nHuman:\"]}" \
     --cli-binary-format raw-in-base64-out \
     --region us-east-1 \
     invoke-model-output.txt

     

found at https://aws.amazon.com/blogs/aws/anthropics-claude-3-haiku-model-is-now-available-in-amazon-bedrock/
     
     
this is just a note for myself later to remind myself of the model endpoint and how to call it, and also to explain why I chose this model endpoint over the others that AWS Bedrock offers.

"""
