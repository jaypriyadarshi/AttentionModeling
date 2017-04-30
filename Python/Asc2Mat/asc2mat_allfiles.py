import scipy.io 
import numpy as np 
import math
import sys
from os import listdir
from os.path import isfile, join

calib_vids = []
clip_vids = []
vids = []

x_calib = []
y_calib = []
a_calib = []

x_clip = []
y_clip = []
a_clip = []

sacc_sIND = []
sacc_eIND = []
sacc_sxy = []
sacc_exy = []
sacc_dur = []
sacc_pVel = []
sacc_dx = []
sacc_dy = []
sacc_amp = []
hasBlink = []

sacc_sIND_calib = []
sacc_eIND_calib = []
sacc_sxy_calib = []
sacc_exy_calib = []
sacc_dur_calib = []
sacc_pVel_calib = []
sacc_dx_calib = []
sacc_dy_calib = []
sacc_amp_calib = []
hasBlink_calib = []

fix_sIND_calib = []
fix_eIND_calib = []
fix_sxy_calib = []
fix_exy_calib = []
fix_dx_calib = []
fix_dy_calib = []
fix_dur_calib = []

fix_sIND = []
fix_eIND = []
fix_sxy = []
fix_exy = []
fix_dx = []
fix_dy = []
fix_dur = []

SUBJnum_calib = []
SUBJnum = []
AIM = []
edf_date = []

FILEname_calib = []
FILEname = []
num_trials = []
num_trials_calib = []
FILEnum = []
FILEnum_calib = []
CLIPnum_calib = []
CLIPnum = []
blink_SIND = []
blink_eIND = []
blink_SIND_calib = []
blink_eIND_calib = []
visit = []
visit_calib = []
trialnum = []
trialnum_calib = []

