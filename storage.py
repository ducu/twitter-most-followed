
def set_user_data(user_id, user_data):
	print "\nSet user data: %s" % user_id
	print user_data

def mark_protected(user_id):
	print "\nProtected user: %s" % user_id


def set_friends(user_id, friends):
	print "\nSet user friends: %s" % user_id
	print friends[:10], "... out of %s." % len(friends)

def has_friends(user_id):
	return False


def set_followers(user_id, followers):
	print "\nSet user followers: %s" % user_id
	print followers[:10], "... out of %s." % len(followers)