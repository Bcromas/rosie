from secrets import DB_PASSWORD, DB_USER, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD
import praw
import pymysql.cursors

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
        result - a list of 2-tuples containing Subreddits display_names & ids in the DB.
    """
    result = []

    for entry in these_subreddits:
        found_subreddit = check_subreddit(entry)
        if found_subreddit:
            print(f"Subreddit '{entry}' already in DB ...")
            result.append((found_subreddit["display_name"], found_subreddit["id"]))
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

                result.append((subreddit.display_name, subreddit.id))
            except Exception as e:
                print(f"Error in insert_subreddits: {e}.")
                connection.close()

    return result

def check_submission(this_submission):
    """
    Check whether a Submissions already exists in DB or not.

    Args:
        this_submission - a string indicating the Submission id.

    Returns:
        Boolean, True if Submission in DB False otherwise.

    """
    try:
        connection = make_connection()
        cursor = connection.cursor()
        statement = "SELECT * "
        statement += "FROM Submission "
        statement += f"WHERE id = '{this_submission}'"
        cursor.execute(statement)
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in check_submission: {e}")
        return False

def insert_submissions(these_names):
    """
    Check if Submissions exist in DB & add them if they don't.

    Args:
        these_names - a list of 2-tuples containing a Subreddit name & id.

    Returns:

    """
    for this_name, this_id in these_names:
        # get latest Submissions from Subreddit
        # check if Submissions are in DB already
        # if already in DB then capture that & continue
        # else add to DB, capture that, & continue

        these_submissions = REDDIT.subreddit(this_name).new()
        print(f"Updating Submissions in DB for {this_name} ...")
        
        for this_id in these_submissions:
            if check_submission(this_id):
                continue
            else:
                #TODO make a call for the Submission itself & get details I want (e.g. author; see: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html)
                insertion = (str(this_id))
                connection = make_connection()
                cursor = connection.cursor()
                statement = "INSERT INTO Submission "
                statement += "VALUES (%s);"
                cursor.execute(statement, insertion)
                connection.commit()

def main():
    """
    Main function for control flow.

    Args:
        None

    Returns:
        None
    """
    these_subreddits = ["worldnews", "offbeat", "news", "AskReddit"]
    # these_subreddits = ["worldnews"]

    subreddit_names_ids = insert_subreddits(these_subreddits)

    # gather newest Submissions from Subreddits
    insert_submissions(subreddit_names_ids)

if __name__ == "__main__":
    main()
    
# FROM CL, can log into DB using 'mysql -u bryan -p testdb'