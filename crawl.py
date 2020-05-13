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
        name - a string indicating the likely display_name of a Subreddit.

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

def insert_subreddits(these_subreddits):
    """
    Insert Subreddits & details into DB.

    Args:
        these_subreddits - list of strings representing a Subreddit name.

    Returns:
        result - a list of Subreddit ids in the DB.
    """
    result = []

    for entry in these_subreddits:
        found_subreddit = check_subreddit(entry)
        if found_subreddit:
            print(f"Subreddit '{entry}' already in DB ...")
            result.append(found_subreddit["display_name"])
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

                result.append(subreddit.display_name)
            except Exception as e:
                print(f"Error in insert_subreddits: {e}.")
                connection.close()

    return result

def get_submissions(these_names):
    for entry in these_names:
        # get latest Submissions from Subreddit
        # check if Submissions are in DB already
        # if already in DB then capture that & continue
        # else add to DB, capture that, & continue
        print(entry)
        this = REDDIT.subreddit(entry).new()
        count = 0
        for i in this[1]: #TODO get newest Submissions & check if they already exist in DB or not
            count += 1
        print(count)

def main():
    """
    Main function for control flow.

    Args:
        None

    Returns:
        None
    """
    these_subreddits = ["worldnews", "offbeat", "news", "AskReddit"]
    subreddit_names = insert_subreddits(these_subreddits)

    # gather newest Submissions from Subreddits
    get_submissions(subreddit_names)

if __name__ == "__main__":
    main()
    
# FROM CL, can log into DB using 'mysql -u bryan -p testdb'