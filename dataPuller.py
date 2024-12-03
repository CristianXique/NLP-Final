import requests 
import csv
import time

def decade(year):
    year = int(year)
    decade = int(year/10) * 10
    return int(decade)

def checkDecadeCount(decadeCount):
    for key in decadeCount:
        
        if decadeCount[key] < 1:
            return False
    return True

count = 0
years = {}
titles = {}
bookNum = 74759
decadeCount = {}


for i in range (1760,1980,10):
    decadeCount[int(i)]=0





earliestYear = 3000
latestYear = 0



for i in range(bookNum-1475,bookNum-2000,-1):
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
                    continue
                #
                if(decade(year) != 1800):
                    continue
                #

                #print(year+" "+language)
                if(int(year) < earliestYear):
                    earliestYear = int(year)
                if(int(year) > latestYear):
                    latestYear = int(year)
                '''
                if(decade(year) not in decadeCount):
                    decadeCount[decade(year)] = 0
                '''
                if(decadeCount[decade(year)] < 1):
                    years[i] = year

                #
                decadeCount[decade(year)] = 1
                if(decadeCount[1800] > 0):
                    break
                #
            
    time.sleep(0.1)
            



with open('datasetTest5.tsv', 'w', newline='', encoding="utf-8") as file:
    counter = 1
    writer = csv.writer(file, delimiter='\t')
    #writer.writerow(["textid","book #","year","label","title","text"])
    writer.writerow(["textid","target","text", "condition"])
    for key in years:
        
        #response = requests.get("https://www.gutenberg.org/cache/epub/"+str(key)+"/pg"+str(key)+".txt")
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

        if "*** START OF" in clean_text:
            pos = clean_text.find("*** START OF")
            after = clean_text[pos+3:]
            startLoc = after.find("***")
            clean_text = after[startLoc+3:]

        if "*** END OF" in clean_text:
            pos = clean_text.find("*** END OF")
            clean_text = clean_text[:pos]
        
        #clean_text = clean_text[0:10]
        
        #writer.writerow([counter,key, years[key],decade(years[key]),title,clean_text])
        writer.writerow([key,decade(years[key]),clean_text, 1])
        counter = counter + 1
        time.sleep(0.1)


print("number in English with publication date: " + str(count))
print(earliestYear)
print(latestYear)
for key in decadeCount:
    print(str(key) + " " + str(decadeCount[key]))
