#!/usr/bin/python
import praw
import re
from pushshift_py import PushshiftAPI

# Quotes taken from: http://www.imdb.com/character/ch0007553/quotes
marvin_quotes = \
    [
        " I've calculated your chance of survival, but I don't think you'll like it. ",
        " Do you want me to sit in a corner and rust or just fall apart where I'm standing?",
        "Here I am, brain the size of a planet, and they tell me to take you up to the bridge. Call that job satisfaction? Cause I don't. ",
        "Here I am, brain the size of a planet, and they ask me to pick up a piece of paper. ",
        " It gives me a headache just trying to think down to your level. ",
        " You think you've got problems. What are you supposed to do if you are a manically depressed robot? No, don't even bother answering. I'm 50,000 times more intelligent than you and even I don't know the answer.",
        "Zaphod Beeblebrox: There's a whole new life stretching out in front of you. Marvin: Oh, not another one.",
        "The first ten million years were the worst. And the second ten million... they were the worst too. The third ten million I didn't enjoy at all. After that, I went into a bit of a decline. ",
        "Sorry, did I say something wrong? Pardon me for breathing which I never do anyway so I don't know why I bother to say it oh God I'm so depressed. ",
        " I have a million ideas, but, they all point to certain death. ",

    ]

reddit = praw.Reddit('GeneralBot')
api = PushshiftAPI()
subreddit = reddit.subreddit("xx")
flairsub = reddit.subreddit("xx")

# for submission in subreddit.stream.submissions():
#     if "Thank You" == submission.link_flair_text:
#         print(submission.id)
#         body = submission.selftext.lower()
#         print(body)
#         z = re.findall("\[(u\/[\w-]+)\]", body, re.MULTILINE)
#         print(z)
#         comments = submission.comments;
#         com =[]
#         for comment in comments:
#             matches = re.findall("(u\/[\w-]+)", comment.body, re.MULTILINE)
#             for match in matches:
#                  com.append(match)
#         com = list(dict.fromkeys(com))
#         print(com)
#         search = com[len(com)-1].split("u/")
#         print(search[1])

for item in subreddit.mod.unmoderated():
    if "Thank You" == item.link_flair_text:
        print(item)

# for submission in reddit.subreddit("raocflair").search("GeneralMessage", sort='relevance',limit=5):
#     print(submission.title)

# search = api.search_submissions(subreddit='raocflair',title = "GeneralMessage", filter=['title', 'id'],limit=1)
# for c in search:
#     api.search_comments()


    # if re.search("Marvin Help", comment.body, re.IGNORECASE):
    #     marvin_reply = "Marvin the Depressed Robot says: " + random.choice(marvin_quotes)
    #     comment.reply(marvin_reply)
    #     print(marvin_reply)


# search = api.search_submissions(subreddit='burlapelements',title = "GeneralMessage", filter=['title', 'id'],limit=1)
# for se in search:
#      id = se.id
#      print(se.id)
#      submission = reddit.submission(id=id)
#      latest_comment = submission.comments[len(submission.comments)-1]
#      print(latest_comment.body)
     # for top_level_comment in submission.comments:
     #     print(top_level_comment.body)