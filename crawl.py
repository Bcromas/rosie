import praw
import pymysql.cursors

#initialize global vars, set to blank
CLIENT_ID = CLIENT_SECRET = USERNAME = PASSWORD = ''

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
#end getting global vars from secrets.txt

# reddit = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, password = PASSWORD,user_agent = f"rosie by {USERNAME}", username = USERNAME)

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='bryan',
                             password='1234',
                             db='testdb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()

if __name__ == "__main__":
    print("in main")