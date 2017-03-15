function [saliency_vals, random_vals] = get_sal_vals(E, t, saccade_timestamps, saccade_index, x, y, frametime, movieFullFileName, mapName)

first_saccade_timestamps = saccade_timestamps(saccade_index);
        data_txy = [t, single(x)/1000, single(y)/1000];
        [~, loc]=ismember(data_txy(:,1), first_saccade_timestamps);
        first_sacc_xy = data_txy(loc>0, 2:3);
    %     first_sacc_amp = all_sacc_amps(first_saccade_index,:);
    %     first_sacc_vel = all_sacc_vel(first_saccade_index,:);


        %to find the closest frame to the timestamp when saccade occured
        frame_num_saccades = discretize(first_saccade_timestamps, frametime);
        frame_num_saccades = frame_num_saccades - 1;

        %loading the appropriate feature map
        [file_name, ~] = strtok(movieFullFileName, '.');
        file_path = strcat('../iLab-ONDRI-EyeTracking/clips/Feature_map/', file_name);
        file_path = strcat(file_path,'/feat', mapName, '.mat');
        load(file_path);

        %removing the case if the first index is zero
        frame_num_saccades(frame_num_saccades == 0) = 1;
        frame_num_saccades = frame_num_saccades(~isnan(frame_num_saccades));
        
        first_sacc_feats = feats(frame_num_saccades,:);

        %DVA to pixels
        first_sacc_xy =  first_sacc_xy .* E.res.PPD;

        %change the axes to image axes
        newOrigin = [E.res.pix_wide/2 E.res.pix_high/2];
        first_sacc_xy(:,1) = first_sacc_xy(:,1) + newOrigin(1);
        first_sacc_xy(:,2) = first_sacc_xy(:,2) + newOrigin(2);

        %get it to 64x80 from 1024x1280
        first_sacc_xy = floor(first_sacc_xy ./ 16);
        %save('first_sacc_xy.mat','first_sacc_xy');
        %feature_map_index = (first_sacc_xy(:,2) - 1) .* 80 + first_sacc_xy(:,1);
        [num_clips, ~] = size(first_sacc_feats);
        saliency_vals = [];
        random_vals = [];
        for i = 1:num_clips
            feature_map = reshape(first_sacc_feats(i,:), [64 80]);
            if first_sacc_xy(i,1) <= 80 && first_sacc_xy(i,2) <= 64 && first_sacc_xy(i,1) > 0 && first_sacc_xy(i,2) > 0
                saliency_vals = [saliency_vals feature_map(first_sacc_xy(i,2), first_sacc_xy(i,1))];
                random_vals = [random_vals feature_map(randi(64,1,1), randi(80,1,1))];
            end    
        end