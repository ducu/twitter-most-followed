=====================
Twitter Most Followed
=====================

Rationale
---------

`How to Find Out Who's Popular on Twitter <https://medium.com/@ducu/d659884fd942>`

>That’s easy. You just look at the number of followers, and you’ll get @katyperry, @justinbieber, and @BarackObama — the top most followed accounts in the whole Twitterverse. No surprise there, right?

>But what if you want to focus on a particular group of Twitter users, for example the Hacker News community? Who’s in the top most followed accounts by the HNers? This is not a trivial exercise, we need a different approach, but if you’re a HNer, the result will be just as predictable.


Test Case
---------

HNers' Most Followed. 
Top most followed by @newsyc20 followers.


Requirements
------------

Tweepy fork, Redis etc.


Routine
-------

0. Select target user and load user's data

	```python
	screen_name = 'newsyc20' # target user
	user_id, user_data = load_user_data(screen_name=screen_name)
	```

1. Load target user's followers

	```python
	followers = load_followers(user_id)
	```

2. Load user's followers' friends

	```python
	for follower_id in followers:
		load_friends(user_id=follower_id)
	```

3. Aggregate friends into top most followed and display

	```python
	s.set_most_followed() # perform aggregation
	top_most_followed(100) # display results
	```

Results
-------




