function [bestAccuracy,method] = featureLevelFusion(features,labels,sparsityFeatures,file_id)

fprintf(file_id,'Feature (Early) level fusion results \n');
fprintf(file_id,'Several settings are considered: \n');
%% compute accuracies for different settings
accuracy = zeros(1,3);

%% compute accuracy for fusing all features
D = prdataset(features,labels); % construct a dataset using the provided features and labels
classifiers = {fisherc(),knnc(),parzenc(),qdc(),ldc(),loglc()};
[ERR,CERR,NLAB_OUT] = prcrossval(D,classifiers,5); % 5 cross-fold validation for the set of provided classifiers
accuracy(1)=max(1-ERR); % select the best accuracy

fprintf(file_id,'1) fusion of all features from all the modalities: %f \n',accuracy(1));

 %% find the feature indices which have a higher sparsity level than a threshold
 threshold = 0.01;
 indFeatures = find(sparsityFeatures>threshold);
 
features_s = features(:,indFeatures);
Ds = prdataset(features_s,labels);
classifiers = {fisherc(),knnc(),parzenc(),qdc(),ldc(),loglc()};
 
[ERR,CERR,NLAB_OUT] = prcrossval(Ds,classifiers,5); % 5 cross-fold validation for the set of provided classifiers
accuracy(2)=max(1-ERR);
fprintf(file_id,'2) fusion of the features with a sparsity level higher than a pre-defined treshold: %f \n',accuracy(2));
fprintf(file_id,'(this option is especially useful for sparse datasets) \n');

%% feature selection
[W,R] = featseli(D);

w=R(:,2); 
w=R(:,2)./sum(R(:,2)); % normalize the obtained weights for each feature

% define the threshold for feature selection
threshold_selection = mean(w);
indices=R(:,3); % select the ordered feature indices
index_selected = max(find(w>=threshold_selection)); 

features_sel= features(:,indices(1:index_selected));

D_sel = prdataset(features_sel,labels);
classifiers = {fisherc(),knnc(),parzenc(),qdc(),ldc(),loglc()};
[ERR,CERR,NLAB_OUT] = prcrossval(D_sel,classifiers,5);
accuracy(3) = max(1-ERR);

fprintf(file_id,'3) fusion of the salient features using a feature selection algorithm: %f \n',accuracy(3));

[bestAccuracy,method] = max(accuracy);

fprintf(file_id,'The best result of %f for early level fusion was obtained for the %d option. \n\n',bestAccuracy,method);

%fprintf(file_id,'2) fusion of the features with a sparsity level higher than a pre-defined treshold: %f \n',accuracy(1));
end

