% load('E_FVIEW_for_ONDRICTRLx_2016-09-13.mat')
% load('end_frames.mat')
load('start_frames.mat')
load('movie_name.mat')
load('badTrials.mat')



n_bins = 10;

avoid_trials = [];
avoid_trials = [avoid_trials badTrials.trialNum];
%maps = ['C', 'F', 'I', 'M', 'O'];
maps = ['C'];
% error on 145 one
for map_idx = 1:length(maps)
    feats_sac1 = [];
    feats_sac2 = [];
    feats_sac_a = [];

    random_sac1 = [];
    random_sac2 = [];
    random_sac_a = [];
    s1_vel = [];
    s2_vel = []; 
    s_a_vel = [];
    s1_amp = [];
    s2_amp = []; 
    s_a_amp = [];
    s1_dx = [];
    s2_dx = []; 
    s_a_dx = [];
    s1_dy = [];
    s2_dy = []; 
    s_a_dy = [];
    s1_ang = [];
    s2_ang = []; 
    s_a_ang = [];
    s1_dur = [];
    s2_dur = []; 
    s_a_dur = [];
    
    for subject = 1:581
        disp(subject);
        if subject == 582
            histogram_feats = vertcat(histogram_feats,[0 0 0]);
        else
            clip_nums = E.CLIPnum(E.SUBJnum==subject);
            trial_nums = find(E.SUBJnum == subject);

            random_feats = [];       
            histogram_feat = [];
         


                subject_feats_s1 = [];
                subject_feats_s2 = [];
                subject_feats_sa = [];
                random_s1 = [];
                random_s2 = [];
                random_sa = [];
                s1_vel_feats = [];
                s2_vel_feats = [];
                s_a_vel_feats = [];
                s1_dy_feats = [];
                s2_dy_feats = [];
                s_a_dy_feats = [];
                
                s1_dx_feats = [];
                s2_dx_feats = [];
                s_a_dx_feats = [];
                
                s1_amp_feats = [];
                s2_amp_feats = [];
                s_a_amp_feats = [];
                
                s1_ang_feats = [];
                s2_ang_feats = [];
                s_a_ang_feats = [];
                
                s1_dur_feats = [];
                s2_dur_feats = [];
                s_a_dur_feats = [];
                
                for i = 1:length(trial_nums)
                    if sum(ismember(trial_nums(i), avoid_trials)) == 0
                        %[feats1, feats2, feats3, random_vals1, random_vals2, random_vals3] = get_sacc_feats(trial_nums(i), E, movie_name, start_frames, maps(map_idx));
                        [first_sac_vel_vals, second_sac_vel_vals, all_sac_vel_vals, first_sac_amp_vals, second_sac_amp_vals, all_sac_amp_vals, first_sac_ang_vals, second_sac_ang_vals, all_sac_ang_vals, first_sac_dx_vals, second_sac_dx_vals, all_sac_dx_vals, first_sac_dy_vals, second_sac_dy_vals, all_sac_dy_vals, first_sac_dur_vals, second_sac_dur_vals, all_sac_dur_vals] = get_sacc_feats(trial_nums(i), E, movie_name, start_frames, maps(map_idx)); 
