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

REDDIT = praw.Reddit(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    password = PASSWORD,
    user_agent = f"rosie by {USERNAME}", 
    username = USERNAME
    )

def make_connection():
    """
    Establish connection to DB.

    Args:
        None
    
    Returns:
        A connection instance.

    """
    this_connection = pymysql.connect(host = 'localhost',
                                        user = DB_USER,
                                        password = DB_PASSWORD,
                                        db = 'testdb',
                                        charset = 'utf8mb4',
                                        cursorclass = pymysql.cursors.DictCursor)
    
    return this_connection

def check_subreddit(name):
    """
    Check whether a Subreddit already exists in DB or not.

    Args:
        name - a string representing the name of a Subreddit

    Returns:
        Dictionary containing key-value pairs for Subreddit id and Subreddit display_name in DB.

    """
    try:
        connection = make_connection()
        cursor = connection.cursor()
        statement = "SELECT * "
        statement += "FROM Subreddit "
        statement += f"WHERE display_name = '{name}'"
        cursor.execute(statement)
        result = cursor.fetchall()
        subreddit = result[0]
        return {"id":subreddit["id"], "display_name": subreddit["display_name"]}
    except Exception as e:
        return {}

def insert_subreddits(some_subreddits):
    """
    Insert Subreddits & details into DB.

    Args:
        some_subreddits - list of strings representing a Subreddit name.

    Returns:
        None
    """
    for entry in some_subreddits:
        if check_subreddit(entry):
            print(f"Subreddit '{entry}' already in DB.")
            continue
        else:
            try:
                subreddit = REDDIT.subreddit(entry)
                insertion = (subreddit.id, subreddit.name, subreddit.display_name, subreddit.subscribers, subreddit.user_is_banned)
                connection = make_connection()
                cursor = connection.cursor()
                statement = "INSERT INTO Subreddit "
                statement += "VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(statement, insertion)
                connection.commit()
            except Exception as e:
                print(f"Error in insert_subreddits: {e}.")
                connection.close()

def main():
    """
    Main function for control flow.

    Args:
        None

    Returns:
        None
    """
    some_subreddits = ["worldnews", "offbeat", "news", "AskReddit"]
    insert_subreddits(some_subreddits)

if __name__ == "__main__":
    main()
    
# FROM CL, can log into DB using 'mysql -u bryan -p testdb'