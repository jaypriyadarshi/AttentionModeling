import scipy.io 
import numpy as np
import h5py
import os
import cPickle as pickle
import vars

class EyeTracker(object):
	def __init__(self, data):
		self.pix_wide = data['E']['res'][0][0][0]['pix_wide'][0][0][0]
		self.pix_high = data['E']['res'][0][0][0]['pix_high'][0][0][0]
		self.ref_rate = data['E']['res'][0][0][0]['ref_rate'][0][0][0]
		self.rec_rate = data['E']['res'][0][0][0]['rec_rate'][0][0][0]
		self.SAMP_INT = data['E']['res'][0][0][0]['SAMP_INT'][0][0][0]
		self.PPD = data['E']['res'][0][0][0]['PPD'][0][0][0]

class Trial(object):
	def __init__(self, data, idx):
		self.group = data['E']['GRUPnum'][0][0][0][idx]
		self.x = data['E']['trials'][0][0][0][idx]['x']
		self.y = data['E']['trials'][0][0][0][idx]['y']
		self.trial_num = idx + 1
		self.movie_num = data['E']['CLIPnum'][0][0][0][idx]
		self.movie_name = data['E']['CLIPname'][0][0][0][self.movie_num - 1] #MATLAB is 1-indexed
		self.dframe_tIND = data['E']['dframe_tIND'][0][0][0][idx].ravel() # Index in timestamps at which the actual trial started, basically the index after which timestamps are positive

	#Takes (x,y) and filters only the (x,y) for which timestamp is >= 0 and scales transforms (x,y) to salinency map dimensions, 
	#also takes eye tracker object as a paramter
	def _preprocess(self, eye_tracker):
		#only consider (x,y) in the actual trial and not calibration
		self.x = self.x[self.dframe_tIND[0] :]
		self.y = self.y[self.dframe_tIND[0] :]
		#DVA to pixels
		self.x = (self.x * eye_tracker.PPD) / 1000
		self.y = (self.y * eye_tracker.PPD) / 1000
		#change axes to image axes
		newOrigin = [eye_tracker.pix_wide / 2, eye_tracker.pix_high / 2]
		#get it to saliency map resolution 
		self.x = ((self.x + newOrigin[0]) / (vars.Actual_Res['height'] / vars.Saliency_Map_Res['height'])).astype(int) - 1 #MATLAB is 1-indexed
		self.y += ((self.y + newOrigin[1]) / (vars.Actual_Res['height'] / vars.Saliency_Map_Res['height'])).astype(int) - 1

	#for index = frame_num we get the timestamp in ms
	def _get_frametime(self, eye_tracker):
		self.timestamps = np.arange(self.x.shape[0]).reshape(self.x.shape[0],1)
		self.timestamps *= eye_tracker.SAMP_INT
		self.timestamps -= self.timestamps[self.dframe_tIND[0]]
		return self.timestamps[self.dframe_tIND.ravel()]

#for all operations on saliency maps
class Saliency_Map(object):
	def __init__(self, Saliency_Map_BaseDir, Saliency_Map_Res, Saliency_Map_Receptive_Field, Map_Types):
		self.height = Saliency_Map_Res['height']
		self.width = Saliency_Map_Res['width']
		self.segment_height = Saliency_Map_Receptive_Field['height']
		self.segment_width = Saliency_Map_Receptive_Field['width']
		self.base_dir = Saliency_Map_BaseDir
		self.map_types = Map_Types
		self.max_saliency_vals = pickle.load(open(max_saliency_SaveFile, 'rb'))

	def _load_saliency_map(self, movie_name, map_type):
		file_path = self.base_dir + '/' + movie_name.split('.')[0] + '/feat' + map_type + '.mat'
		f = h5py.File(file_path)
		feat_map = np.array((f.get('feats')))
		return feat_map.T

	#cuts the saliency map grid into different regions based on saliency map receptive field parameter
	def _segment_saliency_map(self):
		grid = np.zeros((self.height, self.width))
		label = 0
		for r in range(0, self.height, self.segment_height):
			for c in range(0, self.width, self.segment_width):
				grid[r : r + self.segment_height, c : c + self.segment_width] = label
				label += 1
		return grid

	#takes the saliency map and gives the average saliency value in each region assigned by Segment_Saliency_Map()
	def _avg_saliency_region(self, feat_map):
		avg_vals = []
		for r in range(0, self.height, self.segment_height):
			for c in range(0, self.width, self.segment_width):
				avg_vals.append(np.mean(feat_map[r : r + self.segment_height, c : c + self.segment_width]))
		return np.array(avg_vals)

	#Finds the global max of all map types (one value for each map type - C, F, I, M, O)
	def _find_max_saliency_vals(self, file_names):
		max_vals = {}
		for map_type in self.map_types:
			max_vals[map_type] = max(map(lambda file_name: self._load_saliency_map(file_name, map_type).max(), file_names))
		pickle.dump(max_vals, open(max_saliency_SaveFile, 'wb'))
		return max_vals

	def _normalize(self, feat_map, map_type):
		return feat_map / self.max_saliency_vals[map_type]


def get_dir_entries(base_dir):
	return [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

#gets all the trails for a particular group
def get_trials(data, group_num):
	return np.where(data['E']['GRUPnum'][0][0][0] == group_num)[0]

