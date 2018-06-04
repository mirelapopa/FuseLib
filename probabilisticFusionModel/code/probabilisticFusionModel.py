# -*- coding: utf-8 -*-
"""
Created on Fri May 25 12:11:56 2018

@author: Mirela.Popa
"""
import os
import datetime
from datetime import timedelta
from probabilisticFusionClass import probabilisticFusionClass
               
if __name__ == '__main__':
    
    # define the set of parameters
    #the list of userIds need to be updated
    listUserIds = ['2','3']    # for testing purposes we will use only 1 id, but you can complete the analysis for all the users, as long as the information about them is included in each modality file
    nrUsers = len(listUserIds)
    
    investigatedPeriodinDays = 10  #interval for MF analysis
    analysisDate = datetime.date.today()   
    
    str_date = analysisDate.strftime('%d-%m-%Y')        
    analysisDate = analysisDate.replace(2017,11,25) #this date is used for testing purposes
    
    year = analysisDate.year
    month= analysisDate.month
    day = analysisDate.day
    
    #output file of the MF module containing the results of the analysis          
    outputMFpath = '../output'
    inputM1path = '../input/M1'
    inputM2path = '../input/M2'
    inputM3path = '../input/M3'
    
    if (day<10):
        outputMF_File =  'MF_' + str(year) + str(month) + '0'+ str(day) + '.json'                                      
        inputM1_File = 'M1_' + str(year) + str(month) + '0'+ str(day) + '.json'                                      
        inputM2_File = 'M2_' + str(year) + str(month) + '0'+ str(day) + '.json'                                      
        inputM3_File =   'M3_' + str(year) + str(month) + '0'+ str(day) + '.json'                                      
    else:
        outputMF_File =  'MF_' + str(year) + str(month) + str(day) + '.json'                                                              
        inputM1_File = 'M1_' + str(year) + str(month) + str(day) + '.json'                                      
        inputM2_File = 'M2_' + str(year) + str(month) + str(day) + '.json'                                      
        inputM3_File =   'M3_' + str(year) + str(month) + str(day) + '.json'      
                                       
    outputFileMF = outputMFpath + '/' + outputMF_File   
    
    #check if all the input files are available 
    inputFileM1 = inputM1path + '/' + inputM1_File   
    inputFileM2 = inputM2path + '/' + inputM2_File   
    inputFileM3 = inputM3path + '/' + inputM3_File   
     
    if (os.path.isfile(inputFileM1) & os.path.isfile(inputFileM2) & os.path.isfile(inputFileM3)):
    
        print 'all required input files were received'
        outputFile = open(outputFileMF,'w')     
        line = '[\n'
        outputFile.writelines(line)	
        
        for i in range(nrUsers):
            
            userId = listUserIds[i]      
            print 'Analysis for user id: '+ str(userId)    
            mf = probabilisticFusionClass()
            mf.multimodalFusionalgorithm(outputFile,userId,analysisDate,investigatedPeriodinDays,inputFileM1,inputFileM2,inputFileM3)        
        
        #close the MF output file
        line = ']'
        outputFile.writelines(line)    
        outputFile.close()         
          
        print('Multimodal Fusion module completed.')    
        
    else:
        print 'not all input files are received, analysis is postponed'
