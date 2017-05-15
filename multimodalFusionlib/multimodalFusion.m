function [featureLevelFusionAccuracy,decisionLevelFusionAccuracy]=multimodalFusion(datasetPath,inputExcelFile,labelColumn,nrModalities,vectorModalities,outputTxTFile)

%% function for multimodal analysis using feature level fusion and decision level fusion
% Input: path to the Excel dataset (datasetPath), name of the Excel file
% containing the dataset (inputExcelFile)
% index of the column containing labels, the number of modalities and a vector containing the feature indexes for each modality, assuming that they are provided one after the other one
% Output: accuracy for feature and decision level fusion and other results
% saved in an output txt file (outputTxTFile)

%% check if enough parameters were given and otherwise provide initialization values for the provided test sample (inputFile.xlsx)

if(nargin<6)
    outputTxTFile = 'outputFile.txt';
    disp('The filename of output file was not provided. Default one will be used');
end;

if(nargin<5)
    vectorModalities=[1,4,5,10,11,17];
    disp('The vector containing feature indexes for each modality was not provided. Default one will be used');
end;

if(nargin<4)
    nrModalities = 3;
    disp('The number of modalities was not provided. A default number of modalities will be used');
end;

if(nargin<3)
    % the labels column is assumed to the last one in the excel input file
    labelColumn = 18;
    disp('The index of the labels column was not provided. Default one will be used');
end;

if(nargin<2)
   inputExcelFile='inputFile.xlsx';
   disp('The name of the excel file was not provided. A default test file will be used');
end;

if(nargin<1)
   datasetPath='.\data\';
   disp('The path to the excel file was not provided. Default one will be used');
end;

%% add the path to the prtools machine learning library
%% wich can be downloaded from http://37steps.com/software/
p_course = genpath('.\prtools\');
addpath(p_course);

%% read the multimodal dataset
inputData=readtable(strcat(datasetPath,inputExcelFile)); 

%% read the labels from the corresponding column
labels =table2array(inputData(:,labelColumn)); 
features = table2array(inputData(:,1:end-1));

%% compute for each type of feature the sparsity level
nrFeatures = size(features,2);
nrSamples = size(features,1);
sparsityFeatures= zeros(1,nrFeatures);
for i=1:nrFeatures
    sparsityFeatures(i)=numel(find(features(:,i)>0))/nrSamples;
end;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Feature Level and Decision Level Fusion applied on the dataset
useFeatureLevelFusion = 1;
useDecisionLevelFusion = 1;
file_id = fopen(outputTxTFile,'w');
fprintf(file_id,'Results of Multimodal Fusion Library for the provided dataset\n\n');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if(useFeatureLevelFusion)
  featureLevelFusionAccuracy = featureLevelFusion(features,labels,sparsityFeatures,file_id);   
end;

if(useDecisionLevelFusion)
  decisionLevelFusionAccuracy = decisionLevelFusion(features,labels,nrModalities,vectorModalities,file_id);   
end;

fclose(file_id);

end


