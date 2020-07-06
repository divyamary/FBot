import praw
import re
import requests

reddit = praw.Reddit('GeneralBot')
subreddit = reddit.subreddit("xx")
flairsub = reddit.subreddit("xx")

flairs = {1 : 'brown-envelope',
          10 : 'yellow-envelope',
          20 : 'pink-envelope',
          30 : 'red-envelope',
          50 : 'green-envelope',
          100 : 'blue-envelope',
          200 : 'orange-envelope',
          300 : 'navy-envelope',
          500 : 'black-envelope'}

def getflairfromcomment(comment_ids):
    print("Get flair from comments")
    last_comment_id = comment_ids[-1]
    latest_comment = reddit.comment(last_comment_id)
    z = re.match("^\d+", latest_comment.body)
    last_flair_count = z.group(0)
    new_count = int(last_flair_count) + 1
    return new_count


def getflairfrombody(selftext):
    print("Get flair from body")
    z = re.findall("^\d+", selftext, re.MULTILINE)
    print(z)
    last_flair_count = z[-1]
    new_count = int(last_flair_count) + 1
    return new_count


def set_flair(new_count, user):
    if new_count in flairs.keys():
        flairclass = flairs[new_count]
        subreddit.flair.set(user, "", css_class =flairclass)
        if(new_count in [100,500,1000]):
            #send mod mail
            subreddit.modmail.create("Milestone", "Make a post", "u/GeneralMessage")



for item in subreddit.mod.unmoderated():
    if "Thank You" == item.link_flair_text:
        author = item.author.name
        permalink = item.permalink
        #Get all comments
        for comment in item.comments:
            #Look for usernames in comments
            usernames = set(re.findall("(u\/[\w-]+)", comment.body, re.MULTILINE))
            for username in usernames:
                #Split u/
                search_title = username.split("u/")[1]
                print("Username:"+search_title)
                isNew = True
                # Check for this in flairsub
                for submission in flairsub.search(search_title, sort="new"):
                    # If username present in title
                    if (search_title in submission.title):
                        isNew = False
                        isArchived = submission.archived
                        print("Is Archived?" + str(isArchived))
                        #If not archived
                        if (not isArchived):
                            response = requests.get("https://api.pushshift.io/reddit/submission/comment_ids/"+submission.id)
                            json = response.json()
                            comment_ids = json['data']
                            print(comment_ids)
                            if (comment_ids):
                                # Get latest flair
                                new_count = getflairfromcomment(comment_ids)
                                reply = str(new_count) + ") " + "[" + author + "]" + "(https://www.reddit.com" + permalink + ")"
                                print("Reply:"+reply)
                                # Post new flair comment
                                submission.reply(reply)
                                # item.mod.approve()
                                # Flair them
                                set_flair(new_count, search_title)
                            else:
                                # Let's check body
                                new_count = getflairfrombody(submission.selftext)
                                reply = str(new_count) + ") " + "[" + author + "]" + "(https://www.reddit.com" + permalink + ")"
                                print("Reply:"+reply)
                                # Post new flair comment
                                submission.reply(reply)
                                # item.mod.approve()
                                # Flair them
                                set_flair(new_count, search_title)
                        else:
                            # Archived so we make a new Part
                            # part inconsistencies - Uppercase P, Lowercase p, latest post has no Part in title
                            # catch em all
                            if ("Part" in submission.title):
                                # Get number after Part
                                part_no = submission.title.partition("Part")[-1]
                                print(part_no)
                                # older posts have different sort order? :/
                                # reddit api needs more loops to get comment ids so we use pushshift instead
                                # some comments are child comments
                                response = requests.get(
                                    "https://api.pushshift.io/reddit/submission/comment_ids/" + submission.id)
                                json = response.json()
                                comment_ids = json['data']
                                print(comment_ids)
                                if (comment_ids):
                                    new_count = getflairfromcomment(comment_ids)
                                    reply = str(
                                        new_count) + ") " + "[" + author + "]" + "(https://www.reddit.com" + permalink + ")"
                                    print("Reply"+reply)
                                    # Post new flair part
                                    new_title = search_title + "Part "+ str(part_no+1)
                                    archive_here = "[Archive Here]"+"(https://www.reddit.com" + permalink + ")"
                                    flairsub.submit(new_title, selftext=archive_here +"\n"+reply, send_replies=False)
                                    # item.mod.approve()
                                    # Flair them
                                    set_flair(new_count, search_title)
                                else:
                                    # no comments, let's look for count in body
                                    new_count = getflairfrombody(submission.selftext)
                                    reply = str(
                                        new_count) + ") " + "[" + author + "]" + "(https://www.reddit.com" + permalink + ")"
                                    print(reply)
                                    # Post new flair part
                                    new_title = search_title + "Part " + str(part_no + 1)
                                    archive_here = "[Archive Here]" + "(https://www.reddit.com" + permalink + ")"
                                    flairsub.submit(new_title, selftext=archive_here + "\n" + reply, send_replies=False)
                                    # item.mod.approve()
                                    # Flair them
                                    set_flair(new_count, search_title)

                    break
                if (isNew):
                    # Create new Post
                    print("is new")
                    reply = "1.) " + "[" + author + "]" + "(https://www.reddit.com" + permalink + ")"
                    reddit.subreddit("thisisveryrandom").submit(search_title, selftext=reply, send_replies=False)
                    # flair them
                    set_flair(1, search_title)
                    # item.mod.approve()






