﻿# FuseLib library for multimodal fusion of multiple modalities
The user can choose for a specific fusion algorithm from the available ones, or test all of them for finding the most suitable one.
The early fusion is perfomed using the concatenation of all input features, corresponding to all the modalities, after a normalization step which rescales the features in the same interval. 
The late fusion is performed at the end of the processing pipeline, after training each modality independently using machine learning algorithms. 
The multimodal fusion function can be called using a set of parameters containing: the Excel file location, the number of modalities, the range of column indexes for each modality, the labels column index and the name of the output file. The input parameters file (multimodalFusion_parametersFile.txt) is optional and is useful in case the user wants to customize the different available options, otherwise default values will be used.
function [featureLevelFusionAccuracy, decisionLevelFusionAccuracy] = multimodalFusion (datasetPath, inputExcelFile, labelsColumn, numberOfModalities, rangeModalityFeatures, outputTxTFile)
The results of the analysis will be stored in the outputTxTFile.txt, containing the accuracy for each modality, the best classification method, the results for early and late fusion, as well as the best fusion algorithm.
