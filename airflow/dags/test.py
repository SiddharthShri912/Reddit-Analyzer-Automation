import praw
import pymongo
# Set up your Reddit API credentials
client_id = 'qkE1j44jKtqFl1NA9CHqiQ'
client_secret = 'A0RyHUl8pssdzJC1qUfICdzWPvABLw'
user_agent = 'python:DAG project:v1.0 (by u/GlumPlankton3997)'  # Describe your app

# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Specify the subreddit you want to scrape
subreddit_name = 'worldnews'
subreddit = reddit.subreddit(subreddit_name)

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
db = mongo_client['reddit_data']  # Replace with your desired database name
collection = db['reddit_posts']  # Replace with your desired collection name

# Retrieve recent posts
for submission in subreddit.new(limit=5):
    post_data = {
        'title': submission.title,
        'text': submission.selftext,
        'upvotes': submission.score
    }
    collection.insert_one(post_data)
    print(f"Post saved: {submission.title}")

print("Data saved to MongoDB!")

# Close the MongoDB connection
mongo_client.close()
