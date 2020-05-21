import datetime
import praw
import pymysql.cursors
from secrets import DB_PASSWORD, DB_USER, CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, HOST, DB, CHARSET, USER_AGENT

REDDIT = praw.Reddit(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    password = PASSWORD,
    user_agent = f"{USER_AGENT} by {USERNAME}", 
    username = USERNAME
    )

def get_subreddits(this_file):
    """
    Open a CSV file, read in Subreddits, and save them as a list.

    Args:
        this_file - the name of a CSV file containing the names of Subreddits.

    Returns:
        A list of strings representing the Subreddit names.

    """
    with open(this_file) as f:
        content = f.read().split(",")
    
    return content

def make_connection():
    """
    Establish connection to DB.

    Args:
        None
    
    Returns:
        A connection instance.

    """
    this_connection = pymysql.connect(host = HOST,
                                        user = DB_USER,
                                        password = DB_PASSWORD,
                                        db = DB,
                                        charset = CHARSET,
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
                insertion = (
                    None, subreddit.id, subreddit.name, 
                    subreddit.display_name, subreddit.subscribers, subreddit.user_is_banned
                    )
                connection = make_connection()
                cursor = connection.cursor()
                statement = "INSERT INTO Subreddit "
                statement += "VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(statement, insertion)
                connection.commit()

                result.append((subreddit.display_name, subreddit.id))
                connection.close()
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
        connection.close()
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in check_submission: {e}")
        connection.close()
        return False

def insert_submissions(these_names):
    """
    Check if a Subreddit's Submissions exist in the DB & add them if they don't.

    Args:
        these_names - a list of 2-tuples containing a Subreddit name & id.

    Returns:
        result - a list of Submission ids in the DB.

    """
    result = []

    for this_name, this_id in these_names:
        these_submissions = REDDIT.subreddit(this_name).new()
        print(f"Updating Submissions in DB for {this_name} ...")
        
        for this_id in these_submissions:
            if check_submission(this_id):
                result.append(str(this_id))
                continue #! possibly too simplistic of a check, may want to update using timestamp &| updating columns that have changed
            else:
                try: 
                    this_submission = REDDIT.submission(id = this_id)

                    insertion = (
                        None, str(this_id), this_name, 
                        str(this_submission.author), "CREATED_UTC", this_submission.is_original_content,
                        this_submission.locked, this_submission.name, this_submission.title[:100],
                        this_submission.num_comments, this_submission.score, this_submission.permalink, 
                        datetime.datetime.utcnow()
                    ) #TODO fix insert for created_UTC

                    connection = make_connection()
                    cursor = connection.cursor()
                    statement = "INSERT INTO Submission "
                    statement += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    cursor.execute(statement, insertion)
                    connection.commit()

                    result.append(str(this_id))
                    connection.close()

                except Exception as e:
                    print(f"Error in insert_submissions: {e}.")
                    connection.close()
    return result

def check_comment(this_comment):
    """
    Check whether a Comment already exists in DB or not.

    Args:
        this_comment - a string indicating the Comment id.

    Returns:
        Boolean, True if Comment in DB False otherwise.

    """
    try:
        connection = make_connection()
        cursor = connection.cursor()
        statement = "SELECT * "
        statement += "FROM Comment "
        statement += f"WHERE id = '{this_comment}'"
        cursor.execute(statement)
        result = cursor.fetchall()
        if result:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in check_comment: {e}")
        return False

def insert_comments():
    """
    Checks all Submissions in DB to see if their Comments are in DB or not.

    Args:
        None.

    Returns:
        None.

    """
    # get list of all Submissions in DB
    connection = make_connection()
    cursor = connection.cursor()
    statement = "SELECT DISTINCT id "
    statement += "FROM Submission "
    cursor.execute(statement)
    result = cursor.fetchall()
    connection.close()

    # for each Submission make a call to get all Comments
    for submission in result:
        this_submission = REDDIT.submission(id = submission["id"])
        this_comment_forest = this_submission.comments
        this_comment_forest.replace_more(limit = None)
        for comment in this_comment_forest:
            # check if comment.id is in DB, if not add it
            if check_comment(comment.id):
                continue #! possibly too simplistic of a check, may want to update using timestamp &| updating columns that have changed
            else:
                try:
                    insertion = (
                        None, comment.id, comment.link_id,
                        comment.subreddit.name, str(comment.author), comment.body,
                        comment.score, comment.permalink, datetime.datetime.utcnow()   
                    )

                    connection = make_connection()
                    cursor = connection.cursor()
                    statement = "INSERT INTO Comment "
                    statement += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    cursor.execute(statement, insertion)
                    connection.commit()
                    connection.close()

                except Exception as e:
                    print(f"Error in insert_comments: {e}")
                    connection.close()

def main():
    """
    Main function for control flow.

    Args:
        None

    Returns:
        None
    """
    these_subreddits = get_subreddits("data/subreddits.csv")

    subreddit_names_ids = insert_subreddits(these_subreddits)

    # gather newest Submissions from Subreddits
    submission_ids = insert_submissions(subreddit_names_ids)

    #TODO make call to insert_comments
    insert_comments()

if __name__ == "__main__":
    main()