"""
This file includes rate limiting to make sure that it doesn't exceed the maximum number of tweets per second.
"""

#importing the rate limits and the time module to delay any of the requests to the model endpoint as needed
import time
from src.config import DEFAULT_RATE_LIMIT




class RateLimiter:
    def __init__(self, rate_limit:int=DEFAULT_RATE_LIMIT):  #all instannces should have the default rate limit 
        self.rate_limit=rate_limit
        self.interval = 1.0/rate_limit if rate_limit>0 else 0 #To calculate the interval and to avoid division by zero if the rate limit is negative or zero, you can just set the interval to zero, which means no waiting between requests, although we should ideally not allow that.

    def wait(self):
        """I added this so that it'll be called before each request to the model endpoint to ensure that we are not exceeding the rate limit. It will sleep for the appropriate amount of time based on the rate limit."""
        if self.interval>0: time.sleep(self.interval)

    def set_rate(self, new_rate: int):
        """this one is for the extra credit part where I can adjust the rate limit dynamically based on the number of tweets left to process and the time remaining. This will allow for more efficient processing while still adhering to the maximum rate limit."""
        if 1 <= new_rate <= 50:  # just some realistic bounds
            self.rate_limit = new_rate
            self.interval = 1.0 / new_rate
            print(f"The rate limit has been updated to {new_rate} tweets/s.")

            