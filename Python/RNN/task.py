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
		#preprocess (x,y) data
		_ = map(lambda trial: trial._preprocess(eye_tracker), trials)
		#get frametimes
		frametimes = map(lambda trial: trial._get_frametime(eye_tracker), trials)
		#get all saliency maps
		saliency_obj = Saliency_Map(vars.Saliency_Map_BaseDir, vars.Saliency_Map_Res, vars.Saliency_Map_Receptive_Field, vars.Map_Types)
		saliency_maps = map(lambda movie: saliency_obj._load_saliency_maps(movie), get_dir_entries(vars.Saliency_Map_BaseDir))
		segmented_map = saliency_obj._segment_map().astype(int) #get region label for each pixel
		#region in saliency map where (x,y) is located
		xy_regions = map(lambda trial: segmented_map[[trial.y.ravel(), trial.x.ravel()]], trials)
		avg_saliency_vals = [] # avg_saliency over different regions for all trials
		for trial_idx in range(len(trials)):
			trial_avg_saliency = []
			frametimes = trials[trial_idx]._get_frametime(eye_tracker)
			for map_idx in range(len(vars.Map_Types)):
				trial_avg_saliency.append(saliency_maps[trials[trial_idx].movie_num][map_idx][frame_num].reshape(vars.Saliency_Map_Res['height'], vars.Saliency_Map_Res['width']))





