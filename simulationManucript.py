import re
import random as r
import matplotlib.pyplot as plt
import math
import numpy as np
from decimal import Decimal 

plant1_g2s = []

plant2_g2s = []

plant1_g2e = []

plant2_g2e = []

plant1_seedNumber = []

plant2_seedNumber = []

plant1_d = []

plant2_d = []

plant1_germRate = []

plant2_germRate = []


def dormancyPeriod_calculator(self):
    idx = self.sDOY - 1 
    if self.plantType == 1:  # dormany time period
        self.dormancy = 25 # plant1_d[idx]

    elif self.plantType == 2:  # dormany time period
        self.dormancy = 26 # plant2_d[idx]

    else:
        raise Exception('Un-recognized plantType!')
    return self


def germ2startPeriod_calculator(self):
    idx = self.gDOY - 1 
    if self.plantType == 1:
        self.germ2start = plant1_g2s[idx]

    elif self.plantType == 2:
        self.germ2start = plant2_g2s[idx]

    else:
        raise Exception('Un-recognized plantType!')
    return self


def start2endPeriod_calculator(self):
    idx = self.gDOY - 1
    if self.plantType == 1:
        self.start2end = plant1_g2e[idx] - plant1_g2s[idx] + 1
        self.seedNumber = plant1_seedNumber[idx]

    elif self.plantType == 2:
        self.start2end = plant2_g2e[idx] - plant2_g2s[idx] + 1
        self.seedNumber = plant2_seedNumber[idx]

    else:
        raise Exception('Un-recognized plantType!')
    return self


def seedProduce_calculator(self, age):
    self.daySeedNumber = self.seedNumber * 42 / self.start2end
    return self


class Plant(object):
    # Define a plant.
    def __init__(self, startDOY, plantType, germRate): 
        self.plantType = plantType
        self.germRate = germRate
        self.DOY_now = (startDOY - 1) % 365 + 1 


class Colony(Plant): 
    # Define a plant population
    def __init__(self, startDOY, plantType, germRate, iniPlantNumber):
        Plant.__init__(self, startDOY, plantType, germRate)
        
        
        # 0-dormancy plantNumber,
        # 1-dormancy period,
        # 2-current days, 
        # 3-DOY
        self.dPlant = [] 
        
        
        # 0-germinated plantNumber, 
        # 1-germ2start period, 
        # 2-current days, 
        # 3-DOY
        self.gPlant = []

        
        # 0-flowering (giving seeds) plantNumber, 
        # 1-start2end period, 
        # 2-current days, 
        # 3-total seedNumber it can give, 
        # 4-DOY
        self.fPlant = []

        self.gDOY = self.DOY_now

        self = germ2startPeriod_calculator(self) 
        self.gPlant = [[iniPlantNumber, self.germ2start, 1, self.gDOY]]
    
   
    def getGerminate(self):
        return sum([c[0] for c in self.gPlant])

    
    def getFlower(self):
        return sum([c[0] for c in self.fPlant])

    
    def getDormancy(self):
        return sum([c[0] for c in self.dPlant])

    
    def destroy(self):
        self.gPlant = []
        self.fPlant = []

    def nextDay(self):
        flowerPlant_temp = []     
        germinatePlant_temp = []
        dormancyPlant_temp = []

        nextDOY = self.DOY_now % 365 + 1

        
        for i in range(len(self.dPlant)):   
                                            
            age = self.dPlant[i][2]
            if age >= self.dPlant[i][1]:
                self.gDOY = nextDOY
                self = germ2startPeriod_calculator(self) 
                germinatePlant_temp.append([self.dPlant[i][0], self.germ2start, 1, self.gDOY])
                # print self.plantType,self.dPlant[i][0],self.gDOY
            else:
                dormancyPlant_temp.append([self.dPlant[i][0], self.dPlant[i][1], self.dPlant[i][2] + 1, self.gDOY])

        
        seedNumber_temp = Decimal(0)
        for i in range(len(self.gPlant)):   # [plantNumber, period, current days, DOY]
                                            
            age = self.gPlant[i][2]
            if age >= self.gPlant[i][1]:
                self.gDOY = self.gPlant[i][3]
                self = start2endPeriod_calculator(self)
                flowerPlant_temp.append([self.gPlant[i][0], self.start2end, 1, self.seedNumber, self.gDOY])

                self = seedProduce_calculator(self, age)
                self.sDOY = nextDOY
                self = dormancyPeriod_calculator(self)
                seedNumber_temp = seedNumber_temp + Decimal(self.daySeedNumber) * Decimal(self.gPlant[i][0])
            else:
                germinatePlant_temp.append([self.gPlant[i][0], self.gPlant[i][1], self.gPlant[i][2] + 1, self.gDOY])

        
        for i in range(len(self.fPlant)):   # [0-plantNumber, 1-period, 2-current days, 3-total seedNumber, 4-DOY]
                                            
            age = self.fPlant[i][2]
            if age < self.fPlant[i][1]:
                self.seedNumber = self.fPlant[i][3]
                self.start2end = self.fPlant[i][1]
                self = seedProduce_calculator(self, age)
                self.sDOY = nextDOY
                self = dormancyPeriod_calculator(self)
                seedNumber_temp = seedNumber_temp + Decimal(self.daySeedNumber) * Decimal(self.fPlant[i][0])
                flowerPlant_temp.append([self.fPlant[i][0], self.fPlant[i][1], age + 1, self.fPlant[i][3], self.fPlant[i][4]])
            else:  # plant dies
                1
        
        
        germRate= 0
        grIdx = nextDOY - 1
        if self.plantType == 1:
            germRate = plant1_germRate[grIdx]

        elif self.plantType == 2:
            germRate = plant2_germRate[grIdx]

        tmp = seedNumber_temp * Decimal(germRate * 1) 
        seedNumber_temp = int(tmp)
        
        if seedNumber_temp > 0:
            dormancyPlant_temp.append([seedNumber_temp, self.dormancy, 1, 0])


        self.dPlant = dormancyPlant_temp
        self.gPlant = germinatePlant_temp
        self.fPlant = flowerPlant_temp
        self.DOY_now = nextDOY



