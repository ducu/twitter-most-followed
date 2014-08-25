=====================
Twitter Most Followed
=====================

Rationale
---------

**How to Find Out Who's Popular on Twitter.** And why there's no point in doing it

> That’s easy. You just look at the number of followers, and you’ll get @katyperry, @justinbieber, and @BarackObama — the top most followed accounts in the whole Twitterverse. No surprise there, right?

> But what if you want to focus on a particular group of Twitter users, for example the Hacker News community? Who’s in the top most followed accounts by the HNers? This is not a trivial exercise, we need a different approach, but if you’re a HNer, the result will be just as predictable.

Read the whole story here: https://medium.com/@ducu/d659884fd942


Approach
--------

Let's take the Hacker News community as our target group.

There is a Twitter account named [@newsyc20](http://twitter.com/newsyc20/) (Hacker News 20 - "Tweeting Hacker News stories as soon as they reach 20 points."). We consider this as our target user, so the followers of @newsyc20 will be our target group. They are about 13.3K members. To find out their top most followed accounts, we fetch the complete lists of who each of them is following (aka friends), and we aggregate all those lists, counting the occurences of each friend.

You can realize that the most followed account will be exactly @newsyc20, obviously, because all the members are following it. But who's on the 2nd and 3rd place? Who's in the top 100 most followed? This is what we're going to find out by running the routine below, a transcript from [main.py](https://github.com/ducu/twitter-most-followed/blob/master/main.py)


``` python
# Step 1: Select target user and load user's data
screen_name = 'newsyc20' # target user
user_id, user_data = load_user_data(screen_name=screen_name)

# Step 2: Load target user's followers
followers = load_followers(user_id) # target group
	
# Step 3: Load friends of target group members
for follower_id in followers:
	load_friends(user_id=follower_id)

# Step 4: Aggregate friends into top most followed and display
aggregate_friends() # count friend occurences
top_most_followed(100) # display results
```


Requirements
------------

Tweepy fork, Redis etc.


Results
-------



