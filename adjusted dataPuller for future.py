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
#around 67000 is when most books seem to have their original publication listed
decadeCount = {}
decadeLabels = {}
paragraphNumbers = {}

label = 0
for i in range (1760,1980,10):
    decadeCount[int(i)]=0
    decadeLabels[int(i)]=label
    paragraphNumbers[int(i)]=0
    label+=1





earliestYear = 3000
latestYear = 0

'''
#used 5000
for i in range(bookNum-6000,bookNum-8000,-1):
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
                #
                
                #used with other if to get specific year (that might be underrepresented)
                #if(decade(year) != 1800):
                #   continue
                
                #

                #print(year+" "+language)
                if(int(year) < earliestYear):
                    earliestYear = int(year)
                if(int(year) > latestYear):
                    latestYear = int(year)
                
                #if(decade(year) not in decadeCount):
                #    decadeCount[decade(year)] = 0
                
                if(decadeCount[decade(year)] < 100):
                    years[i] = year
                    
                decadeCount[decade(year)]+=1
                
                #the other if mentioned before
                #if(decadeCount[1800] > 0):
                #   break
                
            
    time.sleep(0.1) #needed to not overwhelm gutenberg servers, which will result in your ip being banned


#These next two functions are to write to a tsv, so we don't have to redo data harvesting from the first half if the program breaks or is stopped in the second half
with open('saveDict_test_eval_revised_eval.tsv', 'w', newline='', encoding="utf-8") as file:
    counter = 1
    writer = csv.writer(file, delimiter='\t')
    
    for key in years:
        writer.writerow([key,years[key]])

'''

with open('saveDict_test_eval_revised_eval.tsv', 'r', newline='') as file:
    reader = csv.reader(file, delimiter='\t') 
    rowCount = 1
    for row in reader:
        print(rowCount)
        rowCount+=1
        years[row[0]] = row[1]
        decadeCount[decade(row[1])]+=1


with open('datasetTest_eval_HUGE_revised_final3.tsv', 'w', newline='', encoding="utf-8") as file:
    counter = 1
    writer = csv.writer(file, delimiter='\t')
    #writer.writerow(["textid","book #","year","label","title","text"])
    writer.writerow(["textid","target","text", "condition"])
    #writer.writerow(["label","text"])
    for key in years:

        if paragraphNumbers[decade(years[key])] >= 25:
            continue
        
        #response = requests.get("https://www.gutenberg.org/cache/epub/"+str(key)+"/pg"+str(key)+".txt")
        response = requests.get("https://www.gutenberg.org/cache/epub/"+str(key)+"/pg"+str(key)+".txt")
        
        

        if response.status_code == 200:
            text = response.text

        #clean_text = " ".join(text.split())
        clean_text = text
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
        #writer.writerow([key,decade(years[key]),clean_text, 1])
        place = 0
        new_clean_text = clean_text
        #upperBound = int(200/decadeCount[decade(years[key])])
        if(paragraphNumbers[decade(years[key])] < 25):
            for i in range(0,50):
                #new_clean_text = new_clean_text[place:]
                pos = new_clean_text.find("\r\n")
                paragraph = new_clean_text[:pos]
                #print (repr(new_clean_text))
                breakCount = 0
                while pos != -1 and breakCount < 1000:
                    #print(pos)
                    pos = new_clean_text.find("\r\n\r\n")
                    paragraph = new_clean_text[:pos]
                    new_clean_text = new_clean_text[pos+1:]
                    test_paragraph = " ".join(paragraph.split())
                    if(test_paragraph.count(" ")>350):
                        break
                    breakCount+=1
                
                #place = pos
                paragraph = " ".join(paragraph.split())
                if(paragraph.count(" ")>350):
                    paragraphNumbers[decade(years[key])]+=1
                    writer.writerow([key,decade(years[key]),paragraph, 1])
                    #writer.writerow([getDecadeLabel(decade(years[key])),paragraph])
                if paragraphNumbers[decade(years[key])] >= 25:
                    break

        
            
        print (counter)
        counter +=1
        time.sleep(0.1) #needed to not overwhelm gutenberg servers


    for key in years:

        if paragraphNumbers[decade(years[key])] >= 25:
            continue
        
        #response = requests.get("https://www.gutenberg.org/cache/epub/"+str(key)+"/pg"+str(key)+".txt")
        response = requests.get("https://www.gutenberg.org/cache/epub/"+str(key)+"/pg"+str(key)+".txt")
        
        

        if response.status_code == 200:
            text = response.text

        #clean_text = " ".join(text.split())
        clean_text = text
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
        #writer.writerow([key,decade(years[key]),clean_text, 1])
        place = 0
        new_clean_text = clean_text
        upperBound = int(200/decadeCount[decade(years[key])])
        if(paragraphNumbers[decade(years[key])] < 25):
            for i in range(0,2*upperBound):
                #new_clean_text = new_clean_text[place:]
                pos = new_clean_text.find("\r\n")
                paragraph = new_clean_text[:pos]
                #print (repr(new_clean_text))
                breakCount = 0
                while pos != -1 and breakCount < 1000:
                    #print(pos)
                    pos = new_clean_text.find("\r\n\r\n")
                    paragraph = new_clean_text[:pos]
                    new_clean_text = new_clean_text[pos+1:]
                    test_paragraph = " ".join(paragraph.split())
                    if(test_paragraph.count(" ")<350 and test_paragraph.count(" ")>25):
                        break
                    breakCount+=1
                
                #place = pos
                paragraph = " ".join(paragraph.split())
                if(paragraph.count(" ")<350 and paragraph.count(" ")>25):
                    paragraphNumbers[decade(years[key])]+=1
                    #writer.writerow([getDecadeLabel(decade(years[key])),paragraph])
                    writer.writerow([key,decade(years[key]),paragraph, 1])
                if paragraphNumbers[decade(years[key])] >= 25:
                    break

        
            
        print (counter)
        counter +=1
        time.sleep(0.1) #needed to not overwhelm gutenberg servers


print("number in English with publication date: " + str(count))
print("earliest year: "+str(earliestYear))
print("latest Year: "+str(latestYear))
for key in decadeCount:
    print(str(key) + " " + str(decadeCount[key]))
print()
for key in paragraphNumbers:
    print(str(key) + " " + str(paragraphNumbers[key]))
