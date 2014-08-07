"""
Twitter Most Followed
Top most followed by @someones followers.

E.g.: HNers' Most Followed.
https://twitter.com/ducu/lists/hners-most-followed
Top most followed by @newsyc20 followers.

"""

import twitter as t
from twitter import TweepError

import storage
s = storage.RedisStorage()

from datetime import datetime

user_data = lambda u: dict([(k, getattr(u, k)) for k in \
	['screen_name', 'name', 'description', 'friends_count', 'followers_count']])

def main():

	# Step 1: Load @someones followers
	print "Step 1: %s" % datetime.now()
	source_name = 'newsyc20'
	source = t.get_user(screen_name=source_name)
	source_id = source.id
	# source_id = 148969874
	s.set_user_data(source_id, user_data(source))

	followers = sorted(list(t.followers_ids(source_id)))
	s.set_followers(source_id, followers)
	# followers = s.get_followers(source_id)


	# Step 2: Load followers' friends
	print "Step 2: %s" % datetime.now()
	for follower_id in followers:
		if s.exists(follower_id):
			continue
		try:
			friends = sorted(list(t.friends_ids(follower_id)))
			s.set_friends(follower_id, friends)
		except TweepError, e:
			s.mark_protected(follower_id)


	# Step 3: Aggregate most followed
	print "Step 3: %s" % datetime.now()


if __name__ == '__main__':
	main()
