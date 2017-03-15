function [subtrials] = reconditionData(subtrials)
% Recondition data into single
% A. Gharib 06-27-2016

% do_this_guy = 1;
% 
% subtrials = E.trials(E.SUBJnum == do_this_guy);
% subclips = E.CLIPnum(E.SUBJnum == do_this_guy);

for ii = 1:length(subtrials)
    subtrials(ii).x = single(subtrials(ii).x)/1000;
    subtrials(ii).y = single(subtrials(ii).y)/1000;
    %subtrials(ii).s = single(subtrials(ii).s)/10;
end