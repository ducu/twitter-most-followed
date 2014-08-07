
def set_user_data(user_id, **user_data):
	print "\nSet user data: %s\n%s" % (user_id, user_data)

def set_friends(user_id, *friends):
	print "\nSet user friends: %s\n%s" % (user_id, friends)

def set_followers(user_id, *followers):
	print "\nSet user followers: %s\n%s" % (user_id, followers)
