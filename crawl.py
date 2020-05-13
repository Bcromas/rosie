import praw
import pymysql.cursors

#initialize global vars, set to blank
DB_PASSWORD = DB_USER = CLIENT_ID = CLIENT_SECRET = USERNAME = PASSWORD = ''

#start getting global vars from secrets.txt
with open("secrets.txt") as secrets:
    for line in secrets:
        line_split = line.split("=")
        if line_split[0].strip().lower() == "client_id":
            CLIENT_ID = line_split[1].strip()
        elif line_split[0].strip().lower() == "client_secret":
            CLIENT_SECRET = line_split[1].strip()
        elif line_split[0].strip().lower() == "username":
            USERNAME = line_split[1].strip()
        elif line_split[0].strip().lower() == "password":
            PASSWORD = line_split[1].strip()
        elif line_split[0].strip().lower() == "db_user":
            DB_USER = line_split[1].strip()
        elif line_split[0].strip().lower() == "db_password":
            DB_PASSWORD = line_split[1].strip()
#end getting global vars from secrets.txt

reddit = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, password = PASSWORD,user_agent = f"rosie by {USERNAME}", username = USERNAME)

def insert_subreddits(some_subreddits):
    """
    Attempts to insert Subreddits & details into DB. 

    Args:
        some_subreddits - list of strings representing a Subreddit name.

    Returns:
        None
    """
    for entry in some_subreddits:
        try:
            subreddit = reddit.subreddit(entry)
            insertion = (subreddit.id, subreddit.name, subreddit.display_name, subreddit.subscribers, subreddit.user_is_banned)
            connection = pymysql.connect(host = 'localhost',
                                    user = DB_USER,
                                    password = DB_PASSWORD,
                                    db = 'testdb',
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor)
            cursor = connection.cursor()
            statement = "INSERT INTO Subreddit "
            statement += "VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(statement, insertion)
            connection.commit()
        except Exception as e:
            print(f"Error in test insert: {e}.")
            connection.close()

def main():
    """
    Main function for control flow.

    Args:
        None

    Returns:
        None
    """
    some_subreddits = ["worldnews", "offbeat", "news"]
    insert_subreddits(some_subreddits)

if __name__ == "__main__":
    main()
    
# FROM CL, can log into DB using 'mysql -u bryan -p testdb'