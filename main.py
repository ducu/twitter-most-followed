"""
Twitter Most Followed
Top most followed by @screen_name's followers.

E.g.: HNers' Most Followed. 
Top most followed by @newsyc20 followers.

`screen_name = 'newsyc20'`

Resulting top 301 HNers' Most Followed list:
https://twitter.com/ducu/lists/hners-most-followed
"""

import twitter as t
from twitter import TweepError

import redis
r = redis.StrictRedis(db=2)

import storage
s = storage.RedisStorage(r)

from datetime import datetime

select_user_data = lambda u: dict([(k, getattr(u, k)) for k in \
	['screen_name', 'name', 'description', 'friends_count', 'followers_count']])


def load_user_data(user_id=None, screen_name=None):
	"""
	Retrieve and set user's data.
	Or get it from the store if already there.
	"""
	assert bool(user_id) != bool(screen_name)
	if user_id:
		user_data = s.get_user_data(user_id)
		if user_data:
			return user_id, user_data
		user = t.get_user(user_id=user_id)
	else: # screen_name
		user = t.get_user(screen_name=screen_name)
	user_id = user.id
	user_data = select_user_data(user)
	s.set_user_data(user_id, user_data)
	return user_id, user_data

def load_followers(user_id):
	"""
	Retrieve and set user's followers.
	"""
	followers = sorted(list(t.followers_ids(user_id)))
	s.set_followers(user_id, followers)
	# followers = s.get_followers(user_id)
	return followers

def load_friends(user_id):
	"""
	Retrieve and set user's friends.
	"""
	if s.is_protected(user_id) or \
	   s.has_friends(user_id): # loaded before
		return
	try:
		friends = sorted(list(t.friends_ids(user_id)))
		s.set_friends(user_id, friends)
	except TweepError, e:
		if 'Not authorized' in str(e):
			s.mark_protected(user_id)

def top_most_followed(n):
	"""
	Display top n most followed.
	"""
	i = 1
	top = s.get_most_followed(n) # withscores
	for user_id, score in top:
		user_id, user_data = load_user_data(user_id=user_id)
		print "%s (%d). %s (@%s)" % (
			i, score, user_data['name'], user_data['screen_name'])
		i += 1

def main():
	"""
	Pick a target user (e.g. @newsyc20) and
	find out top most followed by target user's followers.
	"""
	screen_name = 'newsyc20' # target user
	# user_id = 148969874 # for @newsyc20

	# Step 0: Load target user's data
	user_id, user_data = load_user_data(screen_name=screen_name)

	# Step 1: Load target user's followers
	print "\nStep 1: %s" % datetime.now()
	followers = load_followers(user_id)
	
	# Step 2: Load user's followers' friends
	print "\nStep 2: %s" % datetime.now()
	for follower_id in followers:
		load_friends(user_id=follower_id)

	# Step 3: Aggregate friends into top most followed
	print "\nStep 3: %s" % datetime.now()
	s.set_most_followed()
	
	print "\nDone: %s" % datetime.now()

	# Display results
	print "\nTop most followed by @%s's followers" % screen_name
	top_most_followed(100)


if __name__ == '__main__':
	main()
