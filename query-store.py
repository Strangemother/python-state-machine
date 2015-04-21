from discodb import DiscoDB, Q

def main():
	ask()

class Talk(object):

	def ask():
		value = raw_input('Something: ')
		self.got(value)

	def got(s):
		if db.get(s) is None:
			self.store()

if __name__ == '__main__':
	main()
