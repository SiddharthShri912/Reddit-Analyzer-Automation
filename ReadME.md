# Automatic Data Fetcher and analysis tool using Airflow

This Program automates the prcoess of fetching and processing the data from r/india for data analysis purposes.

Tech Used: Airflow, Docker, MongoDB

## How it works:
    1. There is a welcome tasks which basically prints hello, this is just a dummy task, to check the working of the tasks.
    2. The scrape Task is called, which uses the api to scrape 100 posts from r/india. 100 daily i feel is a good number, but can be increased. The data is then stored in the mongoDB server, for easy access and sorting and runnnig queries for processing.
    3. Now, the 3rd task is to connect to the mongodb server in the internal server, and sorted to find the most upvoted post and it is stored in the mongodb server for later access.
    4. Now the word Count program runs and the word count for all words are counted, many stopwords are neglected to get more meaningful data.
    5. Now, we want to write the most upvoted post on the output file so we can send it as an email, the output file is stored on the docker container so it can be accessed and sent accross as an attachment in the email.
    6. We are done with the days tasks so we can clear all the old data in the database, so we dont store alot of data.
    7. Lastly, we just have to send the text file across as an attachment in the email.
    8. We are connected to SMTP server, specifically the gmail smtp server on port 587, for encrypted data transfer.
    9. The DAG is scheduled to run daily, so everyday it will repeat these tasks, without any trigger from us.

### IT IS ALSO IMPORTANT TO IMPORT PRAW AND PYMONGO ON THE DOCKER ITSELF TO NOT RUN INTO ERRORS

The processes look like this, hence called DAGs

![plot](DAG.png)

### FUTURE PLANS AND IDEAS AND DIFFICULTIES FACED

1. I want to make a frontend program which basically allows users to subscribe to this service, but currently I am unable to find a way to send email to multiple people via input
2. NLTK package does not seem to work, it cannot download its resources in the docker enviornment and so i have to use brute force to calculate word count and also its hard to generate stop words.
3. MongoDB can be used in a better way, to optimize some queries
4. I want to add more analysis features like sentiment analysis, trends, user trends and etc.
5. Lastly, I feel like setting up my own SMTP server and send emails through that, by doing some research it came to my knowledge that I can host a SMTP server on my local device, but as of now i find it very tricky.

