#Stores all the variables
IP_MAT_FileName = '../SVM/E_FVIEW_for_ONDRICTRLx_2016-09-13_13h37m45s_firstvisit.mat'
BadTrial_FileName = 'badTrials.mat'
Actual_Res = {'height': 1024, 'width': 1280}
Saliency_Map_Res = {'height': 64, 'width': 80}
Saliency_Map_BaseDir = '/lab/jayp/TS/iLab-ONDRI-EyeTracking/clips/Feature_map'
Map_Types = ['C', 'F', 'I', 'M', 'O']
Saliency_Map_Receptive_Field = {'height': 16, 'width': 16} #GCD(64,80), to reduce the number of parameters for now
max_saliency_SaveFile = 'max_saliency_vals.p'
Groups = [1,2,3,4,5,6]
Groups_len = [150, 116]
train_trials_per_category = 10
test_trials_per_category = 3
n_bins = 3
num_regions = (Saliency_Map_Res['height'] / Saliency_Map_Receptive_Field['height']) * (Saliency_Map_Res['width'] / Saliency_Map_Receptive_Field['width'])
ip_dim = num_regions + (len(Map_Types) * n_bins) + (num_regions * len(Map_Types)) # num regions + 5 sal maps + avg region vals from 5 maps
#ip_dim = num_regions + (len(Map_Types) * n_bins)
num_classes = 6

#hyperparameters
hidden_size = 128 # size of hidden layer of neurons
seq_length = 15 # number of steps to unroll the RNN for
learning_rate = 1e-1
num_iter = 2000000
update_rule = 'adagrad'

#model params
model_SaveFile = 'model.p'
solver_SaveFile = 'solver.p'
data_SaveFile = 'partial_data.p'
train_data_file = 'train_data.p'
test_data_file = 'test_data.p'
training_stats_file = 'training_stats_file.txt'
