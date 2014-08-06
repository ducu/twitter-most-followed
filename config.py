import os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY', '')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', '')

ACCESS_TOKENS = (
	# No need to store these in environ vars, just put them here
	(os.environ.get('ACCESS_KEY1', ''), os.environ.get('ACCESS_SECRET1', '')),
	(os.environ.get('ACCESS_KEY2', ''), os.environ.get('ACCESS_SECRET2', '')),
	# ...
)