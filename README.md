# rosie
<img src="https://farm1.staticflickr.com/69/164954797_474fbdb161_z.jpg" width="150" height="150" />

## A project focused on NLP and chatbots. Details and code to be updated as possible.

Guide to files:
* **build_cache.py**
  * Set up a local MariaDB database.
  * The DB features tables for Subreddit, Submission, and Comment.
  * Generally, this only needs to be called once as it drops any existing tables. 
* **crawl.py**
  * Scrape the Subreddits specified in a file named "subreddits.csv".
  * Relies on [PRAW](https://praw.readthedocs.io/en/latest/) and a secrets.py file you will have to supply to set up the DB.
  * Only the newest submissions and their comments for the given Subreddits are scraped.
  * Attributes currently collected, among others, include:
    * Subreddit.id
    * Subreddit.display_name
    * Subreddit.subscribers
    * Submission.author
    * Submission.title
    * Submission.score
    * Submission.num_comments
    * Comment.body
    * Comment.score
* **export_db_tables.py**
  * Output a .csv containing all records from the Comment table in the DB.
  * Files are saved in a directory named "data" and the file name features the current time stamp.
* **EDA.ipynb**
  * Import the .csv created through export_db_tables.
  * Perform exploratory data analysis of the records.
  * Explore linguistic features of the records, the distribution of scores awarded, the distribution of the length of the content in the comments, as well as ngrams.
* **EDA_pyspark.ipynb**
  * Utilize a parquet file available on U-M's [Cavium cluster](https://arc-ts.umich.edu/cavium/).
  * The dataset features +2.8 billion records from Reddit from 2005 to 2016.
  * Explore the structure of the data.
  * Generate counts of posts per year.
  * Output a 1% sample stratified by year for deeper analysis.
* **EDA_pyspark_one_perct.ipynb**
  * Deeper exploration of a sample of the original dataset.
  * Identify and remove posts from bots and deleted users. We are primarily interested in posts from humans with content in 'body'.
  * Analyze the average lengths of posts, the number of posts per day, the IQR for scores awarded to posts, etc. in various Subreddits, 

Image from [Toby Silver on Flickr](https://flickr.com/photos/tobysilver/164954797)
