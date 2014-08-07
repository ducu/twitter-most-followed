
class Storage(object):

	def set_user_data(self, user_id, user_data):
		print "\nSet user data: %s" % user_id
		print user_data

	def mark_protected(self, user_id):
		print "\nProtected user: %s" % user_id

	def set_friends(self, user_id, friends):
		print "\nSet user friends: %s" % user_id
		print friends[:10], "... out of %s." % len(friends)

	def exists(self, user_id):
		return False

	def set_followers(self, user_id, followers):
		print "\nSet user followers: %s" % user_id
		print followers[:10], "... out of %s." % len(followers)


class MemoryStorage(Storage):
	pass


class RedisStorage(Storage):
	
	import redis
	r = redis.StrictRedis()

	def set_user_data(self, user_id, user_data):
		self.r.hmset('user_data:%s' % user_id, user_data)

	def mark_protected(self, user_id):
		self.r.sadd('system_protected', user_id)
		print "Protected user: %s" % user_id

	def set_friends(self, user_id, friends):
		self.r.sadd('user_friends:%s' % user_id, *friends)
		print "Set user friends: %s\t%s" % (user_id, len(friends))

	def exists(self, user_id):
		return 
			self.r.exists('user_friends:%s' % user_id) or \
			self.r.ismember('system_protected', user_id)

	def set_followers(self, user_id, followers):
		self.r.sadd('user_followers:%s' % user_id, *followers)
