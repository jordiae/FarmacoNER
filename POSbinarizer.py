from sklearn import preprocessing

class POSBinarizer():
	def __init__(self,tags=['A','R','T','D','N','V','P','C','S','M','I','F','U'] ):
		self.tags = tags
		self.lb = preprocessing.LabelBinarizer()
		self.lb.fit(self.tags)
	def get_encoding(self,pos):
		return self.lb.transform([pos[0]])
	def get_index(self,pos):
		encoding = self.lb.transform([pos[0]])
		i = 0
		for e in encoding:
			if e == 1:
				return i
			i += 1