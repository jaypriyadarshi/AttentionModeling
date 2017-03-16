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
		


