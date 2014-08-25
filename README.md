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

There's a Twitter account named [@newsyc20](http://twitter.com/newsyc20/) (Hacker News 20 - "Tweeting Hacker News stories as soon as they reach 20 points."). We consider this as our **source**, and the followers of @newsyc20 as the HNers, our **target group**. To find out the top most followed accounts by our target group members, we get the complete lists of who each of them is following (aka friends), and we aggregate all these lists, counting the occurences of each friend.

You can realize that the most followed account will be exactly @newsyc20, because all the members are following it. But who's on the 2nd and 3rd place? Who's in the top 100 most followed? This is what we're going to find out by running the routine below, a transcript from [main.py](https://github.com/ducu/twitter-most-followed/blob/master/main.py)


``` python
# Step 1: Specify the source
source_name = 'newsyc20' # target group source
source_id, source_data = load_user_data(screen_name=source_name)

# Step 2: Load target group members
followers = load_followers(source_id) # target group

# Step 3: Load friends of target group members
for follower_id in followers:
	load_friends(user_id=follower_id)

# Step 4: Aggregate friends into top most followed
aggregate_friends() # count friend occurences
top_most_followed(100) # display results
```


Requirements
------------

The Python script in this repo uses [Twitter REST API](https://dev.twitter.com/docs/api/1.1) to get the data, and [Redis](http://redis.io/) to store and aggregate it. To use Twitter API you need [an existing application](https://apps.twitter.com/), and [some access tokens](https://dev.twitter.com/docs/auth/obtaining-access-tokens).

There are a couple of performance issues though when dealing with big data sets.

**Twitter API Rate Limits**

We have 13.3K members in our HNers target group. In order to load the friends for each of these members (step 3), we're calling the Twitter API [friends/ids](https://dev.twitter.com/docs/api/1.1/get/friends/ids) method. This method is rate limited at 15 calls/15 minutes/token. We have to perform about 15.3K calls, since one call returns at most 5000 items. The problem is that with a single access token, it would take 10 days and 16 hours to get all this data.

[Tweepy](https://github.com/tweepy/tweepy/) is the preferred Twitter API client for Python, and the current release works with a single access token. But here's a fork I created especially to extend Tweepy so it works with several access tokens in a round robin fashion transparently: https://github.com/svven/tweepy. Using about four dozen tokens I reduced the overall retrieval time to 5 hours (2 hours work time, 3 hours sleep).

git+https://github.com/svven/tweepy.git#egg=tweepy




Results
-------



