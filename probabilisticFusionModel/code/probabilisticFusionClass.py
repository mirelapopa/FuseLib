# -*- coding: utf-8 -*-
"""
Created on Fri May 25 17:10:21 2018

@author: Mirela.Popa
"""

import numpy as np
import time, datetime
import ast
import matplotlib.pyplot as plt
import os
from matplotlib.figure import Figure
from datetime import timedelta
import json
from pprint import pprint
        
class probabilisticFusionClass():
    
    def __init__(self,nightMotion=[],visitsBathroom=[],incontinence=[],digitalTime=[],abnormalDigitalEvents=[],insomnia=0,comorbiditesNeurologist=0,comorbiditesUrinary=0,comorbiditesPsychiatrist=0,depression=0,hipertension=0,comorbiditesCardiovascular=0,heart_rate=[],heartRateLow=[],heartRateHigh=[],gsr=[]):
             
        self.nightMotion = nightMotion
        self.visitsBathroom = visitsBathroom
        self.incontinence = incontinence        
        self.heartRate = heart_rate 
        self.heartRateLow = heartRateLow  
        self.heartRateHigh = heartRateHigh 
        self.galvanicSkinResponse = gsr
        self.digitalTime = digitalTime
        self.abnormalDigitalEvents = abnormalDigitalEvents    
        self.insomnia = insomnia 
        self.depression = depression
        self.hipertension = hipertension
        self.comorbiditesCardiovascular = comorbiditesCardiovascular
        self.comorbiditesNeurologist = comorbiditesNeurologist
        self.comorbiditesUrinary= comorbiditesUrinary
        self.comorbiditesPsychiatrist= comorbiditesPsychiatrist
                      
    def parseM2File(self,filePath,userId,startDate,nrDays):       
        
        nr_visits_bathroom = np.zeros(shape =nrDays)        
        nr_night_visits = np.zeros(shape =nrDays)        
        heart_rate = np.zeros(shape =nrDays)
        heartRateLow = np.zeros(shape =nrDays)
        heartRateHigh = np.zeros(shape =nrDays)
        gsr = np.zeros(shape =nrDays)  
        foundUserId = 0
        indexAnalysis = 0
        startDate = startDate.strftime('%Y-%m-%d')    
        startDate =  datetime.datetime.strptime(startDate,'%Y-%m-%d')       
        
        with open(filePath) as f:
       
            try:
                d = json.load(f) 
                #pprint(d)    
                
            except ValueError,e:
                print e
                
            for line in d:                   
                
                if ('userID' in line.keys()):                    
                    if(line['userID']==userId):
                        foundUserId = 1                        
                        
                    if ('date' in line.keys()):
                        
                        dateFile = datetime.datetime.strptime(str(line['date']),'%Y-%m-%d')
                        difDays = (dateFile-startDate).days                          
                        indexAnalysis = difDays                                               
                                         
                    if('hr' in line.keys()):
                        hr_dict = line['hr']
                        heartRate = round(hr_dict.get('50'))                      
                        heart_rate[indexAnalysis] = heartRate
                        
                    if('gsr' in line.keys()):
                        gsr_dict = line['gsr']
                        gsrValue = round(gsr_dict.get('50'))                      
                        gsr[indexAnalysis] = gsrValue
                           
                    if('heart_rate_low' in line.keys()):
                        hrL_dict = line['heart_rate_low']
                        heartRate_low = round(hrL_dict.get('number'))                                             
                        heartRateLow[indexAnalysis] = heartRate_low
                                    
                    if('heart_rate_high' in line.keys()):
                        hrH_dict = line['heart_rate_high']
                        heartRate_high = round(hrH_dict.get('number'))                                             
                        heartRateHigh[indexAnalysis] = heartRate_high            
                                    
                    if('as_day_motion' in line.keys()):
           
                        daily_dict = line['as_day_motion']
                    
                        toilet_dict = daily_dict.get('toilet') 
                        if('event' in toilet_dict.keys()):
                            toilet_events = toilet_dict.get('event')
                            toiletNr = len(toilet_events)
                            if(toiletNr>0):
                                toilet_duration = np.zeros(shape=
								
								toiletNr)
                                for i in range(toiletNr):
                                    dictToilet = toilet_events[i]                            
                                    toilet_duration[i] = dictToilet.get('duration')                                                               
                        else:
                            toiletNr = 0                        
                        
                        entrance_dict = daily_dict.get('entrance')
                        if('event' in entrance_dict.keys()):
                            entrance_events = entrance_dict.get('event')
                            entranceNr = len(entrance_events)                            
                            if(entranceNr>0):
                                entrance_duration = np.zeros(shape=entranceNr)
                                for i in range(entranceNr):
                                    dictEntrance = entrance_events[i]                            
                                    entrance_duration[i] = dictEntrance.get('duration')
                        else:
                            entranceNr = 0                                                                                                         
                        
                    if('as_night_motion' in line.keys()):
           
                        daily_dict = line['as_day_motion']
                    
                        toilet_dict = daily_dict.get('toilet') 
                        if('event' in toilet_dict.keys()):
                            toilet_events = toilet_dict.get('event')
                            toiletNr = len(toilet_events)
                            if(toiletNr>0):
                                toilet_duration = np.zeros(shape=toiletNr)
                                for i in range(toiletNr):
                                    dictToilet = toilet_events[i]                            
                                    toilet_duration[i] = dictToilet.get('duration')                                                               
                        else:
                            toiletNr = 0                        
                        
                        entrance_dict = daily_dict.get('entrance')
                        if('event' in entrance_dict.keys()):
                            entrance_events = entrance_dict.get('event')
                            entranceNr = len(entrance_events)                            
                            if(entranceNr>0):
                                entrance_duration = np.zeros(shape=entranceNr)
                                for i in range(entranceNr):
                                    dictEntrance = entrance_events[i]                            
                                    entrance_duration[i] = dictEntrance.get('duration')
                        else:
                            entranceNr = 0
                                                
                        bedroom_dict = daily_dict.get('bedroom')  
                        if('event' in bedroom_dict.keys()):
                            bedroom_events = bedroom_dict.get('event')
                            bedroomNr = len(bedroom_events)
                        
                            if(bedroomNr>0):
                                bedroom_duration = np.zeros(shape=bedroomNr)
                                for i in range(bedroomNr):
                                    dictBedroom = bedroom_events[i]                            
                                    bedroom_duration[i] = dictBedroom.get('duration')
                        else:
                            bedroomNr = 0                                                    
                        nr_night_visits[indexAnalysis] = toiletNr + entranceNr + bedroomNr                                                                                        

                        if('visit_bathroom' in line.keys()):
                            
                            visit_bathroom_dict = line['visit_bathroom']
                            if('number' in visit_bathroom_dict.keys()):                                
                                nr_visits_bathroom[indexAnalysis] = visit_bathroom_dict.get('number')  
                            if('event' in visit_bathroom_dict.keys()):
                                visit_bathroomEvents = visit_bathroom_dict.get('event')
                                visit_bathroomNr = len(visit_bathroomEvents)
                        
                                if(visit_bathroomNr>0):
                                    visit_bathroom_duration = np.zeros(shape=visit_bathroomNr)
                                    for i in range(visit_bathroomNr):
                                        dictvisit_bathroom = visit_bathroomEvents[i]                            
                                        visit_bathroom_duration[i] = dictvisit_bathroom.get('duration')           
             
        return foundUserId, nr_visits_bathroom, nr_night_visits, heart_rate, heartRateLow, heartRateHigh, gsr    

    def parseM1File(self,filePath,userId,nrDays,startDate,currentDate):
       
        foundUserId = 0
        depression = 0
        comorbiditesNeurologist = 0
        comorbiditesPsychiatrist  = 0
        comorbiditesCardiovascular = 0
        hipertension = 0
        comorbiditesUrinary = 0
        incontinence = 0
        insomnia = 0
        
        startDate = datetime.datetime(startDate.year, startDate.month, startDate.day)
        currentDate = datetime.datetime(currentDate.year, currentDate.month, currentDate.day)        
               
        with open(filePath) as f:
            
            try:
                d = json.load(f) 
                #print(d)    
                
            except ValueError,e:
                print e
                
            for line in d:                   
                
                if ('userID' in line.keys()):                    
                    if(line['userID']==userId):
                        foundUserId = 1
                        #print 'found patient'                                                                                                            
                                         
                    if ('depression' in line.keys()):  
          
                        depression = int(line['depression'])                 
       
                    if ('comorbiditiesNeurologist' in line.keys()):

                        comorbiditesNeurologist = int(line['comorbiditiesNeurologist'])
           
                    if ('comorbiditiesPsychiatrist' in line.keys()):
          
                        comorbiditesPsychiatrist = int(line['comorbiditiesPsychiatrist'])
                    
                    if ('comorbiditiesCardiovascular' in line.keys()):
          
                        comorbiditesCardiovascular = int(line['comorbiditiesCardiovascular'])          
                   
                    if ('hipertension' in line.keys()):
                        hipertension = int(line['hipertension'])
           
                    if ('comorbiditiesUrinary' in line.keys()):
          
                        comorbiditesUrinary = int(line['comorbiditiesUrinary'])
           
                    if ('incontinence' in line.keys()):
          
                        incontinence = int(line['incontinence'])
       
                    if ('insomnia' in line.keys()):
          
                        insomnia = int(line['insomnia'])        
                    else:
                        str = 'process other functionalities'
                        #print obj
                        
        return foundUserId, comorbiditesNeurologist, comorbiditesPsychiatrist, comorbiditesCardiovascular, hipertension, comorbiditesUrinary, incontinence, insomnia, depression
    
    def parseM3File(self,filePath,userId,nrDays):
    
        usageTime = np.zeros(shape= nrDays)
        
        
        with open(filePath) as f:       
            try:
                d = json.load(f) 
                #pprint(d)    
                
            except ValueError,e:
                print e
                
            for line in d:                   
                
                if ('userID' in line.keys()):                    
                    if(line['userID']==userId):
                        foundUserId = 1
                        #print 'found patient'
                        
                    if ('timeUsage' in line.keys()):                       
                                                
                        time_dict = line['timeUsage']
                        usage_time = time_dict.get('durationPerDay')
                        ind = 0;
                        for i in usage_time:                            
                            usageTime[ind]=round(i,2)
                            ind = ind + 1                   
                                                                
        return usageTime
       
    def fuseUserInformation(self,outputFile,investigatedPeriodinDays):
        
        halfInterval = int(investigatedPeriodinDays/2) 
                  
        #evaluation of the number of visits during the night
        nr_night_visits = self.nightMotion
        maxValue = max(nr_night_visits)
        if maxValue>0:
            nr_night_visits_ = nr_night_visits/maxValue
        else:
            nr_night_visits_ = nr_night_visits
            
        # assess deviations in the night motion
        nightMotion_period1 = np.mean(nr_night_visits_[:halfInterval])    
        nightMotion_period2 = np.mean(nr_night_visits_[halfInterval:])
        
        percent_nightMotion = nightMotion_period2-nightMotion_period1 
                
        if percent_nightMotion > 0.1:
            line = 'Night motion, increase of: ' + str(round(percent_nightMotion*100)) + '%; ' + str(nr_night_visits) + "\n"
            probabilityInsomnia_nightMotion = percent_nightMotion
            
        elif percent_nightMotion < -0.1:
            line = 'Night motion, decrease of: ' + str(round(-percent_nightMotion*100)) + '%; ' + str(nr_night_visits) + "\n"
            
        else:
            line = 'Night motion, no deviations; ' + str(nr_night_visits) + "\n"                 
        print line
        
        line = '\t\t\"nightMotion\":{\n' + '\t\t\t\"result\":' + str(round(percent_nightMotion*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_night_visits))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
    
        insomnia = self.insomnia
        line = '\t\t\"insomnia\":'+str(insomnia)+',\n'
        outputFile.writelines(line)
    
        if(percent_nightMotion>=0):
            probabilityInsomnia_nightMotion = percent_nightMotion              
        else:
            # for decreasing night motion the probability of insomnia is very low
            probabilityInsomnia_nightMotion = 0.001            
                      
        if(insomnia):
            probabilityInsomnia_nightMotion = 0.4*probabilityInsomnia_nightMotion                        
        else:
            probabilityInsomnia_nightMotion = 0.6*probabilityInsomnia_nightMotion            
                
        #plot a graph of the night motion over the investigated days
        showGraph_nightMotion = 0
        if showGraph_nightMotion:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_night_visits)),int(max(nr_night_visits))]
            plt.plot(nr_night_visits,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of events during the night over the investigated days')
            plt.show()
        
        #assess the deviations in the number of visits to the bathroom
        nr_visits_bathroom = self.visitsBathroom
        maxValue = max(nr_visits_bathroom)
        if maxValue>0:
            nr_visits_bathroom_ = nr_visits_bathroom/maxValue
        else:
            nr_visits_bathroom_ = nr_visits_bathroom
            
        nr_visits_bathroom_period1 = np.mean(nr_visits_bathroom_[:halfInterval])
        nr_visits_bathroom_period2 = np.mean(nr_visits_bathroom_[halfInterval:])
        
        percent_nr_visits_bathroom = nr_visits_bathroom_period2 - nr_visits_bathroom_period1 
        
        if percent_nr_visits_bathroom > 0.3:
        
            line = 'Number of visits to the bathroom, increase of: ' + str(round(percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
                   
            if (self.comorbiditesUrinary > 0) or (self.incontinence > 0):
                line1 = 'As the patient has also some urinary problems, a visit to the professional is indicated.'              
                   
        elif percent_nr_visits_bathroom > 0.1:
                
            line = 'Number of visits to the bathroom, increase of: ' + str(round(percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
                   
        elif percent_nr_visits_bathroom < -0.1:
            line = 'Number of visits to the bathroom, decrease of: ' + str(round(-percent_nr_visits_bathroom*100))+ '%; ' + str(nr_visits_bathroom) + "\n"
           
        else:
            line = 'Number of visits to the bathroom, no deviations; '  + str(nr_visits_bathroom) + "\n"
        print line
            
        line = '\t\t\"visitBathroom\":{\n' + '\t\t\t\"result\":' + str(round(percent_nr_visits_bathroom*100)) + ',\n' +'\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,nr_visits_bathroom))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        incontinence = self.incontinence
        
        line = '\t\t\"incontinence\":'+str(incontinence) + ', \n'
        outputFile.writelines(line)

        if(percent_nr_visits_bathroom>=0):            
            probabilityIncontinence_visitsBathroom = 0.7*(percent_nr_visits_bathroom)
        else:
            # for decreasing number of visits to the bathroom the probability of Parkinson events is very low
            probabilityIncontinence_visitsBathroom = 0.001 
        probabilityIncontinence_medicalCondition = 0.3*incontinence 
        incontinenceProb = probabilityIncontinence_medicalCondition  + probabilityIncontinence_visitsBathroom                        
        
        #plot a graph of the number of visits to the bathroom over the investigated days
        showGraph_bathroom = 0
        if showGraph_bathroom:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(nr_visits_bathroom)),int(max(nr_visits_bathroom))]
            plt.plot(nr_visits_bathroom,'ro')
            plt.axis(days_axis)
            plt.xlabel('Number of visits to the bathroom over the investigated days')
            plt.show()
                
        #assess the heart rate events for detecting deviations 
        hr_events = self.heartRate      
        maxValue = max(hr_events)
        if maxValue>0:
            hr_events_ = hr_events/maxValue
        else:
            hr_events_ = hr_events
            
        hr_period1 = np.mean(hr_events_[:halfInterval])
        hr_period2 = np.mean(hr_events_[halfInterval:])
        
        percent_hr = hr_period2 - hr_period1
       
        if percent_hr > 0.2:
        
            line = 'Heart rate, increase of: ' + str(round(percent_hr*100))+ '%; ' + str(hr_events) + "\n"
                    
        elif percent_hr < -0.2:
            line = 'Heart rate, decrease of: ' + str(round(-percent_hr*100)) + '%; ' + str(hr_events) + "\n"
            
        else:
            line = 'Heart rate, no significant deviations; ' + str(hr_events) + "\n"
        print line                
        
        line = '\t\t\"heart_rate\":{\n' + '\t\t\t\"result\":' + str(round(percent_hr*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,hr_events))+'\n\t\t\t],\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(abs(percent_hr)>=0.2):            
            probabilityHipertension_hr= 0.7*(percent_hr)
        else:
            probabilityHipertension_hr = 0.001
        probabilityHipertension_medicalCondition = 0.3*self.hipertension
        hipertensionProb = probabilityHipertension_medicalCondition  + probabilityHipertension_hr                        
        
        if(abs(percent_hr)>=0.2):            
            probabilityCardiovascular_hr= 0.7*(percent_hr)
        else:
            probabilityCardiovascular_hr = 0.001
        probabilityCardiovascular_medicalCondition = 0.3*self.comorbiditesCardiovascular
        cardiovascularProb = probabilityCardiovascular_medicalCondition  + probabilityCardiovascular_hr
                      
        #assess the deviations in the time spent on digital devices
        time_dit =self.digitalTime
        maxValue = max(time_dit)        
        if maxValue>0:
            time_dit_ = time_dit/maxValue
        else:
            time_dit_ = time_dit

        time_dit1 = np.mean(time_dit_[:halfInterval])
        time_dit2 = np.mean(time_dit_[halfInterval:])
      
        percent_time_dit = time_dit2 - time_dit1 
        
        if percent_time_dit > 0.3:
        
            line = 'Time spent on digital devices, increase of: ' + str(round(percent_time_dit*100))+ '%; ' + str(time_dit) + "\n"
            print line         
            #outputFile.writelines(line)        
        
        elif percent_time_dit > 0.1:
                
            line = 'Time spent on digital devices, increase of: ' + str(round(percent_time_dit*100))+ '%; ' + str(time_dit) + "\n" 
                    
        elif percent_time_dit < -0.1:
            line = 'Time spent on digital devices, decrease of: ' + str(round(-percent_time_dit*100))+ '%; ' + str(time_dit) + "\n" 
            
        else:
            line = 'Time spent on digital devices, no deviations; '+ str(time_dit) + "\n" 
        print line
                
        line = '\t\t\"digitalTimeSpent\":{\n' + '\t\t\t\"result\":' + str(round(percent_time_dit*100)) + ',\n' + '\t\t\t\"events\":[\n\t\t\t\t'+',\n\t\t\t\t'.join(map(str,time_dit))+'\n\t\t\t]\n' + '\t\t},\n'              
        outputFile.writelines(line)
        
        if(percent_time_dit>=0):            
            probabilityDigitalAddiction_timeDit = 0.6*(percent_time_dit)                  
        else:
            # for decreasing digital time usage the probability of addiction is very low
            probabilityDigitalAddiction_timeDit = 0.001             

        probabilityDigitalAddiction_depression =  0.3*self.depression
        probDigitalAddiction = probabilityDigitalAddiction_depression + probabilityDigitalAddiction_timeDit
               
        #plot a graph of the time spent on dit over the investigated days
        showGraph_time = 0
        if showGraph_time:
            fig = plt.figure()              
            days_axis = [1,investigatedPeriodinDays,int(min(time_dit)),int(max(time_dit))]
            plt.plot(time_dit,'ro')
            plt.axis(days_axis)
            plt.xlabel('Amount of time spent on the digital platform over the investigated days')
            plt.show()
     
        probabilityInsomnia_digitalAddiction = 0.2*probDigitalAddiction
        probabilityInsomnia_depression = 0.2*self.depression
        probabilityInsomnia_medicalCondition = 0.3*insomnia
        insomniaProb = probabilityInsomnia_medicalCondition + probabilityInsomnia_nightMotion + probabilityInsomnia_depression + probabilityInsomnia_digitalAddiction

        if(insomniaProb>1):
            insomniaProb = 0.9
            
        line = '\t\t\"probabilities\":[\n' 
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|nightMotion\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_nightMotion,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|digitalAddiction\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_digitalAddiction,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|depression\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_depression,3)) + '\n\t\t},\n'
        outputFile.writelines(line)   
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round(probabilityInsomnia_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Insomnia\",\n'+'\t\t\t\"value\":'+str(round(insomniaProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence|visitsBathroom\",\n'+'\t\t\t\"value\":'+str(round(probabilityIncontinence_visitsBathroom,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round( probabilityIncontinence_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)          
        
        line = '\t\t{\n\t\t\t\"type\":\"Incontinence\",\n'+'\t\t\t\"value\":'+str(round(incontinenceProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)              
             
        line = '\t\t{\n\t\t\t\"type\":\"Hipertension|biologicalMeasurements\",\n'+'\t\t\t\"value\":'+str(round(probabilityHipertension_hr,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Hipertension|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round( probabilityHipertension_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  

        line = '\t\t{\n\t\t\t\"type\":\"Hipertension\",\n'+'\t\t\t\"value\":'+str(round(hipertensionProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)              
        
        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition|biologicalMeasurements\",\n'+'\t\t\t\"value\":'+str(round(probabilityCardiovascular_hr,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition|medicalCondition\",\n'+'\t\t\t\"value\":'+str(round(probabilityCardiovascular_medicalCondition,3)) + '\n\t\t},\n'
        outputFile.writelines(line)  

        line = '\t\t{\n\t\t\t\"type\":\"Cardiovascular condition\",\n'+'\t\t\t\"value\":'+str(round(cardiovascularProb,3)) + '\n\t\t},\n'
        outputFile.writelines(line)    
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction|digitalTimeUsage\",\n'+'\t\t\t\"value\":'+str(round(probabilityDigitalAddiction_timeDit,3)) + '\n\t\t},\n'
        outputFile.writelines(line)            
        
        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction|depression\",\n'+'\t\t\t\"value\":'+str(round(probabilityDigitalAddiction_depression,3)) + '\n\t\t},\n'
        outputFile.writelines(line)            
                
        line = '\t\t{\n\t\t\t\"type\":\"digitalAddiction\",\n'+'\t\t\t\"value\":'+str(round(probDigitalAddiction,3)) + '\n\t\t},\n'
        outputFile.writelines(line)
        
        line = '\t\t]\n\t}\n'
        outputFile.writelines(line)          
            
    def multimodalFusionalgorithm(self,outputFile,userId,currentDate,investigatedPeriodinDays,inputFileM1,inputFileM2,inputFileM3):    
      
        # currentDay = currentDate.day
        startDate = currentDate + timedelta(days=-investigatedPeriodinDays)
              
        # parse the M1 File
        foundUser, comorbiditesNeurologist, comorbiditesPsychiatrist, comorbiditesCardiovascular, hipertension, comorbiditesUrinary, incontinence, insomnia, depression  = self.parseM1File(inputFileM1,userId,investigatedPeriodinDays,startDate,currentDate)
        
        if(foundUser):            
            
            self.insomnia = insomnia
            self.incontinence = incontinence
            self.depression = depression
            self.comorbiditesNeurologist = comorbiditesNeurologist
            self.comorbiditesUrinary= comorbiditesUrinary
            self.comorbiditesPsychiatrist= comorbiditesPsychiatrist
            self.comorbiditesCardiovascular = comorbiditesCardiovascular       
            self.hipertension = hipertension            
                        
            line = '\t{\n'+'\t\t\"userID\":\"user'+str(userId)+ '\",\n'
            outputFile.writelines(line)
    
            line = '\t\t\"startDate\":\"' + str(startDate) + '\",\n' 
            outputFile.writelines(line)
            line = '\t\t\"endDate\":\"' + str(currentDate) + '\",\n' 
            outputFile.writelines(line)          
        
            # parameters for DIT analysis
            time_dit = np.zeros(shape= (investigatedPeriodinDays))                     
            time_dit = self.parseM3File(inputFileM3,userId,investigatedPeriodinDays)                                               
        
            # extract the M2 parameters for each of the investigated day in the predefined period
            nr_visits_bathroom = np.zeros(shape= (investigatedPeriodinDays))        
            nr_night_visits = np.zeros(shape= (investigatedPeriodinDays))
            heart_rate = np.zeros (shape= (investigatedPeriodinDays))
            heartRateLow = np.zeros (shape= (investigatedPeriodinDays))
            heartRateHigh = np.zeros (shape= (investigatedPeriodinDays))
            gsr = np.zeros (shape= (investigatedPeriodinDays))
            #movement_evolution_events = np.zeros(shape= (investigatedPeriodinDays))                  
                     
            foundUserId, nr_visits_bathroom, nr_night_visits, heart_rate, heartRateLow, heartRateHigh, gsr = self.parseM2File(inputFileM2,userId,startDate,investigatedPeriodinDays)                                                                                                    
        
            if(foundUserId>0):                                          
                self.nightMotion = nr_night_visits                
                self.visitsBathroom = nr_visits_bathroom                
                self.digitalTime = time_dit               
                self.heartRate = heart_rate #the Q2 value is considered
                self.heartRateLow = heartRateLow  # the number of events is considered              
                self.heartRateHigh = heartRateHigh # the number of events is considered              
                self.galvanicSkinResponse = gsr #the Q2 value is considered
        
                self.fuseUserInformation(outputFile,investigatedPeriodinDays)
                    
            else:              
                print 'The M2 data for user with id: ' + str(userId) + ' was not found.'
        else:
            print 'The M1 data for user with id: ' + str(userId) + ' was not found.'