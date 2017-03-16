import numpy as np
import cPickle as pickle
from optimizer import Optimizer

class Solver(object):
	def __init__(self, model, data, num_iter, learning_rate, update_rule):
		self.model = model
		self.num_iter = num_iter
		self.optimizer = Optimizer(learning_rate, self.model)
		self.data = data
		self.start_id = 0 # start_id is for maintaing the window (start_id + seq_length) for one step of graident descent (or any other optimizer)
		self.hprev1 = np.zeros((self.model.hidden_size, 1)) #RNN l-1 memory
		self.hprev2 = np.zeros((self.model.hidden_size, 1)) #RNN l-2 memory
		self.curr_iter = 0
		self.update_rule = getattr(self.optimizer, '_' + self.optimizer.update_rule)

	def _reset(self):
		self.hprev1 = np.zeros((self.model.hidden_size, 1)) # reset RNN memory
		self.hprev2 = np.zeros((self.model.hidden_size, 1))
		self.start_id = 0

	def _step(self):
		if self.start_id + self.model.seq_length + 1 >= len(self.data):
			self._reset()
		loss, dWxh, dWhh1, dWhh2, dWh1h2, dWhy1, dWhy2, dbh1, dbh2, dby1, dby2, hprev1, hprev2 = self.model._loss(inputs, grp_targets, loc_targets, self.hprev1, self.hprev2)
		self.model.smooth_loss = self.model.smooth_loss * 0.999 + loss * 0.001
		if self.curr_iter % 100 == 0:
			print 'iter %d, loss: %f' % (self.curr_iter, smooth_loss) # print progress
		params = [self.model.Wxh, self.model.Whh1, self.model.Whh2, self.model.Wh1h2, self.model.Why1, self.model.Why2, self.model.bh1, self.model.bh2, self.model.by1, self.model.by2]
		grads = [dWxh, dWhh1, dWhh2, dWh1h2, dWhy1, dWhy2, dbh1, dbh2, dby1, dby2]
		self.model.Wxh, self.model.Whh1, self.model.Whh2, self.model.Wh1h2, self.model.Why1, self.model.Why2, self.model.bh1, self.model.bh2, self.model.by1, self.model.by2 = self.update_rule(params, grads)
		self.start_id += self.model.seq_length
		self.curr_iter += 1

	def _train(self):
		for t in xrange(self.num_iter):
			self._step()

	def _save_model(self):
		pickle.dump(self.model, open(model_SaveFile, 'wb'))


