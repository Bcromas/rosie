# Utility file to export tables from DB to CSV files

import pandas as pd
import pymysql.cursors
import datetime
from secrets import DB_PASSWORD, DB_USER, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, HOST, DB, CHARSET, USER_AGENT

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

timestamp = datetime.datetime.utcnow()
comment_df.to_csv(f"data/{timestamp.year}_{timestamp.month}_{timestamp.day}_Comments.csv")