all_asc_files = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
subj_count = 1
for file in all_asc_files:
	print file
	f = open(sys.argv[1] + file, 'r')
	data = f.readlines()
	f.close()

	x_trial = []
	y_trial = []
	a_trial = []

	sacc_sIND_trial = []
	sacc_eIND_trial = []
	sacc_sxy_trial = []
	sacc_exy_trial = []
	sacc_dur_trial = []
	sacc_pVel_trial = []
	sacc_dx_trial = []
	sacc_dy_trial = []
	sacc_amp_trial = []
	hasBlink_trial = []

	blink_SIND_trial = []
	blink_eIND_trial = []

	time2idx = {}

	fix_sIND_trial = []
	fix_eIND_trial = []
	fix_sxy_trial = []
	fix_exy_trial = []
	fix_dx_trial = []
	fix_dy_trial = []
	fix_dur_trial = []

	#count variable to keep track of saccade index 
	count = 0
	#to report total number of trials
	count_trials = 0
	count_calib_trials = 0

	#strip 'm.edf'
	filename = file[:-5]
	participant_data, age = filename.split("_")
	testing_site = int(participant_data[0])
	participant_num = int(participant_data[1:])
	AIM.append(int(age))

	if int(age) == 2:
		visit_num = 1
	elif int(age) == 6:
		visit_num = 2
	elif int(age) == 9:
		visit_num = 3
	elif int(age) == 12:
		visit_num = 4
	else:
		visit_num = 5


	

	blink_start = 0

	print 'CLIPs First Frame Timestamp:'
	for line in data:
		if '** DATE' in line:
			date = line.split(':')
			edf_date.append(':'.join(date[1:]).replace('\r', '').replace('\n', '').strip())

		line = map(lambda x: x.strip(), line.split('\t'))
		if line[0] == 'MSG' and '*Displayed Frames' not in line[1]:
			continue
		elif line[0] == 'MSG':
			vid_name = line[1].split()[1]
			
			if 'calibcheck' in vid_name:
				count_calib_trials += 1
				if vid_name not in calib_vids:
					calib_vids.append(vid_name)
				x_calib.append(x_trial)
				y_calib.append(y_trial)
				a_calib.append(a_trial)
				sacc_sIND_calib.append(sacc_sIND_trial)
				sacc_eIND_calib.append(sacc_eIND_trial)
				sacc_sxy_calib.append(sacc_sxy_trial)
				sacc_exy_calib.append(sacc_exy_trial)
				sacc_dur_calib.append(sacc_dur_trial)
				sacc_pVel_calib.append(sacc_pVel_trial)
				sacc_dx_calib.append(sacc_dx_trial)
				sacc_dy_calib.append(sacc_dy_trial)
				sacc_amp_calib.append(sacc_amp_trial)
				hasBlink_calib.append(hasBlink_trial)
				fix_sIND_calib.append(fix_sIND_trial)
				fix_eIND_calib.append(fix_eIND_trial)
				fix_sxy_calib.append(fix_sxy_trial)
				fix_exy_calib.append(fix_exy_trial)
				fix_dx_calib.append(fix_dx_trial)
				fix_dy_calib.append(fix_dy_trial)
				fix_dur_calib.append(fix_dur_trial)
				SUBJnum_calib.append(participant_num)
				FILEname_calib.append(file)
				FILEnum_calib.append(subj_count)
				blink_SIND_calib.append(blink_SIND_trial)
				blink_eIND_calib.append(blink_eIND_trial)
				visit_calib.append(visit_num)
				trialnum_calib.append(count_calib_trials)
				if 'sidesX' in vid_name:
					CLIPnum_calib.append(1)
				else:
					CLIPnum_calib.append(2)


			else:
				count_trials += 1
				if vid_name not in clip_vids:
					clip_vids.append(vid_name)
				x_clip.append(x_trial)
				y_clip.append(y_trial)
				a_clip.append(a_trial)
				sacc_sIND.append(sacc_sIND_trial)
				sacc_eIND.append(sacc_eIND_trial)
				sacc_sxy.append(sacc_sxy_trial)
				sacc_exy.append(sacc_exy_trial)
				sacc_dur.append(sacc_dur_trial)
				sacc_pVel.append(sacc_pVel_trial)
				sacc_dx.append(sacc_dx_trial)
				sacc_dy.append(sacc_dy_trial)
				sacc_amp.append(sacc_amp_trial)
				hasBlink.append(hasBlink_trial)
				fix_sIND.append(fix_sIND_trial)
				fix_eIND.append(fix_eIND_trial)
				fix_sxy.append(fix_sxy_trial)
				fix_exy.append(fix_exy_trial)
				fix_dx.append(fix_dx_trial)
				fix_dy.append(fix_dy_trial)
				fix_dur.append(fix_dur_trial)
				SUBJnum.append(participant_num)
				FILEname.append(file)
				FILEnum.append(subj_count)
				blink_SIND.append(blink_SIND_trial)
				blink_eIND.append(blink_eIND_trial)
				visit.append(visit_num)
				trialnum.append(count_trials)
				if 'A' in vid_name:
					CLIPnum.append(1)
				elif 'B' in vid_name:
					CLIPnum.append(2)
				elif 'C' in vid_name:
					CLIPnum.append(3)
				elif 'D' in vid_name:
					CLIPnum.append(4)
				elif 'E' in vid_name:
					CLIPnum.append(5)
				else:
					CLIPnum.append(6)

			

			x_trial = []
			y_trial = []
			a_trial = []
			sacc_sIND_trial = []
			sacc_eIND_trial = []
			sacc_sxy_trial = []
			sacc_exy_trial = []
			sacc_dur_trial = []
			sacc_pVel_trial = []
			sacc_amp_trial = []
			sacc_dx_trial = []
			sacc_dy_trial = []
			hasBlink_trial = []
			fix_sIND_trial = []
			fix_eIND_trial = []
			fix_sxy_trial = []
			fix_exy_trial = []
			fix_dx_trial = []
			fix_dy_trial = []
			fix_dur_trial = []

			count = 0
			blink_eIND_trial = []
			blink_SIND_trial = []

		elif 'EFIX' in line[0]:
			fix_start = int(line[0].split()[-1])
			fix_end = int(line[1])

			#if fixation continuing from last clip
			if fix_start < first_timestamp_clip:
				fix_start = first_timestamp_clip

			fix_sIND_trial.append(time2idx[fix_start])
			try:
				fix_eIND_trial.append(time2idx[fix_end])
			except:
				if fix_end - 1 in time2idx:
					fix_eIND_trial.append(time2idx[fix_end - 1] + 1)
					fix_end -= 1
				elif fix_end - 2 in time2idx:
					fix_exy_trial.append(time2idx[fix_end - 2] + 1)
					fix_end -= 2
			fix_sxy_trial.append([x_trial[time2idx[fix_start] - 1], y_trial[time2idx[fix_start] - 1]])
			fix_exy_trial.append([x_trial[time2idx[fix_end] - 1], y_trial[time2idx[fix_end] - 1]])
			fix_dx_trial.append(x_trial[time2idx[fix_end] - 1] - x_trial[time2idx[fix_start] - 1])
			fix_dy_trial.append(y_trial[time2idx[fix_end] - 1] - y_trial[time2idx[fix_start] - 1])
			fix_dur_trial.append(fix_end - fix_start)

		elif 'EBLINK' in line[0]:
			blink_start = int(line[0].split()[-1])
			blink_end = int(line[1])

			#if blink continuing from last clip
			if blink_start < first_timestamp_clip:
				blink_start = first_timestamp_clip

			blink_SIND_trial.append(time2idx[blink_start])
			blink_eIND_trial.append(time2idx[blink_end])


		elif 'ESACC' in line[0]:
			try:
				#replace unavialable data with NaN
				for i in range(len(line)):
					if line[i] == '.':
						line[i] = 'NaN'

				sacc_start_timestamp = int(line[0].split()[-1])
				sacc_end_timestamp = int(line[1])
				sacc_sIND_trial.append(time2idx[sacc_start_timestamp])
				sacc_eIND_trial.append(time2idx[sacc_end_timestamp])
				sacc_sxy_trial.append([float(line[3]), float(line[4])])
				sacc_exy_trial.append([float(line[5]), float(line[6])])
				sacc_dx_trial.append(float(line[5]) - float(line[3]))
				sacc_dy_trial.append(float(line[4]) - float(line[6]))
				sacc_dur_trial.append(sacc_end_timestamp - sacc_start_timestamp)
				sacc_pVel_trial.append(float(line[8]))
				sacc_amp_trial.append(float(line[7]))

				if blink_start >= sacc_start_timestamp and blink_start <= sacc_end_timestamp:
					hasBlink_trial.append(1)
				else:
					hasBlink_trial.append(0)
			except:
				pass

		else:
			try:
				timestamp = int(line[0])
				if line[1] == '.':
					x_trial.append(float('NaN'))
				else:
					x_trial.append(float(line[1]))

				if line[1] == '.':
					y_trial.append(float('NaN'))
				else:
					y_trial.append(float(line[2]))

				a_trial.append(float(line[3]))
				time2idx[timestamp] = count + 1 #matlab is 1 indexed
				count += 1
				if count == 1:
					first_timestamp_clip = timestamp 
					print first_timestamp_clip
			except:
				continue
	num_trials_calib.append(count_calib_trials)
	num_trials.append(count_trials)
	subj_count += 1

