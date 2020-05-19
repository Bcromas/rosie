import pandas as pd
import pymysql.cursors
from secrets import DB_PASSWORD, DB_USER, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, HOST, DB, CHARSET, USER_AGENT

# import Subreddit, Submission, & Comments tables
# this_connection = pymysql.connect(
#     host = HOST,
#     user = DB_USER,
#     password = DB_PASSWORD,
#     db = DB,
#     charset = CHARSET,
#     cursorclass = pymysql.cursors.DictCursor
#     )
# cursor = this_connection.cursor()
# statement = "SELECT * "
# statement += "FROM Subreddit "
# cursor.execute(statement)
# result = cursor.fetchall()
# this_connection.close()

# subreddit_df = pd.DataFrame.from_records(result)
# print(subreddit_df.shape)

# this_connection = pymysql.connect(
#     host = HOST,
#     user = DB_USER,
#     password = DB_PASSWORD,
#     db = DB,
#     charset = CHARSET,
#     cursorclass = pymysql.cursors.DictCursor
#     )
# cursor = this_connection.cursor()
# statement2 = "SELECT * "
# statement2 += "FROM Submission "
# cursor.execute(statement2)
# result = cursor.fetchall()
# this_connection.close()

# submission_df = pd.DataFrame.from_records(result)
# print(submission_df.shape)

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
# print(comment_df.shape)

# # create three DFs that join related Subreddits-Submissions-Comments
# print(comment_df.columns)
# # print(comment_df["link_id"]) # t3_gf9im6

# print(submission_df.columns)
# print(submission_df[submission_df["id"]=="gf9im6"]) # can join comment_df to submission_df on link_id & id (if you drop the prefix from link_id)

# # pick a DF & perform some EDA: counts of Submissions & Comments; counts of authors; popular n-grams (1 to 3) used in titles & body; tf-idf for titles & bodies(?)

#######################
### EDA w/ Comments ###

#* columns are 'insert_update_ts', 'id', 'link_id', 'author', 'body', 'score','permalink', 'retrieved'
# print(comment_df.columns)

#* body_len has mean of 149 but large std dev of 234
comment_df["body_len"] = comment_df.apply(lambda x: len(x["body"]), axis = 1)
# print(comment_df["body_len"].describe())

from nltk import ngrams

comment_df["body_2gram"] = comment_df.apply(lambda x: [i for i in ngrams(x["body"].lower().split(),2)], axis = 1)
# print(comment_df[["body","body_2gram"]].sample(3))

comment_df["body_3gram"] = comment_df.apply(lambda x: [i for i in ngrams(x["body"].lower().split(),3)], axis = 1)
# print(comment_df[["body","body_3gram"]].sample(3))

import collections
counter_2gram = collections.Counter()
for i in comment_df["body_2gram"]:
    counter_2gram.update(i)
# print(counter_2gram.most_common(10))

counter_3gram = collections.Counter()
for i in comment_df["body_3gram"]:
    counter_3gram.update(i)
# print(counter_3gram.most_common(10))


#* other Comments featuring "the best tl;dr"
# | fqvygmm |
# | fqwpmbp |
# | fqwpoc7 |
# | fqwpp2k |
# | fqwt7gh |
# | fqwt807 |
# | fqwt8y8 |
# | fqxvnkn |
# | fqy3p49 |
# | fqy3ptb |
# | fqy3qh4 |
# | fqy3r7l |
print(comment_df[(comment_df["id"]=="fqovhw6")|(comment_df["id"]=="fqvygmm")]["permalink"])