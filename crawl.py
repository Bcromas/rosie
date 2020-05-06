import praw

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

reddit = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, password = PASSWORD,user_agent = f"rosie by {USERNAME}", username = USERNAME)

if __name__ == "__main__":
    print("in main")