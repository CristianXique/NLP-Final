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
    for row in reader:
        count+=1
        if count == 1:
            continue
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
print("within ten years: "+str((matches+tenOff)/count))
print("within twenty years: "+str((matches+tenOff+twentyOff)/count))
print("within thirty years: "+str((matches+tenOff+twentyOff+thirtyOff)/count))
print("within forty years: "+str((matches+tenOff+twentyOff+thirtyOff+fortyOff)/count))
print("within fifty years: "+str((matches+tenOff+twentyOff+thirtyOff+fortyOff+fiftyOff)/count))