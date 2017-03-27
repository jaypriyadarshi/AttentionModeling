import scipy.io 
import numpy as np
import h5py
import os
import cPickle as pickle
from data_utils import EyeTracker, Trial, Saliency_Map, get_dir_entries, get_trials
from solver import Solver
from model import Model
from optimizer import Optimizer
import vars

class Task(object):
	def _prep_Data(self):
		print "Loading Data"
		data = scipy.io.loadmat(vars.IP_MAT_FileName)
		badTrials = scipy.io.loadmat(vars.BadTrial_FileName)
		self.badTrials = map(lambda trial_num: trial_num[0][0], badTrials['badTrials']['trialNum'][0])
		eye_tracker = EyeTracker(data)
		train_trials = []
		test_trials = []
		for grp in vars.Groups:
			grp_trials = get_trials(data, grp)
			grp_trials_shuff_idx = np.random.permutation(grp_trials.shape[0])
			grp_trials = grp_trials[grp_trials_shuff_idx]
			_ = map(lambda trial_num: train_trials.append(Trial(data, trial_num)), grp_trials[:vars.train_trials_per_category])
			_ = map(lambda trial_num: test_trials.append(Trial(data, trial_num)), grp_trials[vars.train_trials_per_category: vars.train_trials_per_category + vars.test_trials_per_category])
		#_ = map(lambda grp: map(lambda trial_num: trials.append(Trial(data, trial_num)), get_trials(data, grp)), vars.Groups)

		#compute frametimes
		_ = map(lambda trial: trial._compute_frametime(eye_tracker), train_trials)
		_ = map(lambda trial: trial._compute_frametime(eye_tracker), test_trials)
		#preprocess (x,y) data
		_ = map(lambda trial: trial._preprocess(eye_tracker), train_trials)
		_ = map(lambda trial: trial._preprocess(eye_tracker), test_trials)
		#get all saliency maps
		train_trials = np.array(train_trials)
		idx = np.random.permutation(train_trials.shape[0])
		train_trials = train_trials[idx]

		test_trials = np.array(test_trials)
		idx = np.random.permutation(test_trials.shape[0])
		test_trials = test_trials[idx]
		#save train and test data
		pickle.dump(train_trials, open(vars.train_data_file, 'wb'))
		pickle.dump(test_trials, open(vars.test_data_file, 'wb'))
		#trianing_size = int(.80 * trials.shape[0])
		#trianing_trials, test_trials = trials[:trianing_size], trials[trianing_size:]
		self.saliency_obj = Saliency_Map(vars.Saliency_Map_BaseDir, vars.Saliency_Map_Res, vars.Saliency_Map_Receptive_Field, vars.Map_Types)
		self.saliency_maps = map(lambda movie: self.saliency_obj._load_saliency_maps(movie), get_dir_entries(vars.Saliency_Map_BaseDir))
		self.segmented_map = self.saliency_obj._segment_map().astype(int) #get region label for each pixel
		#region in saliency map where (x,y) is located
		#xy_regions_train = map(lambda trial: segmented_map[[trial.y.ravel(), trial.x.ravel()]], trianing_trials)
		#xy_regions_test = map(lambda trial: segmented_map[[trial.y.ravel(), trial.x.ravel()]], test_trials)	
		train_group, train_region, train_avg_saliency_vals, train_saliency_bins, _ = self._get_saliency_feats(train_trials)
		test_group, test_region, test_avg_saliency_vals, test_saliency_bins, trial_end_idx = self._get_saliency_feats(test_trials)
		print "Data Loaded"
		return {'train_group_targets': train_group, 'train_regions': train_region, 'train_avg_saliency_region': train_avg_saliency_vals, 'train_saliency_bin_num': train_saliency_bins, 'test_group_targets': test_group, 'test_regions': test_region, 'test_avg_saliency_region': test_avg_saliency_vals, 'test_saliency_bin_num': test_saliency_bins ,'test_trial_end_idx': trial_end_idx} 

	def _get_saliency_feats(self, trials):
		saliency_bins = [] # stores which bin the saliency val corresponding to (x,y) belongs to
		avg_saliency_vals = [] # avg_saliency over different regions for all trials
		region = []
		group = []
		trial_end_idx = [0]
		for trial_idx in range(len(trials)):
			if trials[trial_idx].trial_num in self.badTrials:
				continue
			#trial_avg_saliency = []
			#trial_saliency_bins = []
			frame_seq = np.digitize(trials[trial_idx].timestamps, trials[trial_idx].frametimes) #will return an array like [1,1,1,2,2,2,...] each entry indicating the framenumber
			for frame_idx in range(len(frame_seq)):
				frame_avg_saliency = []
				frame_saliency_bins = []
				for map_idx in range(len(vars.Map_Types)):
					try:
						saliency_value = self.saliency_maps[trials[trial_idx].movie_num][map_idx][frame_seq[frame_idx]].reshape(self.saliency_obj.height, self.saliency_obj.width)[trials[trial_idx].y[frame_idx], trials[trial_idx].x[frame_idx]][0]
					except:
						continue
					frame_avg_saliency.append(self.saliency_obj._avg_saliency_region(self.saliency_maps[trials[trial_idx].movie_num][map_idx][frame_seq[frame_idx]].reshape(self.saliency_obj.height, self.saliency_obj.width)))
					hist, bin_edges = np.histogram(self.saliency_maps[trials[trial_idx].movie_num][map_idx][frame_seq[frame_idx]], bins=vars.n_bins)
					#print bin_edges, saliency_value
					try:
						bin_num = np.where(bin_edges >  saliency_value)[0][0]
						if bin_num >= vars.n_bins:
							bin_num = vars.n_bins - 1
						frame_saliency_bins.append(bin_num)
					except:
						frame_saliency_bins.append(vars.n_bins - 1)
			
				if len(frame_saliency_bins) == len(vars.Map_Types):
					saliency_bins.append(frame_saliency_bins)
					avg_saliency_vals.append(np.array(frame_avg_saliency).ravel())
					region.append(self.segmented_map[trials[trial_idx].y[frame_idx][0]][trials[trial_idx].x[frame_idx][0]])
					group.append(trials[trial_idx].group - 1)
			trial_end_idx.append(len(group))

			#avg_saliency_vals.append(trial_avg_saliency)
			#saliency_bins.append(trial_saliency_bins)
			#print saliency_bins
		#saliency bins: [[each trial[each frame]]] - each element represents a trial and each trial has a list for each frame, each frame contains the bin number for each saliency map (list)
		#avg_saliency_vals: [[each trial[each frame]]] - each element represents a trial and each trial has a list for each frame's average saliency value over regions,
		#each frame contains another list with each element representing avg of a particular map
		return group, region, avg_saliency_vals, saliency_bins, trial_end_idx


	def _train_rnn(self):
		model = Model(vars.hidden_size, vars.num_classes, vars.num_regions, vars.seq_length)
		self.task_data = self._prep_Data()
		#pickle.dump(data, open(vars.data_SaveFile, 'wb'))
		#data = pickle.load(open(vars.data_SaveFile, 'rb'))
		np.save(open(vars.data_SaveFile, 'wb'), self.task_data)
		self.solver = Solver(model, self.task_data)
		self.solver._train()
		self.solver._save_model()
		#pickle.dump(solver, open(vars.solver_SaveFile, 'wb'))

	def _predict_grp(self):
		trial_end_idx = self.task_data['test_trial_end_idx']
		correct = 0
		total = 0
		for i in range(len(trial_end_idx) - 1):
			inputs = map(lambda (region_id, saliency_bin_nums): [region_id] + [saliency_bin_nums], zip(self.task_data['test_regions'][trial_end_idx[i] : trial_end_idx[i+1]], self.task_data['test_saliency_bin_num'][trial_end_idx[i] : trial_end_idx[i+1]]))
			avg_saliency_region = self.task_data['test_avg_saliency_region'][trial_end_idx[i] : trial_end_idx[i+1]]
			hprev1 = np.zeros((self.solver.model.hidden_size, 1)) #RNN l-1 memory
			hprev2 = np.zeros((self.solver.model.hidden_size, 1)) #RNN l-2 memory
			pred = self.solver.model._predict(inputs, hprev1, hprev2, avg_saliency_region)
			correct_label = self.task_data['test_group_targets'][trial_end_idx[i] : trial_end_idx[i+1]][1]
			if correct_label == pred:
				correct += 1
			total += 1
			print correct_label, pred
		print 'Accuracy: {0}'.format(float(correct) / total)













