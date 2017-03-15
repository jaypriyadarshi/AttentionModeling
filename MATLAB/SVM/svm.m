sac1 = [];
load('features/no_pctl_sac1_C.mat');
sac1 = horzcat(sac1, feats_sac1);
load('features/no_pctl_sac1_F.mat');
sac1 = horzcat(sac1, feats_sac1);
load('features/no_pctl_sac1_I.mat');
sac1 = horzcat(sac1, feats_sac1);
load('features/no_pctl_sac1_M.mat');
sac1 = horzcat(sac1, feats_sac1);
load('features/no_pctl_sac1_O.mat');
sac1 = horzcat(sac1, feats_sac1);

sac2 = [];
load('features/no_pctl_sac2_C.mat');
sac2 = horzcat(sac2, feats_sac2);
load('features/no_pctl_sac2_F.mat');
sac2 = horzcat(sac2, feats_sac2);
load('features/no_pctl_sac2_I.mat');
sac2 = horzcat(sac2, feats_sac2);
load('features/no_pctl_sac2_M.mat');
sac2 = horzcat(sac2, feats_sac2);
load('features/no_pctl_sac2_O.mat');
sac2 = horzcat(sac2, feats_sac2);

sac_a = [];
load('features/no_pctl_sac_a_C.mat');
sac_a = horzcat(sac_a, feats_sac_a);
load('features/no_pctl_sac_a_F.mat');
sac_a = horzcat(sac_a, feats_sac_a);
load('features/no_pctl_sac_a_I.mat');
sac_a = horzcat(sac_a, feats_sac_a);
load('features/no_pctl_sac_a_M.mat');
sac_a = horzcat(sac_a, feats_sac_a);
load('features/no_pctl_sac_a_O.mat');
sac_a = horzcat(sac_a, feats_sac_a);

random1 = [];
load('features/no_pctl_random1_C.mat');
random1 = horzcat(random1, random_sac1);
load('features/no_pctl_random1_F.mat');
random1 = horzcat(random1, random_sac1);
load('features/no_pctl_random1_I.mat');
random1 = horzcat(random1, random_sac1);
load('features/no_pctl_random1_M.mat');
random1 = horzcat(random1, random_sac1);
load('features/no_pctl_random1_O.mat');
random1 = horzcat(random1, random_sac1);

random2 = [];
load('features/no_pctl_random2_C.mat');
random2 = horzcat(random2, random_sac2);
load('features/no_pctl_random2_F.mat');
random2 = horzcat(random2, random_sac2);
load('features/no_pctl_random2_I.mat');
random2 = horzcat(random2, random_sac2);
load('features/no_pctl_random2_M.mat');
random2 = horzcat(random2, random_sac2);
load('features/no_pctl_random2_O.mat');
random2 = horzcat(random2, random_sac2);

random_a = [];
load('features/no_pctl_random_a_C.mat');
random_a = horzcat(random_a, random_sac_a);
load('features/no_pctl_random_a_F.mat');
random_a = horzcat(random_a, random_sac_a);
load('features/no_pctl_random_a_I.mat');
random_a = horzcat(random_a, random_sac_a);
load('features/no_pctl_random_a_M.mat');
random_a = horzcat(random_a, random_sac_a);
load('features/no_pctl_random_a_O.mat');
random_a = horzcat(random_a, random_sac_a);

load('features/sac1_pvel.mat');
load('features/sac1_amp.mat');
load('features/sac1_ang.mat');
load('features/sac1_dx.mat');
load('features/sac1_dy.mat');
load('features/sac1_dur.mat');

mis_sac1 = horzcat(s1_vel, s1_amp, s1_ang, s1_dx, s1_dy, s1_dur);

load('features/sac2_pvel.mat');
load('features/sac2_amp.mat');
load('features/sac2_ang.mat');
load('features/sac2_dx.mat');
load('features/sac2_dy.mat');
load('features/sac2_dur.mat');

mis_sac2 = horzcat(s2_vel, s2_amp, s2_ang, s2_dx, s2_dy, s2_dur);

load('features/sac_a_pvel.mat');
load('features/sac_a_amp.mat');
load('features/sac_a_ang.mat');
load('features/sac_a_dx.mat');
load('features/sac_a_dy.mat');
load('features/sac_a_dur.mat');

mis_sac_a = horzcat(s_a_vel, s_a_amp, s_a_ang, s_a_dx, s_a_dy, s_a_dur);

all_feats = horzcat(sac1, sac2, sac_a, mis_sac1, mis_sac2, mis_sac_a);
%all_feats = horzcat(sac1, sac2, sac_a);
%all_feats = horzcat(mis_sac1, mis_sac2, mis_sac_a);
%all_feats = sac1;
%all_feats = random_a;
%all_feats = horzcat(random1, random2, random_a);
load('labels.mat');

train_feats = [];
train_labels = [];
test_feats = [];
test_labels = [];

class_lables = [1, 2];
min_subj = min([length(find(labels == class_lables(1))) length(find(labels == class_lables(2)))]);
train_end = 0.8 * min_subj;
test_end = min_subj - train_end;
accuracies = [];
for i = 1:100
    train_feats = [];
    train_labels = [];
    test_feats = [];
    test_labels = [];
    for label = 1:length(class_lables)
        idx = find(labels == class_lables(label));
        disp(length(labels));
        shuff_idx = randperm(length(idx));
        shuff_idx = idx(shuff_idx);
        %train_end = cast(0.8 * length(idx), 'uint32');
        train_idx = shuff_idx(1:train_end);
        %test_idx = idx(train_end + 1:end);
        test_idx = shuff_idx(train_end + 1: train_end + test_end);
        train_feats = vertcat(train_feats, all_feats(train_idx,:));
        test_feats = vertcat(test_feats, all_feats(test_idx,:));
        train_labels = vertcat(train_labels, labels(train_idx));
        test_labels = vertcat(test_labels, labels(test_idx));
    end

    train_idx_shuff = randperm(length(train_labels));
    train_feats_shuff = train_feats(train_idx_shuff, :);
    train_labels_shuff = double(train_labels(train_idx_shuff));

    test_idx_shuff = randperm(length(test_labels));
    test_feats_shuff = test_feats(test_idx_shuff, :);
    test_labels_shuff = double(test_labels(test_idx_shuff));

    model = svmtrain(train_labels_shuff, train_feats_shuff, '-s 0 -t 0 -c 1');
    predict = svmpredict(test_labels_shuff, test_feats_shuff, model);
    accuracies = horzcat(accuracies, sum(predict == test_labels_shuff) / length(test_labels_shuff));
end    
mean_accuracy = mean(accuracies)
std_accuracies = std(accuracies)


