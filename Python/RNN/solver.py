class Solver(object):
	def __init__(self, model, data, num_iter, learning_rate, update_rule, seq_length):
		self.model = model
		self.num_iter = num_iter
		self.optimizer = Optimizer(learning_rate, self.model)
		self.seq_length = seq_length
		self.data = data
		self.start_id = 0 # start_id is for maintaing the window (start_id + seq_length) for one step of graident descent (or any other optimizer)
		self.hprev = np.zeros((self.model.hidden_size, 1)) #RNN memory
		self.curr_iter = 0
		self.update_rule = getattr(self.optimizer, '_' + self.optimizer.update_rule)

	def _step(self):
		if self.start_id + self.seq_length + 1 >= len(self.data):
			self.hprev = np.zeros((self.model.hidden_size, 1)) # reset RNN memory
			self.start_id = 0

		loss, dWxh, dWhh, dWhy, dbh, dby, hprev = self.model._loss(inputs, targets, self.hprev)
		smooth_loss = smooth_loss * 0.999 + loss * 0.001
		if self.curr_iter % 100 == 0:
			print 'iter %d, loss: %f' % (self.curr_iter, smooth_loss) # print progress
		params = [self.model.Wxh, self.model.Whh, self.model.Why, self.model.bh, self.model.by]
		grads = [dWxh, dWhh, dWhy, dbh, dby]
		self.model.Wxh, self.model.Whh, self.model.Why, self.model.bh, self.model.by = self.update_rule(params, grads)
		self.start_id += self.seq_length
		self.curr_iter += 1

	def _train(self):
		for t in xrange(self.num_iter):
			self._step()

	def _save_model(self):
		pickle.dump(self.model, open(model_SaveFile, 'wb'))


