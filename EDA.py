import pandas as pd
import pymysql.cursors
from secrets import DB_PASSWORD, DB_USER, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, HOST, DB, CHARSET, USER_AGENT

# import Subreddit, Submission, & Comments tables
this_connection = pymysql.connect(
    host = HOST,
    user = DB_USER,
    password = DB_PASSWORD,
    db = DB,
    charset = CHARSET,
    cursorclass = pymysql.cursors.DictCursor
    )
cursor = this_connection.cursor()
statement = "SELECT * "
statement += "FROM Subreddit "
cursor.execute(statement)
result = cursor.fetchall()
this_connection.close()

subreddit_df = pd.DataFrame.from_records(result)
print(subreddit_df.shape)

this_connection = pymysql.connect(
    host = HOST,
    user = DB_USER,
    password = DB_PASSWORD,
    db = DB,
    charset = CHARSET,
    cursorclass = pymysql.cursors.DictCursor
    )
cursor = this_connection.cursor()
statement2 = "SELECT * "
statement2 += "FROM Submission "
cursor.execute(statement2)
result = cursor.fetchall()
this_connection.close()

submission_df = pd.DataFrame.from_records(result)
print(submission_df.shape)

this_connection = pymysql.connect(
    host = HOST,
    user = DB_USER,
    password = DB_PASSWORD,
    db = DB,
    charset = CHARSET,
    cursorclass = pymysql.cursors.DictCursor
    )
cursor = this_connection.cursor()
statement3 = "SELECT * "
statement3 += "FROM Comment "
cursor.execute(statement3)
result = cursor.fetchall()
this_connection.close()

comment_df = pd.DataFrame.from_records(result)
print(comment_df.shape)

# create three DFs that join related Subreddits-Submissions-Comments
print(comment_df.columns)
# print(comment_df["link_id"]) # t3_gf9im6

print(submission_df.columns)
print(submission_df[submission_df["id"]=="gf9im6"]) # can join comment_df to submission_df on link_id & id (if you drop the prefix from link_id)

# pick a DF & perform some EDA: counts of Submissions & Comments; counts of authors; popular n-grams (1 to 3) used in titles & body; tf-idf for titles & bodies(?)