from secrets import DB_PASSWORD, DB_USER
import pymysql.cursors

DBNAME = 'testdb'

def db_setup():
    """
    Drops and creates the following tables: Subreddit, Submission, Comment.

    Args:
        None

    Returns:
        None
    """
    # Connect to the database
    try:
        connection = pymysql.connect(host = 'localhost',
                                    user = DB_USER,
                                    password = DB_PASSWORD,
                                    db = DBNAME,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor)
        cursor = connection.cursor()
    except Exception as e:
        print(f"Error creating DB: {e}.")
        connection.close()

    ###################
    ### DROP TABLES ###

    # Drop Subreddit table
    try:
        statement = """
        DROP TABLE IF EXISTS Subreddit;
        """
        cursor.execute(statement)
        connection.commit()
    except Exception as e:
        print(f"Error dropping Subreddit table: {e}.")
        connection.close()

    # Drop Submission table
    try:
        statement = """
        DROP TABLE IF EXISTS Submission;
        """
        cursor.execute(statement)
        connection.commit()
    except Exception as e:
        print(f"Error dropping Submission table: {e}.")
        connection.close()

    # Drop Comment table
    try:
        statement = """
        DROP TABLE IF EXISTS Comment;
        """
        cursor.execute(statement)
        connection.commit()
    except Exception as e:
        print(f"Error dropping Comment table: {e}.")
        connection.close()

    #####################
    ### CREATE TABLES ###

    # Create Subreddit table
    try:
        statement = """
        CREATE TABLE Subreddit(
            insert_update_ts TIMESTAMP,
            id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            display_name VARCHAR(100) NOT NULL,
            subscribers INT NOT NULL,
            user_is_banned BOOLEAN NOT NULL
            );
        """
        cursor.execute(statement)
        connection.commit()
    except Exception as e:
        print(f"Error creating Subreddit table: {e}.")
        connection.close()

    # Create Submission table
    try:
        statement = """

        CREATE TABLE Submission(
            insert_update_ts TIMESTAMP,
            id VARCHAR(100) PRIMARY KEY,
            subreddit_id VARCHAR(100) NOT NUll,
            author VARCHAR(100) NOT NULL,
            created_utc VARCHAR(100) NOT NULL,
            is_original_content BOOLEAN NOT NULL,
            locked BOOLEAN NOT NULL,
            name VARCHAR(100),
            title VARCHAR(100),
            num_comments INT NOT NULL,
            score INT NOT NULL,
            permalink VARCHAR(100) NOT NULL,
            retrieved TIMESTAMP NOT NULL
        );
        """
        cursor.execute(statement)
        connection.commit()
    except Exception as e:
        print(f"Error creating Submission table: {e}.")
        connection.close()

    # Create Comment table
    try:
        statement = """
        CREATE TABLE Comment(
            insert_update_ts TIMESTAMP,
            id VARCHAR(100) PRIMARY KEY,
            link_id VARCHAR(100) NOT NULL,
            author VARCHAR(100) NOT NULL,
            body BLOB NOT NULL,
            score INT NOT NULL,
            permalink VARCHAR(100) NOT NULL,
            retrieved TIMESTAMP NOT NULL
        );
        """
        #* link_id = submission_id
        cursor.execute(statement)
        connection.commit()
    except Exception as e:
        print(f"Error creating Comment table: {e}.")
        connection.close()

if __name__ == "__main__":
    db_setup()

# FROM CL, can log into DB using 'mysql -u bryan -p testdb'