FOM = []
f = open('ToxicStressDatabaseF_DATA_LABELS_2017-02-15_1231.txt', 'r')
fom_data = f.readlines()
f.close()

for data in fom_data[1:]:
	data = data.strip().split()
	if len(data) == 2:
		if 'Male' in data.split()[1]:
			FOM.append(0)
		else:
			FOM.append(1)

#to convert python string lists to cell arrays in matlab
FOM_name = np.zeros((3,), dtype=np.object)
FOM_name[:] = ['female', 'male', 'unkown']

EDF_date = np.zeros((len(edf_date), ), dtype=np.object)
EDF_date[:] = edf_date

CLIPname = np.zeros((len(clip_vids),), dtype=np.object)
CLIPname[:] = clip_vids
CLIPname_calib = np.zeros((len(calib_vids),), dtype=np.object)
CLIPname_calib[:] = calib_vids
FILEname_cell_array = np.zeros((len(FILEname),), dtype=np.object)
FILEname_cell_array[:] = FILEname
FILEname_calib_cell_array = np.zeros((len(FILEname_calib),), dtype=np.object)
FILEname_calib_cell_array[:] = FILEname_calib



mat_data = {'E_new': {'res': {'pix_wide_screen': 1920, 'pix_high_screen': 1200, 'pix_wide_clip': 1280, 'pix_high_clip': 720, 'ref_rate': 60, 'rec_rate': 500, 'SAMP_INT': 2, 'PPD': 36.1794} , 'FOM_name': FOM_name, 'FILEname': FILEname_cell_array, 'CLIPname' : CLIPname, 'FOM': FOM, 'AIM': AIM, 'num_trials': num_trials, 'visit': visit, 'EDF_date': EDF_date, 'FILEnum': FILEnum, 'SUBJnum': SUBJnum, 'CLIPnum': CLIPnum, 'trials': np.core.records.fromarrays([x_clip,y_clip,a_clip], names='x, y, a'), 'trialnum': trialnum, 'sacs': np.core.records.fromarrays([sacc_sIND, sacc_eIND, sacc_sxy, sacc_exy, sacc_dx, sacc_dy, sacc_amp, sacc_pVel, sacc_dur, hasBlink], names='sIND, eIND, sXY, eXY, dX, dY, AMPL, pVel, DUR, hasBlink'), 'blink_SIND': blink_SIND, 'blink_eIND': blink_eIND, 'fixs': np.core.records.fromarrays([fix_sIND, fix_eIND, fix_sxy, fix_exy, fix_dx, fix_dy, fix_dur], names='sIND, eIND, sXY, eXY, dX, dY, DUR'), 'FILEname_calib': FILEname_calib_cell_array, 'CLIPname_calib': CLIPname_calib, 'num_trials_calib': num_trials_calib, 'visit_calib': visit_calib, 'FILEnum_calib': FILEnum_calib, 'SUBJnum_calib': SUBJnum_calib, 'CLIPnum_calib': CLIPnum_calib, 'trials_calib': np.core.records.fromarrays([x_calib,y_calib,a_calib], names='x, y, a'), 'trialnum_calib': trialnum_calib, 'sacs_calib': np.core.records.fromarrays([sacc_sIND_calib, sacc_eIND_calib, sacc_sxy_calib, sacc_exy_calib, sacc_dx_calib, sacc_dy_calib, sacc_amp_calib, sacc_pVel_calib, sacc_dur_calib, hasBlink_calib], names='sIND, eIND, sXY, eXY, dX, dY, AMPL, pVel, DUR, hasBlink'), 'blink_SIND_calib': blink_SIND_calib, 'blink_eIND_calib': blink_eIND_calib, 'fixs_calib': np.core.records.fromarrays([fix_sIND_calib, fix_eIND_calib, fix_sxy_calib, fix_exy_calib, fix_dx_calib, fix_dy_calib, fix_dur_calib], names='sIND, eIND, sXY, eXY, dX, dY, DUR')} }

scipy.io.savemat('Child_Data_Full', mat_data, oned_as='column')
#scipy.io.savemat('Child_Data_Full', mat_data)


