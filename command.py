import praw
import re
import requests

reddit = praw.Reddit('GeneralBot')
subreddit = reddit.subreddit("")
flairsub = reddit.subreddit("")

flairs = {1 : 'brown-envelope',
          10 : 'yellow-envelope',
          20 : 'pink-envelope',
          30 : 'red-envelope',
          50 : 'green-envelope',
          100 : 'blue-envelope',
          200 : 'orange-envelope',
          300 : 'grey-envelope',
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


def make_new_part(submission, reply, search_title):
    if ("Part" in submission.title):
        # Get number after Part
        part_no = submission.title.partition("Part")[-1]
        print(part_no)
        new_title = search_title + " Part " + str(part_no + 1)
        archive_here = "[Archive Here]" + "(https://www.reddit.com" + submission.permalink + ")\n\n"
        flairsub.submit(new_title, selftext=archive_here + reply, send_replies=False)
    else:
        #Add part 2 to title
        new_title = search_title + " Part 2"
        archive_here = "[Archive Here]" + "(https://www.reddit.com" + submission.permalink + ")\n\n"
        flairsub.submit(new_title, selftext=archive_here + reply, send_replies=False)


def start_flair(submission, comm):
    if submission.author is not None:
        author = submission.author.name
        permalink = submission.permalink
        if "Thank You" == submission.link_flair_text and author != "[deleted]":
            # Get all comments
            for comment in submission.comments:
                # Look for usernames in comments
                usernames = set(re.findall("(u\/[\w-]+)", comment.body, re.MULTILINE))
                for username in usernames:
                    # Split u/
                    search_title = username.split("u/")[1]
                    print("Username:" + search_title)
                    isNew = True
                    # Check for this in flairsub
                    for submission in flairsub.search(search_title, sort="new"):
                        # If username present in title
                        if (search_title in submission.title):
                            isNew = False
                            comm.save()
                            isArchived = submission.archived
                            print("Is Archived?" + str(isArchived))
                            # Older posts have different sort order? :/
                            # Reddit API needs more loops to get comment ids so we use Pushshift instead
                            response = requests.get(
                                "https://api.pushshift.io/reddit/submission/comment_ids/" + submission.id)
                            json = response.json()
                            comment_ids = json['data']
                            print(comment_ids)
                            if (comment_ids):
                                # Get latest flair
                                new_count = getflairfromcomment(comment_ids)
                                reply = str(
                                    new_count) + ") " + "[" + author + "]" + "(https://www.reddit.com" + permalink + ")"
                                print("Reply:" + reply)
                                # Post new flair comment
                                if (not isArchived):
                                    submission.reply(reply)
                                else:
                                    make_new_part(submission, reply, search_title)
                                # item.mod.approve()
                                # Flair them
                                set_flair(new_count, search_title)
                            else:
                                # Let's check body
                                new_count = getflairfrombody(submission.selftext)
                                reply = str(
                                    new_count) + ") " + "[" + author + "]" + "(https://www.reddit.com" + permalink + ")"
                                print("Reply:" + reply)
                                # Post new flair comment
                                if (not isArchived):
                                    submission.reply(reply)
                                else:
                                    make_new_part(submission, reply, search_title)
                                # item.mod.approve()
                                # Flair them
                                set_flair(new_count, search_title)
                        break
                    if (isNew):
                        # Create new Post for new user
                        print("is new")
                        reply = "1.) " + "[" + author + "]" + "(https://www.reddit.com" + permalink + ")"
                        flairsub.submit(search_title, selftext=reply, send_replies=False)
                        # flair them
                        set_flair(1, search_title)
                        comm.save()
                        # item.mod.approve()



for comment in subreddit.stream.comments():
    if re.search("Flair!", comment.body, re.IGNORECASE):
        submission = comment.submission
        saved_items = list(reddit.user.me().saved())
        if comment.id not in saved_items:
            print(comment.id)
            start_flair(submission, comment)














