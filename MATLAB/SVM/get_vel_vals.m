function [sacc_vels] = get_vel_vals(all_sacc_vel, saccade_timestamps, saccade_index)

first_saccade_timestamps = saccade_timestamps(saccade_index);
data_txy = [saccade_timestamps, all_sacc_vel];
[~, loc]=ismember(data_txy(:,1), first_saccade_timestamps);
sacc_vels = data_txy(loc>0, 2);
end