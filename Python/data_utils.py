import scipy.io 
from vars import MAT_FileName

class Trial(object):
	def __init__(self, data, idx):
		self.group = data['E']['GRUPnum'][0][0][0][idx]
		self.x = data['E']['trials'][0][0][0][idx]['x']
		self.y = data['E']['trials'][0][0][0][idx]['y']
		self.trial_num = idx + 1
		self.movie_num = data['E']['CLIPnum'][0][0][0][idx]
		self.movie_name = data['E']['CLIPname'][0][0][0][self.movie_num - 1] #MATLAB is 1-indexed

	#def preprocess():
"""
class Movie(object):
	def __init__(self, name):
"""
#class saliency_data(object):



if __name__ == '__main__':
	data = scipy.io.loadmat(MAT_FileName)
