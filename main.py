import praw
import time
import re
from praw.models import Comment

f = open("api.txt", "r")  # api values stored in "api.txt."
api_id = (f.readline())  # id line
api_secret = (f.readline())  # secret line
api_id = api_id[:-1]
api_secret = api_secret[:-1]

reddit = praw.Reddit(client_id=api_id,
                     client_secret=api_secret,
                     username=HIDDEN,
                     password=HIDDEN,
                     user_agent='<console:reddit_bot:0.0.1')


def search():
    unread_mentions = []

    for message in reddit.inbox.unread(limit=None):
        subject = message.subject.lower()
        if subject == 'username mention' and isinstance(message, praw.models.Comment):
            unread_mentions.append(message)
            message.mark_read()

    for x in unread_mentions:
        submission = x.submission.url
        subparse = str(submission)
        if str(x.body) == '/u/lazer_eye_bot':
            if ".png" in subparse or ".jpg" in subparse or ".jpeg" in subparse:
                print(submission)
                result = str(process(submission))
                # x.reply(result) RESPOND WITH OUTPUT IMAGE
                print("Link posted!")
            else:
                # x.reply('The format of this post does not support lazer eyes :(')
                print("Unsupported format!")
        else:
            urlfinder = str(x.body)
            print(re.search("(?P<url>https?://[^\s]+)", urlfinder).group("url"))
            result = process(urlfinder)
            # x.reply(result) #RESPOND WITH OUTPUT IMAGE

def process(url):
    print('Processing...')
    finalurl = "whatever" # DO IMAGE PROCESSING HERE
    return(finalurl)

while True:
    search()
    time.sleep(5)
