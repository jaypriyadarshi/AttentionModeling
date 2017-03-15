labels = [];
for subject = 1:570
    trial_nums = find(E.SUBJnum == subject);
    labels = vertcat(labels, E.GRUPnum(trial_nums(1)));
end

save('labels.mat', 'labels')