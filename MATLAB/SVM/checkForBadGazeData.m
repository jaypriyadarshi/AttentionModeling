% Checks whether each trial has bad gaze data 
% Puts trial info into a struct called "badTrials" if any of the below 
% conditions are met:
% 1) xy or area vectors are filled with zeros
% 2) xy or area data has not been recorded for entire duration of clip
% 3) saccade calculations are missing
% 4) there are not enough frame indices for the length of the clip (E.dframe_tIND)
% 09-26-2016 A. Gharib

addpath(genpath(pwd))
%load('E_FVIEW_for_ONDRICTRLx_2016-09-13_13h37m45s_firstvisit.mat');
load('ClipStats.mat')

trialCount = 1;

for trialNum = 1:5635
    
    trialxydata = E.trials(trialNum);
    trialsacdata = E.sacs(trialNum);
    
    % 1) xy or area vectors are filled with zeros
    xya_zeros = any(all(trialxydata.x == 0) | all(trialxydata.y == 0) | all(trialxydata.a == 0));
    if xya_zeros
        warning('Trial %s has invalid x,y, or pupil area data.', num2str(trialNum))
    end
    
    % 2) xy or area data has not been recorded for entire duration of clip
    minSamples = ClipStats(E.CLIPnum(trialNum)).Duration * E.res.rec_rate;
    xya_short = any(length(trialxydata.x) < minSamples | length(trialxydata.y) < minSamples | length(trialxydata.a) < minSamples);
    if xya_short
        warning('Trial %s has not enough x,y, or pupil area data.', num2str(trialNum))
    end
    
    % 3) saccade calculations are missing
    sacs_empty = arrayfun(@(s) any(structfun(@isempty,s)), trialsacdata);
    if sacs_empty
        warning('Trial %s is missing saccade calculations.', num2str(trialNum))
    end
    
    % 4) there are not enough frame indices for the length of the clip (E.dframe_tIND)
    dframe_tIND = E.dframe_tIND{1,trialNum}; % get frame refresh timestamps for the trial
    dframe_tIND_short = length(dframe_tIND) ~= ClipStats(E.CLIPnum(trialNum)).NumFrames;
    if dframe_tIND_short
        warning('Trial %s does not have the correct number of frame refresh timestamps.', num2str(trialNum))
    end
    
    % Make note of bad trial number and issues in struct
    if any( xya_zeros | sacs_empty | dframe_tIND_short)
        badTrials(trialCount).trialNum = trialNum;
        badTrials(trialCount).xya_zeros = xya_zeros;
        badTrials(trialCount).xya_short = xya_short;
        badTrials(trialCount).sacs_empty = sacs_empty;
        badTrials(trialCount).dframe_tIND_short = dframe_tIND_short;
        
        trialCount = trialCount + 1;
    end
    
end

