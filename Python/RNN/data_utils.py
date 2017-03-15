import scipy.io 
import numpy as np
from vars import MAT_FileName, Actual_Res, Saliency_Map_Res

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
		self.x = int((self.x + newOrigin[0]) / (Actual_Res[0] / Saliency_Map_Res[0]))
		self.y += int((self.y + newOrigin[1]) / (Actual_Res[0] / Saliency_Map_Res[0]))

	#for index = frame_num we get the timestamp in ms
	def _get_frametime(self, eye_tracker):
		self.timestamps = np.arange(self.x.shape[0]).reshape(self.x.shape[0],1)
		self.timestamps *= eye_tracker.SAMP_INT
		self.timestamps -= self.timestamps[self.dframe_tIND[0]]
		return self.timestamps[self.dframe_tIND.ravel()]
