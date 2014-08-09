"""
Tweepy wrapper using RateLimitHandler with multiple access tokens,
based on this fork https://github.com/svven/tweepy.
It also handles API method cursors and splits input param lists in 
chunks if neccessary.
"""

from tweepy import API, Cursor
from tweepy import RateLimitHandler
from tweepy.error import TweepError

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKENS

def get_api():
	auth = RateLimitHandler(CONSUMER_KEY, CONSUMER_SECRET)
	for key, secret in ACCESS_TOKENS:
		try:
			auth.add_access_token(key, secret)
		except TweepError, e:
			print e, key
			continue
	print 'Token pool size: %d' % len(auth.tokens)
	api = API(auth, 
		wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	return api

api = get_api()

# Tweepy API methods
def get_user(**kwargs):
	"""
	https://dev.twitter.com/docs/api/1.1/get/users/show
	http://docs.tweepy.org/en/latest/api.html#API.get_user
	"""
	return api.get_user(**kwargs)

def lookup_users(**kwargs):
	"""
	https://dev.twitter.com/docs/api/1.1/get/users/lookup
	"""
	param = ('user_ids' in kwargs and 'user_ids') or \
			('screen_names' in kwargs and 'screen_names')
	items = ('user_ids' in kwargs and kwargs['user_ids']) or \
			('screen_names' in kwargs and kwargs['screen_names'])
	assert param and items

	def chunks(l, n):
		for i in xrange(0, len(l), n):
			yield l[i:i+n]

	for items_chunk in chunks(items, 100): # 100 ids at a time
		chunk = api.lookup_users(**dict([(param, items_chunk)]))
		for u in chunk: yield u

def friends_ids(user_id):
	"""
	https://dev.twitter.com/docs/api/1.1/get/friends/ids
	http://docs.tweepy.org/en/latest/api.html#API.friends_ids
	"""
	for friends_ids_chunk in Cursor(api.friends_ids, user_id=user_id).pages():
		for f in friends_ids_chunk: yield f

def followers_ids(user_id):
	"""
	https://dev.twitter.com/docs/api/1.1/get/followers/ids
	http://docs.tweepy.org/en/latest/api.html#API.followers_ids
	"""
	for followers_ids_chunk in Cursor(api.followers_ids, user_id=user_id).pages():
		for f in followers_ids_chunk: yield f

