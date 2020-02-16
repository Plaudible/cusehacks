import praw
import time
import re
from praw.models import Comment
from imgurpython import ImgurClient
from fryer import doBot
# from auth import authenticate

f = open("api.txt", "r")  # api values stored in "api.txt."
api_id = (f.readline())  # id line
api_secret = (f.readline())  # secret line
api_id = api_id[:-1] 
api_secret = api_secret[:-1]

reddit = praw.Reddit(client_id=api_id,#reddit api initialization
                     client_secret=api_secret,
                     username=HIDDEN,
                     password=HIDDEN,
                     user_agent=HIDDEN)


def search():
    unread_mentions = [] #keeps track of the unread messages

    for message in reddit.inbox.unread(limit=None): #marks read messages to prevent repeats
        subject = message.subject.lower()
        if subject == 'username mention' and isinstance(message, praw.models.Comment):
            unread_mentions.append(message)
            message.mark_read()

    for x in unread_mentions: #parse submission
        submission = x.submission.url 
        subparse = str(submission)
        if str(x.body) == '/u/lazer_eye_bot': #post input handling, no image link
            if ".png" in subparse or ".jpg" in subparse or ".jpeg" in subparse:
                print(submission)
                result = str(process(submission))
                x.reply(result)
                print("Link posted!")
            else:
                x.reply('The format of this post does not support laser eyes :( .jpg or .png please!')
                print("Unsupported format!")
        else: #image link input handling
            urlfinder = str(x.body)
            print(re.search("(?P<url>https?://[^\s]+)", urlfinder).group("url"))
            result = process(urlfinder)
            x.reply(result)

def process(url):

    imgup = doBot(url) #imgur API initialization and authentication
    imgup.save('godhelpusall.jpg')
    client = ImgurClient(HIDDEN,HIDDEN)
    config = { #upload descriptions
        'album': None,
        'name': 'Deep fried',
        'title': 'Delicious',
        'description': 'This image is officially blessed'
    }

    print("Uploading image... ")
    finalurl = str(client.upload_from_path('godhelpusall.jpg', config=config, anon=False)) #upload image
    finalurl = re.search("(?P<url>https?://[^\s]+)", finalurl).group("url") #remove non-URL clutter
    print("Done")
    return(finalurl) #return the final url to message reply above

if __name__ == "__main__":
    while True:
        search() #REMINDER: with not enough karma, it can only return an output every 10 minutes!
        time.sleep(5) #sleep to avoid exceeding rate limit
