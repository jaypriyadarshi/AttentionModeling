import scipy.io 
import numpy as np 
import math
import sys
from os import listdir
from os.path import isfile, join


#all_asc_files = [f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]

#for file in all_asc_files:

f = open(sys.argv[1], 'r')
data = f.readlines()
f.close()



#count variable to keep track of saccade index 
count = 0

calib_vids = []
clip_vids = []
vids = []

x_calib = []
y_calib = []
a_calib = []

x_clip = []
y_clip = []
a_clip = []

x_trial = []
y_trial = []
a_trial = []

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

time2idx = {}

fix_sIND_trial = []
fix_eIND_trial = []
fix_sxy_trial = []
fix_exy_trial = []
fix_dx_trial = []
fix_dy_trial = []
fix_dur_trial = []

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

filename = sys.argv[1]
#strip 'm.edf'
filename = filename[:-5]
participant_data, age = filename.split("_")
testing_site = int(participant_data[0])
participant_num = int(participant_data[1:])
SUBJnum_calib = []
SUBJnum = []
AIM = [int(age)]

blink_start = 0

print 'CLIPs First Frame Timestamp:'
for line in data:
	line = map(lambda x: x.strip(), line.split('\t'))
	if line[0] == 'MSG' and '*Displayed Frames' not in line[1]:
		continue
	elif line[0] == 'MSG':
		vid_name = line[1].split()[1]
		
		if 'calibcheck' in vid_name:
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

		else:
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

	elif 'EBLINK' in line[0]:
		blink_start = int(line[0].split()[-1])
		blink_end = int(line[1])

		#if fixation continuing from last clip
		if blink_start < first_timestamp_clip:
			blink_start = first_timestamp_clip

		fix_sIND_trial.append(time2idx[blink_start])
		fix_eIND_trial.append(time2idx[blink_end])
		fix_sxy_trial.append([x_trial[time2idx[blink_start] - 1], y_trial[time2idx[blink_start] - 1]])
		fix_exy_trial.append([x_trial[time2idx[blink_end] - 1], y_trial[time2idx[blink_end] - 1]])
		fix_dx_trial.append(x_trial[time2idx[blink_end] - 1] - x_trial[time2idx[blink_start] - 1])
		fix_dy_trial.append(y_trial[time2idx[blink_end] - 1] - y_trial[time2idx[blink_start] - 1])
		fix_dur_trial.append(blink_end - blink_start)


	elif 'ESACC' in line[0]:
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

		if blink_start != 0:
			if blink_start >= sacc_start_timestamp and blink_start <= sacc_end_timestamp:
				hasBlink_trial.append(1)
			else:
				hasBlink_trial.append(0)

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

mat_data = {'E_new': {'SUBJnum_calib': SUBJnum_calib, 'SUBJnum': SUBJnum, 'AIM': AIM, 'trials': np.core.records.fromarrays([x_clip,y_clip,a_clip], names='x, y, a'), 'calib_trials': np.core.records.fromarrays([x_calib,y_calib,a_calib], names='x, y, a'), 'CLIPname' : clip_vids.sort(), 'CALIBname': calib_vids, 'sacs': np.core.records.fromarrays([sacc_sIND, sacc_eIND, sacc_sxy, sacc_exy, sacc_dx, sacc_dy, sacc_amp, sacc_pVel, sacc_dur, hasBlink], names='sIND, eIND, sXY, eXY, dX, dY, AMPL, pVel, DUR, hasBlink'), 'calib_sacs': np.core.records.fromarrays([sacc_sIND_calib, sacc_eIND_calib, sacc_sxy_calib, sacc_exy_calib, sacc_dx_calib, sacc_dy_calib, sacc_amp_calib, sacc_pVel_calib, sacc_dur_calib, hasBlink_calib], names='sIND, eIND, sXY, eXY, dX, dY, AMPL, pVel, DUR, hasBlink'), 'fixs': np.core.records.fromarrays([fix_sIND, fix_eIND, fix_sxy, fix_exy, fix_dx, fix_dy, fix_dur], names='sIND, eIND, sXY, eXY, dX, dY, DUR'), 'calib_fixs': np.core.records.fromarrays([fix_sIND_calib, fix_eIND_calib, fix_sxy_calib, fix_exy_calib, fix_dx_calib, fix_dy_calib, fix_dur_calib], names='sIND, eIND, sXY, eXY, dX, dY, DUR') } }  

scipy.io.savemat('Child_Data', mat_data, oned_as='column')