%                         subject_feats_s1 = horzcat(subject_feats_s1, feats1);
%                         subject_feats_s2 = horzcat(subject_feats_s2, feats2);
%                         subject_feats_sa = horzcat(subject_feats_sa, feats3);
% 
%                         random_s1 = horzcat(random_s1, random_vals1);
%                         random_s2 = horzcat(random_s2, random_vals2);
%                         random_sa = horzcat(random_sa, random_vals3);

                           s1_vel_feats = horzcat(s1_vel_feats, first_sac_vel_vals');
                           s2_vel_feats = horzcat(s2_vel_feats, second_sac_vel_vals');
                           s_a_vel_feats = horzcat(s_a_vel_feats, all_sac_vel_vals');
                           
                           s1_amp_feats = horzcat(s1_amp_feats, first_sac_amp_vals');
                           s2_amp_feats = horzcat(s2_amp_feats, second_sac_amp_vals');
                           s_a_amp_feats = horzcat(s_a_amp_feats, all_sac_amp_vals');
                           
                           s1_ang_feats = horzcat(s1_ang_feats, first_sac_ang_vals');
                           s2_ang_feats = horzcat(s2_ang_feats, second_sac_ang_vals');
                           s_a_ang_feats = horzcat(s_a_ang_feats, all_sac_ang_vals');
                           
                           s1_dx_feats = horzcat(s1_dx_feats, first_sac_dx_vals');
                           s2_dx_feats = horzcat(s2_dx_feats, second_sac_dx_vals');
                           s_a_dx_feats = horzcat(s_a_dx_feats, all_sac_dx_vals');
                           
                           s1_dy_feats = horzcat(s1_dy_feats, first_sac_dy_vals');
                           s2_dy_feats = horzcat(s2_dy_feats, second_sac_dy_vals');
                           s_a_dy_feats = horzcat(s_a_dy_feats, all_sac_dy_vals');
                           
                           s1_dur_feats = horzcat(s1_dur_feats, first_sac_dur_vals');
                           s2_dur_feats = horzcat(s2_dur_feats, second_sac_dur_vals');
                           s_a_dur_feats = horzcat(s_a_dur_feats, all_sac_dur_vals');

                    end
                end


                %load sac1_thresold i.e 90th percentile
                
%                 load(strcat('percentile/95_pctile_sac1_', maps(map_idx), '.mat'))
%                 subject_feats_s1(subject_feats_s1 >= val) = val;
%                 subject_feats_s1 = histcounts(subject_feats_s1, n_bins) ./ length(subject_feats_s1);
%                 random_s1(random_s1 >= val) = val;
%                 random_s1 = histcounts(random_s1, n_bins) ./ length(random_s1);
%                 load(strcat('percentile/95_pctile_sac2_', maps(map_idx), '.mat'))
%                 subject_feats_s2(subject_feats_s2 >= val) = val;
%                 subject_feats_s2 = histcounts(subject_feats_s2, n_bins) ./ length(subject_feats_s2);
%                 random_s2(random_s2 >= val) = val;
%                 random_s2 = histcounts(random_s2, n_bins) ./ length(random_s2);
%                 load(strcat('percentile/95_pctile_sac_a_', maps(map_idx), '.mat'))
%                 subject_feats_sa(subject_feats_sa >= val) = val;
%                 subject_feats_sa = histcounts(subject_feats_sa, n_bins) ./ length(subject_feats_sa);
%                 random_sa(random_sa >= val) = val;
%                 random_sa = histcounts(random_sa, n_bins) ./ length(random_sa);


                  s1_vel_feats = histcounts(s1_vel_feats, n_bins) ./ length(s1_vel_feats);
                  s2_vel_feats = histcounts(s2_vel_feats, n_bins) ./ length(s2_vel_feats);
                  s_a_vel_feats = histcounts(s_a_vel_feats, n_bins) ./ length(s_a_vel_feats);
                  
                  s1_amp_feats = histcounts(s1_amp_feats, n_bins) ./ length(s1_amp_feats);
                  s2_amp_feats = histcounts(s2_amp_feats, n_bins) ./ length(s2_amp_feats);
                  s_a_amp_feats = histcounts(s_a_amp_feats, n_bins) ./ length(s_a_amp_feats);
                  
                  s1_ang_feats = histcounts(s1_ang_feats, n_bins) ./ length(s1_ang_feats);
                  s2_ang_feats = histcounts(s2_ang_feats, n_bins) ./ length(s2_ang_feats);
                  s_a_ang_feats = histcounts(s_a_ang_feats, n_bins) ./ length(s_a_ang_feats);
                  
                  s1_dur_feats = histcounts(s1_dur_feats, n_bins) ./ length(s1_dur_feats);
                  s2_dur_feats = histcounts(s2_dur_feats, n_bins) ./ length(s2_dur_feats);
                  s_a_dur_feats = histcounts(s_a_dur_feats, n_bins) ./ length(s_a_dur_feats);
                  
                  s1_dx_feats = histcounts(s1_dx_feats, n_bins) ./ length(s1_dx_feats);
                  s2_dx_feats = histcounts(s2_dx_feats, n_bins) ./ length(s2_dx_feats);
                  s_a_dx_feats = histcounts(s_a_dx_feats, n_bins) ./ length(s_a_dx_feats);
                  
                  s1_dy_feats = histcounts(s1_dy_feats, n_bins) ./ length(s1_dy_feats);
                  s2_dy_feats = histcounts(s2_dy_feats, n_bins) ./ length(s2_dy_feats);
                  s_a_dy_feats = histcounts(s_a_dy_feats, n_bins) ./ length(s_a_dy_feats);

% 
%             feats_sac1 = vertcat(feats_sac1, subject_feats_s1);
%             feats_sac2 = vertcat(feats_sac2, subject_feats_s2);
%             feats_sac_a = vertcat(feats_sac_a, subject_feats_sa);
% 
%             random_sac1 = vertcat(random_sac1, random_s1);
%             random_sac2 = vertcat(random_sac2, random_s2);
%             random_sac_a = vertcat(random_sac_a, random_sa);

              s1_vel = vertcat(s1_vel, s1_vel_feats);
              s2_vel = vertcat(s2_vel, s2_vel_feats);
              s_a_vel = vertcat(s_a_vel, s_a_vel_feats);
              
              s1_amp = vertcat(s1_amp, s1_amp_feats);
              s2_amp = vertcat(s2_amp, s2_amp_feats);
              s_a_amp = vertcat(s_a_amp, s_a_amp_feats);
              
              s1_ang = vertcat(s1_ang, s1_ang_feats);
              s2_ang = vertcat(s2_ang, s2_ang_feats);
              s_a_ang = vertcat(s_a_ang, s_a_ang_feats);
              
              
              s1_dx = vertcat(s1_dx, s1_dx_feats);
              s2_dx = vertcat(s2_dx, s2_dx_feats);
              s_a_dx = vertcat(s_a_dx, s_a_dx_feats);
              
              
              s1_dy = vertcat(s1_dy, s1_dy_feats);
              s2_dy = vertcat(s2_dy, s2_dy_feats);
              s_a_dy = vertcat(s_a_dy, s_a_dy_feats);
              
              s1_dur = vertcat(s1_dur, s1_dur_feats);
              s2_dur = vertcat(s2_dur, s2_dur_feats);
              s_a_dur = vertcat(s_a_dur, s_a_dur_feats);
              
            % pick my own bin locations;
            % no_bins = linspace(0, 100, 20); 
            % y1 = hist(subject_feats, no_bins);
            % y2 = hist(random_feats, no_bins);
            % plot the results:
            % bar(no_bins, [y1;y2]');
            % title('Cross validation plot');

        end

    end
% save(strcat('features/no_pctl_sac1_', maps(map_idx), '.mat'),'feats_sac1');
% save(strcat('features/no_pctl_sac2_', maps(map_idx), '.mat'),'feats_sac2');
% save(strcat('features/no_pctl_sac_a_', maps(map_idx), '.mat'),'feats_sac_a');
% save(strcat('features/no_pctl_random1_', maps(map_idx), '.mat'),'random_sac1');
% save(strcat('features/no_pctl_random2_', maps(map_idx), '.mat'),'random_sac2');
% save(strcat('features/no_pctl_random_a_', maps(map_idx), '.mat'),'random_sac_a');

save(strcat('features/sac1_10_b_pvel.mat'),'s1_vel');
save(strcat('features/sac2_10_b_pvel.mat'),'s2_vel');
save(strcat('features/sac_a_10_b_pvel.mat'),'s_a_vel');

save(strcat('features/sac1_10_b_amp.mat'),'s1_amp');
save(strcat('features/sac2_10_b_amp.mat'),'s2_amp');
save(strcat('features/sac_a_10_b_amp.mat'),'s_a_amp');

save(strcat('features/sac1_10_b_ang.mat'),'s1_ang');
save(strcat('features/sac2_10_b_ang.mat'),'s2_ang');
save(strcat('features/sac_a_10_b_ang.mat'),'s_a_ang');

save(strcat('features/sac1_10_b_dx.mat'),'s1_dx');
save(strcat('features/sac2_10_b_dx.mat'),'s2_dx');
save(strcat('features/sac_a_10_b_dx.mat'),'s_a_dx');


save(strcat('features/sac1_10_b_dy.mat'),'s1_dy');
save(strcat('features/sac2_10_b_dy.mat'),'s2_dy');
save(strcat('features/sac_a_10_b_dy.mat'),'s_a_dy');

save(strcat('features/sac1_10_b_dur.mat'),'s1_dur');
save(strcat('features/sac2_10_b_dur.mat'),'s2_dur');
save(strcat('features/sac_a_10_b_dur.mat'),'s_a_dur');


end




% save('avg_sacc_amp.mat','mean_amp');
% save('avg_sacc_vel.mat','mean_vel');