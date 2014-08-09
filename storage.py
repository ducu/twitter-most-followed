"""
Data storage classes for Twitter Most Followed.
It should also perform aggregation for "most followed".
"""

class Storage(object):
	"Base storage class doin nothin."

	# Basic user functions
	def set_user_data(self, user_id, user_data):
		"Store user_data dictionary."
		print "Set user data:\t%s\n%s" % (user_id, user_data)

	# def get_user_data(self, user_id):
	# 	"Return user_id's data."
	# 	return None

	def is_protected(self, user_id):
		return False

	def mark_protected(self, user_id):
		print "Mark protected:\t%s" % user_id

	# Followers
	def set_followers(self, user_id, followers):
		"Store user_id's followers list."
		print "Set followers:\t%s\t%s" % (user_id, len(followers))

	def get_followers(self, user_id):
		"Return user_id's followers list."
		return None

	# Friends (aka following, or better yet leaders)
	def has_friends(self, user_id):
		"Return whether user_id's friends are stored."
		return False

	def set_friends(self, user_id, friends):
		"Store user_id's friends list."
		print "Set friends:\t%s\t%s" % (user_id, len(friends))

	def get_friends(self, user_id):
		"Return user_id's friends list."
		return None


class RedisStorage(Storage):
	"Redis storage "
	
	import redis
	r = redis.StrictRedis(db=1)

	def set_user_data(self, user_id, user_data):
		self.r.hmset('user_data:%s' % user_id, user_data)
		super(RedisStorage, self).set_user_data(user_id, user_data)

	def is_protected(self, user_id):
		return self.r.sismember('system_protected', user_id)

	def mark_protected(self, user_id):
		self.r.sadd('system_protected', user_id)
		super(RedisStorage, self).mark_protected(user_id)

	# Followers
	def set_followers(self, user_id, followers):
		"Store user_id's followers list."
		self.r.sadd('user_followers:%s' % user_id, *followers)
		super(RedisStorage, self).set_followers(user_id, followers)

	def get_followers(self, user_id):
		"Return user_id's followers list."
		return self.r.smembers('user_followers:%s' % user_id)

	# Friends (aka following, or better yet leaders)
	def has_friends(self, user_id):
		"Return whether user_id's friends are stored."
		return self.r.exists('user_friends:%s' % user_id)

	def set_friends(self, user_id, friends):
		"Store user_id's friends list."
		self.r.sadd('user_friends:%s' % user_id, *friends)
		super(RedisStorage, self).set_friends(user_id, friends)

	def get_friends(self, user_id):
		"Return user_id's friends list."
		return self.r.smembers('user_friends:%s' % user_id)


class FileStorage(Storage):
	pass

