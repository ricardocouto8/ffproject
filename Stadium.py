class Stadium(object):

	def __str__(self):
		return str(self.name) + '\n' + 'Cap: ' + str(self.cap)
		
	def __init__(self, name = None, cap = None):
		self.name = name
		self.cap = cap