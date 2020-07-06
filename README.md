# FBot

**app.py** flow:

Check posts in unmoderated queue

Check if post flair is Thank You

Get all comments from the post submission

Check if username starts with u/

Search for this username post in flair subreddit

Pushshift here spits out the latest entry.

Get all comments for the latest flair post.

If comments are empty, we look for flair count in body of the post.

If not, we get the latest comment and look for the flair count.

Now we check if the post was archived.

If yes, we make a new part.

If not, we make a new comment.

If we couldn't find a username in the flair sub, we make a new post.

Flair the user

Approve the submission

------------------------------------------------------

**command.py** does everything stated above but it starts like this:

Check new stream of comments in the subreddit for keyword 'Flair!'

Check if this was commented on a Thank You post.

Check if this comment wasn't saved by the bot previously.

If it was saved, then we have already assigned flair.

Get all comments from the post submission

Check if username starts with u/

Search for this username post in flair subreddit

Pushshift here spits out the latest entry.

Get all comments for the latest flair post.

If comments are empty, we look for flair count in body of the post.

If not, we get the latest comment and look for the flair count.

Now we check if the post was archived.

If yes, we make a new part.

If not, we make a new comment.

If we couldn't find a username in the flair sub, we make a new post.

Flair the user

Save the original 'Flair!' comment.

