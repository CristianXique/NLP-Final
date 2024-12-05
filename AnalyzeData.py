import csv
import math

with open('finalOutput_HUGE.tsv', 'r', newline='') as file:
    
    reader = csv.reader(file, delimiter='\t') 
    count = 0
    matches = 0
    tenOff = 0
    twentyOff = 0
    thirtyOff = 0
    fortyOff = 0
    fiftyOff = 0

    totalPerDecade = {}
    rightPerDecade = {}
    predictedPerDecade = {}

    for i in range (1760,1980,10):
        totalPerDecade[i]=0
        rightPerDecade[i]=0
        predictedPerDecade[i]=0

    for row in reader:
        count+=1
        if count == 1:
            continue
        
        totalPerDecade[int(row[1])]+=1
        predictedPerDecade[int(row[4])]+=1
        
        if row[1] == row[4]:
            rightPerDecade[int(row[1])]+=1



        if row[1] == row [4]:
            matches+=1
        if abs(int(row[1])-int(row[4]))==10:
            tenOff+=1
        if abs(int(row[1])-int(row[4]))==20:
            twentyOff+=1
        if abs(int(row[1])-int(row[4]))==30:
            thirtyOff+=1
        if abs(int(row[1])-int(row[4]))==40:
            fortyOff+=1
        if abs(int(row[1])-int(row[4]))==50:
            fiftyOff+=1

    

   
        

        

print("total evaluated: "+str(count))
print("exact matches: "+str(matches/count))
print("within 10 years: "+str((matches+tenOff)/count))
print("within 20 years: "+str((matches+tenOff+twentyOff)/count))
print("within 30 years: "+str((matches+tenOff+twentyOff+thirtyOff)/count))
print("within 40 years: "+str((matches+tenOff+twentyOff+thirtyOff+fortyOff)/count))
print("within 50 years: "+str((matches+tenOff+twentyOff+thirtyOff+fortyOff+fiftyOff)/count))

for key in totalPerDecade:
    if(totalPerDecade[key] != 0 and predictedPerDecade[key] != 0):
        if((rightPerDecade[key]/totalPerDecade[key]+rightPerDecade[key]/predictedPerDecade[key])!=0):
            recall = rightPerDecade[key]/totalPerDecade[key]
            precision = rightPerDecade[key]/predictedPerDecade[key]
            print("f1 score of "+str(key)+": "+str(2*((precision*recall)/(precision+recall))))
