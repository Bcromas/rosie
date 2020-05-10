import pymysql.cursors

#initialize global vars, set to blank
DB_PASSWORD = DB_USER = ''

DBNAME = 'testdb'

#start getting global vars from secrets.txt
with open("secrets.txt") as secrets:
    for line in secrets:
        line_split = line.split("=")
        if line_split[0].strip().lower() == "db_user":
            DB_USER = line_split[1].strip()
        elif line_split[0].strip().lower() == "db_password":
            DB_PASSWORD = line_split[1].strip()
#end getting global vars from secrets.txt

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
    # Can view columns in CL using 'SHOW COLUMNS FROM Subreddit;'
    try:
        statement = """
        CREATE TABLE Subreddit(
            id VARCHAR(100) NOT NULL,
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
            id VARCHAR(100) NOT NULL,
            title VARCHAR(100),
            author_name VARCHAR(100)
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
            id VARCHAR(100) NOT NULL,
            commentor_id VARCHAR(100),
            body_text VARCHAR(500)
        );
        """
        cursor.execute(statement)
        connection.commit()
    except Exception as e:
        print(f"Error creating Comment table: {e}.")
        connection.close()

if __name__ == "__main__":
    db_setup()

# FROM CL, can log into DB using 'mysql -u bryan -p testdb'