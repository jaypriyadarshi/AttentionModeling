class optimizer(object):
	def __init__(self, learning_rate, model):
		self.learning_rate = learning_rate 
		#memory_vars
		self.mWxh = np.zeros_like(model.Wxh)
		self.mWhh = np.zeros_like(model.Whh)
		self.mWhy = np.zeros_like(model.Why)
		self.mbh = np.zeros_like(model.bh)
		self.mby = np.zeros_like(model.by)

	def _sgd(self, params, grads):
		for param, dparam in zip(params, grads):
			param -= self.learning_rate * dparam
		return params

	def _adagrad(self, params, grads):
		mem_vars = [self.mWxh, self.mWhh, self.mWhy, self.mbh, self.mby]
		for param, dparam, mem in zip(params, grads, mem_vars):
			mem += dparam * dparam
			param += -self.learning_rate * dparam / np.sqrt(mem + 1e-8) # adagrad update
		return params
