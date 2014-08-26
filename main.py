"""
Twitter Most Followed

Finding out top most followed accounts by a particular
group of Twitter users such as the Hacker News community.
For this exercise we consider @newsyc20 as our *source*,
and @newsyc20 followers as the HNers, our *target group*.

You can easily run the exercise for a different target
group by specifying the corresponding target group source.
Or you can modify the script so it considers several 
sources to start from, such as @newsyc20, @brainpickings,
and @ThisIsSethsBlog. This should be more interesting.
"""

import twitter as t
from twitter import TweepError

import redis
r = redis.StrictRedis(db=0)

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

def aggregate_friends():
	"Aggregate friends into top most followed."
	s.set_most_followed()

def top_most_followed(n):
	"""
	Display top n most followed.
	"""
	i = 1
	top = s.get_most_followed(n) # withscores
	format = "%d | %d | %s | [@%s](https://twitter.com/%s) | %s | %s"
	print "Rank | Popularity | Name | Twitter | Followers | Friends"
	print "--- | --- | --- | --- | --- | ---"
	for user_id, score in top:
		user_id, user_data = load_user_data(user_id=user_id)
		print format % (i, score, user_data['name'],
			user_data['screen_name'], user_data['screen_name'],
			user_data['followers_count'], user_data['friends_count'])
		i += 1

def main():
	"""
	Starting from a source (e.g. @newsyc20),
	consider the target group as the source's followers, and
	find out top most followed accounts by the target group.
	"""

	# Step 1: Specify the source
	print "\nStep 1: %s" % datetime.now()
	source_name = 'newsyc20' # target group source
	source_id, source_data = load_user_data(screen_name=source_name)

	# Step 2: Load target group members
	print "\nStep 2: %s" % datetime.now()
	followers = load_followers(source_id) # target group
	
	# Step 3: Load friends of target group members
	print "\nStep 3: %s" % datetime.now()
	for follower_id in followers:
		load_friends(user_id=follower_id)

	# Step 4: Aggregate friends into top most followed
	print "\nStep 4: %s" % datetime.now()
	aggregate_friends() # count friend occurences
	print "\nDone: %s" % datetime.now()
	print "\nTop most followed by @%s's followers" % source_name
	top_most_followed(100) # display results


if __name__ == '__main__':
	main()
