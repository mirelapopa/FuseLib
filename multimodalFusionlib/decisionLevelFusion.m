function [accuracyCombination] = decisionLevelFusion(features,labels, nrModalities,vectorModalities,file_id)

fprintf(file_id,'Decision (Late) level fusion results \n\n');
fprintf(file_id,'Several settings are considered: \n');

%% compute accuracies for different settings
accuracy = zeros(1,2);

%% define a set of classifiers
classifiers = {fisherc(),knnc(),parzenc(),qdc(),ldc(),loglc()};

%% evaluate separately different modalities (or groups of semantically different features)
%% according to the parameters (number of Modalities and the vector of feature indexes for each modality)

accuracy = [];
val = [];index =0;
fprintf(file_id,'Initially the accuracies of each modality is computed for a set of classifiers: \n');

for i=1:2:2*nrModalities
    
    index=index+1;
    features_modality = features(:,vectorModalities(i):vectorModalities(i+1));
    
    D_modality{index} = prdataset(features_modality,labels);
    
    [ERR,CERR,NLAB_OUT] = prcrossval(D_modality{index},classifiers,5); % 5 cross-fold validation for the set of provided classifiers
    [accuracy(index),val(index)]=max(1-ERR);    
    
    fprintf(file_id,'Modality %d achieved an accuracy of %f for the %s classifier.\n',index,accuracy(index),classifiers{val(index)}.name);
    
end;

[acc_independent,index_modality] = max(accuracy);
fprintf(file_id,'The best accuracy of %f is obtained for the %d modality. \n',acc_independent,index_modality);

%% combination of all datasets at the decision level using different rules (max, sum, mean and product)
accuracy_combination1 = zeros(1,4);
accuracy_combination2 = zeros(1,4);
accuracy_combination3 = zeros(1,4);

for i=1:nrModalities
    
    randreset; % reset the random number generator
  
    [train{i},test{i}] = gendat(D_modality{i},0.5); % generate randomly a training and a testing set for each modality          
    W1{i} = train{i}*knnc*classc; % train the K-NN classifier for the considered modality
    W2{i} = train{i}*loglc*classc; % train the Logistic Regression classifier for the considered modality
    W3{i} = train{i}*ldc*classc; % train the Liniar Discriminat classifier for the considered modality           
end;

for i=1:nrModalities
    if(i==1)
        W1_=W1{i};W2_=W2{i};W3_=W3{i};
        test_=test{1};
    else
        W1_=[W1_;W1{i}];W2_=[W2_;W2{i}];W3_=[W3_;W3{i}];
        test_ = [test_,test{i}];
    end;
end;



results1=testc(test_,{W1_*maxc,W1_*minc,W1_*meanc,W1_*prodc}); %% apply the different combination rules to the test sets
results2=testc(test_,{W2_*maxc,W2_*minc,W2_*meanc,W2_*prodc}); %% apply the different combination rules to the test sets
results3=testc(test_,{W3_*maxc,W3_*minc,W3_*meanc,W3_*prodc}); %% apply the different combination rules to the test sets

for i=1:4  
 accuracy_combination1(i)=1-results1{i};
 accuracy_combination2(i)=1-results2{i};
 accuracy_combination3(i)=1-results3{i};
end;

[acc_combination1,combinationRule1] = max(accuracy_combination1);
fprintf(file_id,'The accuracies obtained for different combination rules using the K-NN classifier are for the maximum %f, minimum %f, average %f and product %f rule.\n',accuracy_combination1(1),accuracy_combination1(2),accuracy_combination1(3),accuracy_combination1(4));

[acc_combination2,combinationRule2] = max(accuracy_combination2);
fprintf(file_id,'The accuracies obtained for different combination rules using the Logistic Regression classifier are for the maximum %f, minimum %f, average %f and product %f rule.\n',accuracy_combination2(1),accuracy_combination2(2),accuracy_combination2(3),accuracy_combination2(4));
 
[acc_combination3,combinationRule3] = max(accuracy_combination3);
fprintf(file_id,'The accuracies obtained for different combination rules using the Linear Discriminant classifier are for the maximum %f, minimum %f, average %f and product %f rule.\n\n',accuracy_combination3(1),accuracy_combination3(2),accuracy_combination3(3),accuracy_combination3(4));

[accuracyCombination,~] = max([acc_independent,acc_combination1,acc_combination2,acc_combination3])
fprintf(file_id,'The best accuracy for the decision level fusion is: %f. \n',accuracyCombination);

end

