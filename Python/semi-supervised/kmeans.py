import numpy as np
import scipy.io
#import matplotlib.pyplot as plt
import vars

def _read_data():
	features = scipy.io.loadmat(vars.feat_loc)
	features = features['all_feats'][:570] #while generating feats, incorrectly generated feats for non-existant participants 571-580 that is just NAN values, filter those out
	labels = scipy.io.loadmat(vars.labels_loc)
	labels = labels['labels']
	known_features = []
	known_labels = []
	unknown_features = []
	unknown_labels = []
	means = []

	for group in vars.groups:
		idx = np.where(labels == group)[0]
		group_features = features[np.random.permutation(idx)]
		group_known_instances = int(vars.known_pct * group_features.shape[0])
		known_features.append(group_features[:group_known_instances])
		unknown_features.append(group_features[group_known_instances:])
		known_labels.append(labels[labels == group][:group_known_instances])
		unknown_labels.append(labels[labels == group][group_known_instances:])
		#known_labels.append(np.ones(known_features.shape[0]).astype('int') * group)
		#unknown_labels.append(np.ones(known_features.shape[0]).astype('int') * group)
		means.append(np.mean(group_features, axis=0))
	return np.vstack(known_features), np.concatenate(known_labels), np.vstack(unknown_features), np.concatenate(unknown_labels), np.vstack(means)

def _compute_l2_dist(features, means):
	#sqrt((x-y)**2) = sqrt(x**2 + y**2 - 2x*y)
	sq_sum_means = np.sum(np.square(means), axis=1)
	sq_sum_features = np.sum(np.square(features), axis=1)
	inner_product = np.dot(features, means.T)
	return np.sqrt(sq_sum_means - 2 * inner_product + sq_sum_features.reshape(-1,1))

def _assign_label(features, means):
	scores = _compute_l2_dist(features, means)
	predicted_labels = np.argsort(scores)[:,0] + 1 #because the groups are 1 indexed in the data, add 1 to all predicted groups: 0 -> 1, 1 -> 2
	return predicted_labels

def _calc_means(known_features, unknown_features, known_labels, predicted_labels):
	means = []
	for group in vars.groups:
		means.append(np.mean(np.vstack((known_features[np.where(known_labels == group)[0]], unknown_features[np.where(predicted_labels == group)[0]])), axis=0))
	return np.vstack(means)

def _calc_accuracy(predictions, true_labels):
	#print predictions
	#print true_labels
	return float(np.sum(predictions == true_labels)) / true_labels.shape[0]

def _run_kmeans(known_features, unknown_features, known_labels, means):
	itr = 1
	while True:
		#print 'Iteration: {0}'.format(itr)
		predicted_labels = _assign_label(unknown_features, means)
		updated_means = _calc_means(known_features, unknown_features, known_labels, predicted_labels)
		if np.array_equal(updated_means, means):
			return predicted_labels
		means = updated_means
		itr += 1

def _run_task():
	accuracies = []
	for _ in range(vars.kmeans_runs):
		known_features, known_labels, unknown_features, unknown_labels, means = _read_data()
		predicted_labels = _run_kmeans(known_features, unknown_features, known_labels, means)
		accuracy = _calc_accuracy(predicted_labels, unknown_labels)
		print 'Accuracy: {0}'.format(accuracy)
		accuracies.append(accuracy)
	accuracies = np.array(accuracies)
	print 'Mean Accuracy: {0}, std: {1}, Max: {2}, Min: {3}'.format(np.mean(accuracies), np.std(accuracies), np.max(accuracies), np.min(accuracies))

def main():
	_run_task()

if __name__ == '__main__':
	main()
	





