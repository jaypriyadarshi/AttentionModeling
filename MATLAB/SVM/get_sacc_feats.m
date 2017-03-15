%function [first_sac_sal_vals, second_sac_sal_vals, all_sac_sal_vals, random_vals1, random_vals2, random_vals3] = get_sacc_feats(trial_num, E, movie_name, start_frames, mapName)
function [first_sac_vel_vals, second_sac_vel_vals, all_sac_vel_vals, first_sac_amp_vals, second_sac_amp_vals, all_sac_amp_vals, first_sac_ang_vals, second_sac_ang_vals, all_sac_ang_vals, first_sac_dx_vals, second_sac_dx_vals, all_sac_dx_vals, first_sac_dy_vals, second_sac_dy_vals, all_sac_dy_vals, first_sac_dur_vals, second_sac_dur_vals, all_sac_dur_vals] = get_sacc_feats(trial_num, E, movie_name, start_frames, mapName)

% if E.GRUPnum(trial_num) == 1
    trial = E.trials(trial_num);
%     disp(trial_num);
    start_time_index = E.sacs(trial_num).sIND;
    end_sacc_xy =  E.sacs(trial_num).eXY;
    all_sacc_vel = E.sacs(trial_num).pVel;
    all_sacc_amp = E.sacs(trial_num).AMPL;
    all_sacc_ang = E.sacs(trial_num).ANG;
    all_sacc_dur = E.sacs(trial_num).DUR;
    all_sacc_dx = E.sacs(trial_num).dX;
    all_sacc_dy = E.sacs(trial_num).dY;
    
    
    first_sac_sal_vals = [];
    second_sac_sal_vals = [];
    all_sac_sal_vals = []; 
    random_vals1 = []; 
    random_vals2 = []; 
    random_vals3 = [];

    if ~isempty(end_sacc_xy)
        delta_t = 150;
        x = trial.x;
        t = single(1:length(x))';
        t = t * E.res.SAMP_INT;
        t = t - t(E.dframe_tIND{trial_num}(1));
        %for index=frame_num we get the timestamp in ms
        frametime = t(E.dframe_tIND{trial_num}); 
        saccade_timestamps = t(start_time_index) - delta_t;
        %keep only true saccades, remove the ones which occured during callibration
        %disp(size(saccade_timestamps));
        saccade_timestamps = saccade_timestamps(saccade_timestamps >= 0); 

        movieFullFileName = E.CLIPname{1,E.CLIPnum(trial_num)};
        %disp(['movie is: ' movieFullFileName]);

        %start_frame numbers for all the clips in movieFullFileName
        clip_frame_start = start_frames(strmatch(movieFullFileName, movie_name, 'exact'));

        clip_frame_start = clip_frame_start + 1;
        if length(frametime) < clip_frame_start(end)
            saliency_vals = zeros(1,length(clip_frame_start));
            return
        end
        clip_change_timestamps = frametime(clip_frame_start);

        % collect saccades for each clip into bins

        clip_change_timestamps = [clip_change_timestamps' frametime(end)]';
        categorized_saccades = discretize(saccade_timestamps,clip_change_timestamps,'IncludedEdge','right');
        %%find the timestamp for first saccade in each clip and store the indexes
        %%of first saccades in first_saccade_index

        % first_sacc_amp = [];
         first_saccade_index = [];
         second_saccade_index = [];
         all_saccade_index = [];
            for i = 1:length(clip_frame_start)
                sacc_index_found = find(categorized_saccades==i);
                all_saccade_index = [all_saccade_index sacc_index_found'];
                if length(sacc_index_found) >= 1
                    first_saccade_index = [first_saccade_index sacc_index_found(1)];
                    if length(sacc_index_found) >= 2
                        second_saccade_index = [second_saccade_index sacc_index_found(2)];
                    end
%                 else
%                     disp(categorized_saccades);
%                     saccade_index(i) = sacc_index_found(end);
                end
            end
            
%             [first_sac_sal_vals, random_vals1] = get_sal_vals(E, t, saccade_timestamps, first_saccade_index, trial.x, trial.y, frametime, movieFullFileName, mapName);
%             [second_sac_sal_vals, random_vals2] = get_sal_vals(E, t, saccade_timestamps, second_saccade_index, trial.x, trial.y, frametime, movieFullFileName, mapName);
%             [all_sac_sal_vals, random_vals3] = get_sal_vals(E, t, saccade_timestamps, all_saccade_index, trial.x, trial.y, frametime, movieFullFileName, mapName);

            %uncomment for vel, amp and other features
            
             first_sac_vel_vals = get_other_sacc_vals(all_sacc_vel, saccade_timestamps, first_saccade_index);
             second_sac_vel_vals = get_other_sacc_vals(all_sacc_vel, saccade_timestamps, second_saccade_index);
             all_sac_vel_vals = get_other_sacc_vals(all_sacc_vel, saccade_timestamps, all_saccade_index);
             
             
             first_sac_amp_vals = get_other_sacc_vals(all_sacc_amp, saccade_timestamps, first_saccade_index);
             second_sac_amp_vals = get_other_sacc_vals(all_sacc_amp, saccade_timestamps, second_saccade_index);
             all_sac_amp_vals = get_other_sacc_vals(all_sacc_amp, saccade_timestamps, all_saccade_index);
             
             first_sac_ang_vals = get_other_sacc_vals(all_sacc_ang, saccade_timestamps, first_saccade_index);
             second_sac_ang_vals = get_other_sacc_vals(all_sacc_ang, saccade_timestamps, second_saccade_index);
             all_sac_ang_vals = get_other_sacc_vals(all_sacc_ang, saccade_timestamps, all_saccade_index);
             
             first_sac_dx_vals = get_other_sacc_vals(all_sacc_dx, saccade_timestamps, first_saccade_index);
             second_sac_dx_vals = get_other_sacc_vals(all_sacc_dx, saccade_timestamps, second_saccade_index);
             all_sac_dx_vals = get_other_sacc_vals(all_sacc_dx, saccade_timestamps, all_saccade_index);
             
             
             first_sac_dy_vals = get_other_sacc_vals(all_sacc_dy, saccade_timestamps, first_saccade_index);
            second_sac_dy_vals = get_other_sacc_vals(all_sacc_dy, saccade_timestamps, second_saccade_index);
             all_sac_dy_vals = get_other_sacc_vals(all_sacc_dy, saccade_timestamps, all_saccade_index);
             
             first_sac_dur_vals = get_other_sacc_vals(all_sacc_dur, saccade_timestamps, first_saccade_index);
             second_sac_dur_vals = get_other_sacc_vals(all_sacc_dur, saccade_timestamps, second_saccade_index);
             all_sac_dur_vals = get_other_sacc_vals(all_sacc_dur, saccade_timestamps, all_saccade_index);
        %saliency_vals = [saliency_vals mean(first_sacc_amp)];
        %saliency_vals = [saliency_vals mean(first_sacc_vel)];
    else
        first_sac_sal_vals = [];
        second_sac_sal_vals = [];
        all_sac_sal_vals = [];
        random_vals1 = [];
        random_vals2 = [];
        random_vals3 = [];
        
        first_sac_dur_vals = [];
        second_sac_dur_vals = [];
        all_sac_dur_vals = [];
        
        first_sac_vel_vals = [];
        second_sac_vel_vals = [];
        all_sac_vel_vals = [];
        
        first_sac_amp_vals = [];
        second_sac_amp_vals = [];
        all_sac_amp_vals = [];
        
        first_sac_dx_vals = [];
        second_sac_dx_vals = [];
        all_sac_dx_vals = [];
        
        first_sac_dy_vals = [];
        second_sac_dy_vals = [];
        all_sac_dy_vals = [];
        
        first_sac_ang_vals = [];
        second_sac_ang_vals = [];
        all_sac_ang_vals = [];
        
    end
% else
%     saliency_vals = [];
%     random_vals = [];
% end
end