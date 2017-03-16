class optimizer(object):
	def __init__(self, learning_rate, model):
		self.learning_rate = learning_rate 
		#memory_vars
		self.mWxh = np.zeros_like(model.Wxh)
		self.mWhh1 = np.zeros_like(model.Whh1)
		self.mWhh2 = np.zeros_like(model.Whh2)
		self.mWh1h2 = np.zeros_like(model.Wh1h2)
		self.mWhy1 = np.zeros_like(model.Why1)
		self.mWhy2 = np.zeros_like(model.Why2)
		self.mbh1 = np.zeros_like(model.bh1)
		self.mbh2 = np.zeros_like(model.bh2)
		self.mby1 = np.zeros_like(model.by1)
		self.mby2 = np.zeros_like(model.by2)

	def _sgd(self, params, grads):
		for param, dparam in zip(params, grads):
			param -= self.learning_rate * dparam
		return params

	def _adagrad(self, params, grads):
		mem_vars = [self.mWxh, self.mWhh1, self.mWhh2, self.mWh1h2, self.mWhy1, self.mWhy2, self.mbh1, self.mbh2, self.mby1, self.mby2]
		for param, dparam, mem in zip(params, grads, mem_vars):
			mem += dparam * dparam
			param += -self.learning_rate * dparam / np.sqrt(mem + 1e-8) # adagrad update
		return params