def randomClear(clearCount, clearStartDay, clearEndDay, clearTime):
    tmp = []
    while (len(tmp) < clearCount):
        d = int(r.random() * (clearEndDay - clearStartDay) + clearStartDay)
        if (tmp.count(d) == 0):
            tmp.append(d)
    for t in tmp:
        clearTime.append(t)



def rangeRandomClear(dateRange, clearTime):
    date = []
    for i, j in dateRange.items():
        for d in range(i, j + 1):
            date.append(d)

    s = len(date)
    idx = int(r.random() * s)
    clearTime.append(date[idx])



def simulateClearMode():

    
    # plantType: 1 for WT, 2 for mutant
    plantType1, germRate1, iniPlantNumber1 = 1, 0, 10 
    plantType2, germRate2, iniPlantNumber2 = 2, 0, 10

    
    # startDOY: day of year when starting simulation 
    startDOY = 90
    daySimulate = 7300
    N_times_simulate = 1100


    with open("./20211027for2018-ratio1-clear1.txt", "w") as fnOut: 

        if N_times_simulate == 1:
            fnOut.write('DOY\t'
                        'p1d\tp1g\tp1f\tp1gf\tp1all\t'
                        'p2d\tp2g\tp2f\tp2gf\tp2all\t'
                        'gfRatio2\tallRatio2\n')
        else:
            fnOut.write('time\tgfRatio2\tallRatio2\tclearTime\n')

        
        for simulate_i in range(N_times_simulate):
            print(simulate_i) 

            # Mode 1: Certain time cleaning

            # clearTime = [0]


            # Mode 2
            
            # --------------- START ---------------
            # clearTime = [] 

            # randomClear(1, 141, 7389, clearTime)
            # randomClear(6, 366, 730, clearTime)

            # ---------------- END ----------------

            # Mode 3
            # --------------- START ---------------

            # startClearTime = 1096 
            # clearTime = [startClearTime + simulate_i, startClearTime + simulate_i + 365*2, startClearTime + simulate_i + 365*2*2, startClearTime + simulate_i + 365*2*3, startClearTime + simulate_i + 365*2*4, startClearTime + simulate_i + 365*2*5, startClearTime + simulate_i + 365*2*6, startClearTime + simulate_i + 365*2*7]
            

            # ---------------- END ----------------

            # Mode 4
            # --------------- START ---------------

            # clearTime = [] 
            # startClearTime = 1096 

            # randomClear(1, startClearTime + simulate_i -5, startClearTime + simulate_i +5, clearTime)
            # randomClear(1, startClearTime + simulate_i + 365*3 -5, startClearTime + simulate_i + 365*3 +5, clearTime)
            # randomClear(1, startClearTime + simulate_i + 365*3*2 -5, startClearTime + simulate_i + 365*3*2 +5, clearTime)
            # randomClear(1, startClearTime + simulate_i + 365*3*3 -5, startClearTime + simulate_i + 365*3*3 +5, clearTime)
            # randomClear(1, startClearTime + simulate_i + 365*3*4 -5, startClearTime + simulate_i + 365*3*4 +5, clearTime)
            
            

            # ---------------- END ----------------


            # Mode 5
            # --------------- START ---------------

            #clearTime = [] 
            # rangeRandomClear({149:215, 475:580, 840:945, 1205:1310, 1570:1675, 1935:2040, 2300:2405, 2665:2770, 3030:3135, 3395:3500}, clearTime)
            # rangeRandomClear({3760:3865, 4125:4230, 4490:4595, 4855:4960, 5220:5325, 5585:5690, 5950:6055, 6315:6420, 6680:6785, 7045:7150}, clearTime)

            # ---------------- END ----------------       

            print(clearTime) 

            # Simulate two colonys.
            
            colony1 = Colony(startDOY, plantType1, germRate1, iniPlantNumber1)
            colony2 = Colony(startDOY, plantType2, germRate2, iniPlantNumber2)

            plant1germ_list = []    
            plant2germ_list = []         

            plantNumber1_list = []  
            plantNumber2_list = []

            allNumber1_list = []    
            allNumber2_list = []


            for i in range(startDOY, daySimulate + startDOY):

                g1count = colony1.getGerminate()
                g2count = colony2.getGerminate()

                plant1germ_list.append(g1count)
                plant2germ_list.append(g2count)

                gf1count = g1count + colony1.getFlower()
                gf2count = g2count + colony2.getFlower()

                plantNumber1_list.append(gf1count)
                plantNumber2_list.append(gf2count)

                allNumber1_list.append(gf1count + colony1.getDormancy())
                allNumber2_list.append(gf2count + colony2.getDormancy())

                
                if i in clearTime:
                    colony1.destroy()   
                    colony2.destroy()

                colony1.nextDay()
                colony2.nextDay()

            if N_times_simulate == 1:
                curDOY = startDOY

                for i in range(len(allNumber1_list)):

                    totalPlant = plantNumber1_list[i] + plantNumber2_list[i]
                    totalAll = allNumber1_list[i] + allNumber2_list[i]
                    gfRatio2 = -1
                    if totalPlant != 0:
                        gfRatio2 = Decimal(plantNumber2_list[i]) * Decimal(1.0) / Decimal(totalPlant)
                    allRatio2 = -1
                    if totalAll != 0:
                        allRatio2 = Decimal(allNumber2_list[i]) * Decimal(1.0) / Decimal(totalAll)

                    fnOut.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%f\t%f\n" % (
                        curDOY,
                        allNumber1_list[i] - plantNumber1_list[i], plant1germ_list[i], plantNumber1_list[i] - plant1germ_list[i],
                        plantNumber1_list[i], allNumber1_list[i],
                        allNumber2_list[i] - plantNumber2_list[i], plant2germ_list[i], plantNumber2_list[i] - plant2germ_list[i],
                        plantNumber2_list[i], allNumber2_list[i],
                        gfRatio2, allRatio2
                    ))
                    curDOY += 1
            else:
                count = len(allNumber1_list) - 1
                totalPlant = plantNumber1_list[count] + plantNumber2_list[count]
                totalAll = allNumber1_list[count] + allNumber2_list[count]
                gfRatio2 = -1
                if totalPlant != 0:
                    gfRatio2 = Decimal(plantNumber2_list[count]) * Decimal(1.0) / Decimal(totalPlant)
                allRatio2 = -1
                if totalAll != 0:
                    allRatio2 = Decimal(allNumber2_list[count]) * Decimal(1.0) / Decimal(totalAll)

                fnOut.write("%d\t%f\t%f\t%s\n" % (
                        simulate_i,
                        gfRatio2, allRatio2,
                        clearTime
                    ))
        


simulateClearMode()
