"""
Twitter Most Followed
Top most followed by @someones followers.

E.g.: HNers' Most Followed.
https://twitter.com/ducu/lists/hners-most-followed
Top most followed by @newsyc20 followers.

"""

import twitter as t
from twitter import TweepError

import storage as s

user_data = lambda u: dict([(k, getattr(u, k)) for k in \
	['screen_name', 'name', 'description', 'friends_count', 'followers_count']])

def main():

	# Step 1: Load @someones followers
	source_name = 'newsyc20'
	source = t.get_user(screen_name=source_name)
	source_id = source.id
	# source_id = 148969874
	s.set_user_data(source_id, **user_data(source))

	followers = t.followers_ids(source_id)
	s.set_followers(source_id, *followers)
	# followers = s.get_followers(source_id)


	# Step 2: Load followers' friends


	# Step 3: Aggregate most followed


if __name__ == '__main__':
	main()
