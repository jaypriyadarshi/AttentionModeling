import numpy as np

class Model(object):
    def __init__(self, hidden_size, ip_dim, num_classes, num_regions, seq_length):
        # model parameters
        self.hidden_size = hidden_size
        self.ip_dim = ip_dim
        self.num_classes = num_classes
        self.num_regions = num_regions #number of regions after segmenting the saliency map
        self.seq_length = seq_length
        self.Wxh = np.random.randn(hidden_size, ip_dim)*0.01 # input to hidden
        self.Whh1 = np.random.randn(hidden_size, hidden_size)*0.01 # hidden to hidden
        self.Whh2 = np.random.randn(hidden_size, hidden_size)*0.01 # hidden to hidden - 2nd RNN layer
        self.Wh1h2 = np.random.randn(hidden_size, hidden_size)*0.01 # hidden to hidden - b/w 1st and 2nd RNN layer
        self.Why1 = np.random.randn(num_classes, hidden_size)*0.01 # hidden to output1 - ALS, PARK, CTRL, etc. participant label
        self.Why2 = np.random.randn(num_regions, hidden_size)*0.01 # hidden to output2 - location
        self.bh1 = np.zeros((hidden_size, 1)) # hidden1 bias
        self.bh2 = np.zeros((hidden_size, 1)) # hidden2 bias
        self.by1 = np.zeros((num_classes, 1)) # output1 bias
        self.by2 = np.zeros((num_regions, 1)) # output2 bias
        self.smooth_loss = -np.log(1.0/self.num_classes)*seq_length + -np.log(1.0/self.num_regions)*seq_length # loss at iteration 0

    def forward_pass(self, inputs, grp_targets, loc_targets, hprev1, hprev2):
        xs, hs1, hs2, ys1, ys2, ps1, ps2 = {}, {}, {}, {}, {}, {}, {}
        hs1[-1] = np.copy(hprev1)
        hs2[-1] = np.copy(hprev2) 
        loss = 0
        for t in xrange(len(inputs)):
            xs[t] = np.zeros((vocab_size,1)) # encode in 1-of-k representation
            xs[t][inputs[t]] = 1
            hs1[t] = np.tanh(np.dot(self.Wxh, xs[t]) + np.dot(self.Whh1, hs1[t-1]) + self.bh1) # hidden state 1
            ys1[t] = np.dot(self.Why1, hs1[t]) + self.by1 # unnormalized log probabilities for participant group
            ps1[t] = np.exp(ys1[t]) / np.sum(np.exp(ys1[t])) # probabilities for participant group
            hs2[t] = np.tanh(np.dot(self.Wh1h2, hs1[t]) + np.dot(self.Whh2, hs2[t-1]) + self.bh2) # hidden state 2
            ys2[t] = np.dot(self.Why2, hs2[t]) + self.by2 # unnormalized log probabilities for next location
            ps2[t] = np.exp(ys2[t]) / np.sum(np.exp(ys2[t])) # probabilities for next location
            loss += -np.log(ps1[t][grp_targets[t],0]) + -np.log(ps2[t][loc_targets[t],0]) #1st and 2nd softmax (cross-entropy loss)
        return loss, xs, hs1, hs2, ps1, ps2


    def backward_pass(self, inputs, grp_targets, loc_targets, xs, hs1, hs2, ps1, ps2):
        dWxh, dWhh1, dWhh2, dWh1h2, dWhy1, dWhy2 = np.zeros_like(self.Wxh), np.zeros_like(self.Whh1), np.zeros_like(self.Whh2), np.zeros_like(self.Wh1h2), np.zeros_like(self.Why1), np.zeros_like(self.Why2)
        dbh1, dbh2, dby1, dby2 = np.zeros_like(self.bh1), np.zeros_like(self.bh2), np.zeros_like(self.by1), np.zeros_like(self.by2)
        dh1next = np.zeros_like(hs1[0])
        dh2next = np.zeros_like(hs2[0])
        for t in reversed(xrange(len(inputs))):
            dy2 = np.copy(ps2[t])
            dy2[loc_targets[t]] -= 1 # backprop into y2
            dWhy2 += np.dot(dy2, hs2[t].T)
            dby2 += dy2
            dh2 = np.dot(self.Why2.T, dy2) + dh2next # backprop into h2
            dhraw2 = (1 - hs2[t] * hs2[t]) * dh2 # backprop through tanh nonlinearity
            dbh2 += dhraw2
            dWh1h2 += np.dot(dhraw2, hs1[t].T)
            dWhh2 += np.dot(dhraw2, hs2[t-1].T)
            dh1 = np.dot(dhraw2, self.Wh1h2.T) #review
            dh2next = np.dot(self.Whh2.T, dhraw2)
            #backprop through layer-1 
            dy1 = np.copy(ps1[t])
            dy1[grp_targets[t]] -= 1 # backprop into y1
            dWhy1 += np.dot(dy1, hs1[t].T)
            dby1 += dy1
            dh1 += np.dot(self.Why1.T, dy1) + dh1next # backprop into h1
            dhraw1 = (1 - hs1[t] * hs1[t]) * dh1 # backprop through tanh nonlinearity
            dbh1 += dhraw1
            dWxh += np.dot(dhraw1, xs[t].T)
            dWhh1 = np.dot(dhraw1, hs1[t-1].T)
            dh1next = np.dot(Whh1.T, dhraw1) 
        return dWxh, dWhh1, dWhh2, dWh1h2, dWhy1, dWhy2, dbh1, dbh2, dby1, dby2

    def _loss(self, inputs, grp_targets, loc_targets, hprev1, hprev2):
        """
        inputs,targets are both list of integers.
        hprev is Hx1 array of initial hidden state
        returns the loss, gradients on model parameters, and last hidden state
        """
        # forward pass
        loss, xs, hs1, hs2, ps1, ps2 = self.forward_pass(inputs, grp_targets, loc_targets, hprev1, hprev2)
        # backward pass: compute gradients going backwards
        dWxh, dWhh1, dWhh2, dWh1h2, dWhy1, dWhy2, dbh1, dbh2, dby1, dby2 = self.backward_pass(inputs, grp_targets, loc_targets, xs, hs1, hs2, ps1, ps2)
        for dparam in [dWxh, dWhh1, dWhh2, dWh1h2, dWhy1, dWhy2, dbh1, dbh2, dby1, dby2]:
            np.clip(dparam, -5, 5, out=dparam) # clip to mitigate exploding gradients
        return loss, dWxh, dWhh1, dWhh2, dWh1h2, dWhy1, dWhy2, dbh1, dbh2, dby1, dby2, hs1[len(grp_inputs)-1], hs2[len(loc_inputs)-1]

    def _sample(self, h, seed_ix, n):
        """ 
        sample a sequence of integers from the model 
        h is memory state, seed_ix is seed letter for first time step
        """
        x = np.zeros((vocab_size, 1))
        x[seed_ix] = 1
        ixes = []
        for t in xrange(n):
            h = np.tanh(np.dot(self.Wxh, x) + np.dot(self.Whh, h) + self.bh)
            y = np.dot(self.Why, h) + self.by
            p = np.exp(y) / np.sum(np.exp(y))
            ix = np.random.choice(range(vocab_size), p=p.ravel())
            x = np.zeros((vocab_size, 1))
            x[ix] = 1
            ixes.append(ix)
        return ixes