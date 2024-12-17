import requests 
import csv
import time

def decade(year):
    year = int(year)
    decade = int(year/10) * 10
    return int(decade)

def checkDecadeCount(decadeCount):
    for key in decadeCount:
        
        if decadeCount[key] <= 20:
            return False
    return True

def getDecadeLabel(decade):
    return decadeLabels[int(decade)]

count = 0
years = {}
titles = {}
bookNum = 74836
#around 67000 is when most books seem to start have their original publication listed
decadeCount = {}
decadeLabels = {}

label = 0
for i in range (1760,1980,10):
    decadeCount[int(i)]=0
    decadeLabels[int(i)]=label
    label+=1




#check range of years
earliestYear = 3000
latestYear = 0

#used -0 to -6000 to train, -6000 to -7500 for evaluate
for i in range(bookNum-6001,bookNum-7500,-1):
    print(-(i-bookNum))
    response = requests.get("https://www.gutenberg.org/ebooks/"+str(i))

    if checkDecadeCount(decadeCount) == True:
        print("we're breaking, boss")
        break


    #print(response.status_code)
    if response.status_code == 200:
        text = response.text
    
    pos = text.find("<th>Language</th>")
    after = text[pos:]
    languageLoc = after.find("</td>")
    language = after[languageLoc-7:languageLoc]
    language = language.lower()
    
    if language == "english":
        
        if "Original Publication" in text:
            count = count + 1
            pos = text.find("Original Publication")
            after = text[pos:]
            yearLoc = after.find("</td>")
            #realized some books have the year the were originally published and the year they were reprinted; for the sake of convenience, we can just ignore these
            checkReprint = after[:yearLoc]
            if "reprint" not in checkReprint.lower():
                
                year = after[yearLoc-6:yearLoc-2]
                if(not year.isdigit()):
                    print("year is not number: " + str(year))
                    continue
                if(decade(year) not in decadeCount):
                    print("not in decadeCount")
                    continue
                
                
               

                #print(year+" "+language)
                if(int(year) < earliestYear):
                    earliestYear = int(year)
                if(int(year) > latestYear):
                    latestYear = int(year)
                
                
                
                if(decadeCount[decade(year)] <= 60):
                    years[i] = year
                    
                decadeCount[decade(year)]+=1
                
                
                
            
    time.sleep(0.1) #needed to not overwhelm gutenberg servers, which will result in your ip being banned


#These next two functions are to write to a tsv, so we don't have to redo data harvesting from the first half if the program breaks or is stopped in the second half
with open('saveDict_test_eval.tsv', 'w', newline='', encoding="utf-8") as file:
    counter = 1
    writer = csv.writer(file, delimiter='\t')
    
    for key in years:
        writer.writerow([key,years[key]])


with open('saveDict_test_eval.tsv', 'r', newline='') as file:
    reader = csv.reader(file, delimiter='\t') 
    rowCount = 1
    for row in reader:
        print(rowCount)
        rowCount+=1
        years[row[0]] = row[1]

with open('datasetTest_eval_HUGE.tsv', 'w', newline='', encoding="utf-8") as file:
    counter = 1
    writer = csv.writer(file, delimiter='\t')

    #comment in or our depending on what kind of data you need
    #writer.writerow(["textid","book #","year","label","title","text"]) 
    writer.writerow(["textid","target","text", "condition"]) #evaluate data
    #writer.writerow(["label","text"]) #training data
    for key in years:
        
        #gets the plain text page
        response = requests.get("https://www.gutenberg.org/cache/epub/"+str(key)+"/pg"+str(key)+".txt")
        
        

        if response.status_code == 200:
            text = response.text

        clean_text = " ".join(text.split())
        #content = text.replace("\n", " ")
        title = "ERROR"
        pos1 = clean_text.find("Title: ")
        pos2 = clean_text.find("Author: ")
        #print(str(pos1)+" "+str(pos2))
        title= clean_text[pos1+7:pos2]

        #two if find the start and end and crop the text to be only that
        if "*** START OF" in clean_text:
            pos = clean_text.find("*** START OF")
            after = clean_text[pos+3:]
            startLoc = after.find("***")
            clean_text = after[startLoc+3:]

        if "*** END OF" in clean_text:
            pos = clean_text.find("*** END OF")
            clean_text = clean_text[:pos]
        
        #clean_text = clean_text[0:10]

        #same thing as before, comment in or out, make sure lines up with the header
        #writer.writerow([counter,key, years[key],decade(years[key]),title,clean_text])
        writer.writerow([key,decade(years[key]),clean_text, 1]) #evaluate data
        #writer.writerow([getDecadeLabel(decade(years[key])),clean_text]) #training data
        
        print (counter)
        counter +=1
        time.sleep(0.1) #needed to not overwhelm gutenberg servers

#final count at the end to see how many were found from each decade
print("number in English with publication date: " + str(count))
print("earliest year: "+str(earliestYear))
print("latest Year: "+str(latestYear))
for key in decadeCount:
    print(str(key) + " " + str(decadeCount[key]))
