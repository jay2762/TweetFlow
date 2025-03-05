import tweepy
import time

# Set up your Twitter API v2 Bearer Token (from the Developer Portal)
bearer_token = "AAAAAAAAAAAAAAAAAAAAAF28zAEAAAAAgWCXrQE2rVEPlIh4vMmWvPIZ9Ss%3DdCWXOpgyuFerXnjGPvsstd9rFsRY3xOX7yyPYWMGXrUNEfURUN"

# Create a Tweepy client object for Twitter API v2
client = tweepy.Client(bearer_token=bearer_token)

# Function to fetch tweets using Twitter API v2
def fetch_tweets(username):
    retries = 0
    while retries < 5:  # Try up to 5 times
        try:
            # Get user info using username
            user_response = client.get_user(username=username)
            user_id = user_response.data.id  # Extract user ID

            # Fetch tweets using the user ID (using max_results to limit the number)
            tweets = client.get_users_tweets(id=user_id, max_results=5, tweet_fields=["created_at", "text", "public_metrics"])

            # Refine and store tweets in the desired format
            tweet_list = []
            for tweet in tweets.data:
                refined_tweet = {
                    "user": username,
                    "text": tweet.text,
                    "favorite_count": tweet.public_metrics['like_count'],
                    "retweet_count": tweet.public_metrics['retweet_count'],
                    "created_at": tweet.created_at
                }
                tweet_list.append(refined_tweet)

            # Print the refined tweet information
            for tweet in tweet_list:
                print(tweet)

            return  # Return if successful
        except tweepy.errors.TooManyRequests as e:
            # If rate limit is exceeded, backoff gradually
            wait_time = 2 ** retries  # Exponential backoff (2^retries)
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)  # Wait before retrying
            retries += 1  # Increment retry counter
    print("Max retries reached. Please try again later.")

# Fetch and print tweets from "elonmusk"
fetch_tweets("elonmusk")
