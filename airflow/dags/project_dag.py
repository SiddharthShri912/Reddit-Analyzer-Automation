from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import praw
import pymongo

def print_welcome():
    print('Welcome!')

def scrape():
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
    subreddit_name = 'india'
    subreddit = reddit.subreddit(subreddit_name)

    mongo_client = pymongo.MongoClient('mongodb://host.docker.internal:27017/')
    db = mongo_client['reddit_data']  # Replace with your desired database name
    collection = db['reddit_posts']  # Replace with your desired collection name

    # Retrieve recent posts
    for submission in subreddit.new(limit=100):
        post_data = {
            'title': submission.title,
            'text': submission.selftext,
            'upvotes': submission.score
        }
        collection.insert_one(post_data)
        print(f"Post saved: {submission.title}")

def processing():
    mongo_client = pymongo.MongoClient('mongodb://host.docker.internal:27017/')
    db = mongo_client['reddit_data']  # Replace with your desired database name
    collection = db['reddit_posts']  # Replace with your desired collection name
    # Find the most upvoted post (sorted by upvotes in descending order)

    most_upvoted_post = collection.find().sort('upvotes', pymongo.DESCENDING).limit(1)

    db = mongo_client['processed']  # Replace with your desired database name
    collection = db['results']  # Replace with your desired collection name

    # Print the most upvoted post (you can process it further as needed)
    for submission in most_upvoted_post:
        print(submission)
        post_data = {
            'title': submission['title'],
            'text': submission['text'],
            'upvotes': submission['upvotes']
        }
        collection.insert_one(post_data)    
        

def processing2():
    mongo_client = pymongo.MongoClient('mongodb://host.docker.internal:27017/')
    db = mongo_client['reddit_data']  # Replace with your desired database name
    collection = db['reddit_posts']  # Replace with your desired collection name

    all_data = collection.find()

    all_post = ""
    all_title = ""
    for post in all_data:
        all_title += post.get('title')
        all_post += post.get('text')

    print(all_post)
    print(all_title)
    # Assuming you have the 'all_post' and 'all_title' strings
    combined_text = all_post + " " + all_title

    # Split the combined text into individual words based on whitespace
    all_words = combined_text.split()

    # Create a dictionary to store word frequencies
    word_freq = {}

    # Count the occurrences of each word
    for word in all_words:
        word = word.lower()  # Convert to lowercase for case-insensitivity
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    # Get the top 10 most common wordss
    most_common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    world_news_stopwords = [
    'news', 'world', 'international', 'report', 'reports', 'breaking',
    'update', 'updates', 'latest', 'headline', 'headlines', 'daily',
    'today', 'yesterday', 'tomorrow', 'source', 'sources', 'coverage',
    'coverage', 'article', 'articles', 'story', 'stories', 'read',
    'readers', 'readership', 'media', 'press', 'broadcast', 'broadcasts',
    'broadcasting', 'journalism', 'journalist', 'journalists', 'agency',
    'agencies', 'outlet', 'outlets', 'coverage', 'current', 'events',
    'event', 'breaking', 'developments', 'situation', 'context',
    'analysis', 'commentary', 'opinion', 'editorial', 'column', 'columns',
    'op-ed', 'exclusive', 'investigation', 'investigative', 'reporting',
    'correspondent', 'correspondents', 'live', 'coverage', 'press',
    'conference', 'briefing', 'interview', 'interviews', 'debate',
    'debates', 'forum', 'forums', 'panel', 'panels', 'summit', 'summits',
    'forum', 'forums', 'symposium', 'symposia', 'webinar', 'webinars',
    'town hall', 'town halls', 'townhall', 'townhalls', 'broadcast',
    'broadcasts', 'livestream', 'livestreams', 'stream', 'streams',
    'podcast', 'podcasts', 'episode', 'episodes', 'segment', 'segments',
    'feature', 'features', 'special', 'specials', 'exclusive',"the", "and", "of", "to", "in", "a", "for", "is", "on", "with",
    "you", "this", "that", "it", "from", "at", "by", "about",
    "as", "by", "from", "at", "on", "into", "over", "under", "through", "between",
    "after", "before", "during", "since", "while", "because", "although", "unless", "whether", "among","has","what","where","why","how","or","said","asked","our","see","again","see","i","us","are","say","against"]

    f = open('airflow\output.txt','w+') 
    f.write("Top words and their frequencies\n")

    for word, freq in most_common_words:
        if word in world_news_stopwords:
            continue
        else:
            print(f"{word}: {freq}")
            f.write(f"{word}: {freq}\n")
    
    f.close()

def saveTopVoted():
    mongo_client = pymongo.MongoClient('mongodb://host.docker.internal:27017/')
    db = mongo_client['processed']  # Replace with your desired database name
    collection = db['results']  # Replace with your desired collection name

    post_list = collection.find()

    f = open('airflow\output.txt', 'a+')
    f.write("Top Voted Posts\n\n")

    for p in post_list:
        f.write(f"{p['title']} {p['upvotes']}\n")
        print(p)

    f.close()

def clearDB():
    mongo_client = pymongo.MongoClient('mongodb://host.docker.internal:27017/')

    db = mongo_client['reddit_data']  # Replace with your desired database name
    collection = db['reddit_posts']  # Replace with your desired collection name

    collection.delete_many({})

    db = mongo_client['processed']  # Replace with your desired database name
    collection = db['results']  # Replace with your desired collection name

    collection.delete_many({})



dag = DAG(
    'reddit_dag',
    default_args={'start_date': days_ago(1)},
    schedule_interval='@daily',
    catchup=False,
)

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag
)

scrape_sub_reddit_task = PythonOperator(
    task_id = 'print_subreddit_posts',
    python_callable=scrape,
    dag = dag
)

processing_task = PythonOperator(
    task_id='processing',
    python_callable=processing,
    dag = dag
)

processing_2_task = PythonOperator(
    task_id='processing2',
    python_callable=processing2,
    dag = dag
)

email = EmailOperator(
    task_id='send_email',
    to='siddharthshrivastav912@gmail.com',
    subject='Test',
    html_content="""<h1>Airflow DAG Done successfully</h1> <h3>Results Attached</h3>""",
    files = ['airflow\output.txt'],
    dag = dag
)

save_top_voted_post = PythonOperator(
    task_id = 'saving_top_post',
    python_callable= saveTopVoted,
    dag=dag
)

clear_db = PythonOperator(
    task_id = "clearing_db",
    python_callable=clearDB,
    dag=dag
)

print_welcome_task >> scrape_sub_reddit_task >> processing_task >> processing_2_task >> save_top_voted_post >> clear_db >> email
