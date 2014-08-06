"""
Twitter Most Followed
Top most followed by @someones followers.

E.g.: HNers' Most Followed.
https://twitter.com/ducu/lists/hners-most-followed
Top most followed by @newsyc20 followers.

"""

import twitter as t
from twitter import TweepError

user_data = lambda u: dict([(k, getattr(u, k)) for k in \
	['screen_name', 'name', 'description', 'friends_count', 'followers_count']])

def main():
	pass

if __name__ == '__main__':
	main()
