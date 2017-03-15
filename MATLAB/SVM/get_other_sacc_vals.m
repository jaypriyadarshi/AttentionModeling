function [sacc_attr_vals] = get_other_sacc_vals(all_sacc_attr, saccade_timestamps, saccade_index)
    sacc_attr_vals = [];
    first_saccade_timestamps = saccade_timestamps(saccade_index);
    [size_valid_sacc var] = size(saccade_timestamps);
    [size_sacc_attr var] = size(all_sacc_attr); 
    %removing the values of vel, amp etc belonging to negative saccade
    %timestamps
    all_sacc_attr = all_sacc_attr(size_sacc_attr - size_valid_sacc + 1 : end);
    data_txy = [saccade_timestamps, all_sacc_attr];
    [~, loc]=ismember(data_txy(:,1), first_saccade_timestamps);
    sacc_attr_vals = data_txy(loc>0, 2);
end