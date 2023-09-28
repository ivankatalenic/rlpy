class Brace:
	open: str
	close: str

	def __init__(self, open: str, close: str):
		if len(open) != 1:
			raise ValueError("the open brace symbol must have len equal to one")
		if len(close) != 1:
			raise ValueError("the close brace symbol must have len equal to one")
		self.open = open
		self.close = close
