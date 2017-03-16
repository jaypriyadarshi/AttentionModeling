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
		data = scipy.io.loadmat(vars.IP_MAT_FileName)
		eye_tracker = EyeTracker(data)
		trials = []
		_ = map(lambda grp: map(lambda trial_num: trials.append(Trial(data, trial_num)), get_trials(data, grp)), vars.Groups)
		#compute frametimes
		_ = map(lambda trial: trial._compute_frametime(eye_tracker), trials)
		#preprocess (x,y) data
		_ = map(lambda trial: trial._preprocess(eye_tracker), trials)
		#get all saliency maps
		saliency_obj = Saliency_Map(vars.Saliency_Map_BaseDir, vars.Saliency_Map_Res, vars.Saliency_Map_Receptive_Field, vars.Map_Types)
		saliency_maps = map(lambda movie: saliency_obj._load_saliency_maps(movie), get_dir_entries(vars.Saliency_Map_BaseDir))
		segmented_map = saliency_obj._segment_map().astype(int) #get region label for each pixel
		#region in saliency map where (x,y) is located
		xy_regions = map(lambda trial: segmented_map[[trial.y.ravel(), trial.x.ravel()]], trials)
		saliency_bins = [] # stores which bin the saliency val corresponding to (x,y) belongs to
		avg_saliency_vals = [] # avg_saliency over different regions for all trials
		for trial_idx in range(len(trials)):
			trial_avg_saliency = []
			trial_saliency_bins = []
			frame_seq = np.digitize(trials[trial_idx].timestamps, trials[trial_idx].frametimes) #will return an array like [1,1,1,2,2,2,...] each entry indicating the framenumber
			for frame_idx in range(len(frame_seq)):
				frame_avg_saliency = []
				frame_saliency_bins = []
				for map_idx in range(len(vars.Map_Types)):
					frame_avg_saliency.append(saliency_obj._avg_saliency_region(saliency_maps[trials[trial_idx].movie_num][map_idx][frame_seq[frame_idx]].reshape(saliency_obj.height, saliency_obj.width)))
					hist, bin_edges = np.histogram(saliency_maps[trials[trial_idx].movie_num][map_idx][frame_seq[frame_idx]], bins=vars.n_bins)
					saliency_value = saliency_maps[trials[trial_idx].movie_num][map_idx][frame_seq[frame_idx]].reshape(saliency_obj.height, saliency_obj.width)[trials[trial_idx].y[frame_idx], trials[trial_idx].x[frame_idx]][0]
					frame_saliency_bins.append(np.where(bin_edges >  saliency_value)[0][0])
				trial_avg_saliency.append(frame_avg_saliency)
				trial_saliency_bins.append(frame_saliency_bin)
			avg_saliency_vals.append(trial_avg_saliency)
			saliency_bins.append(trial_saliency_bin)






