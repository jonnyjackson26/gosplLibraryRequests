import requests
import re
import os
import time
import json

languages=[
    {"code":"eng","full-eng-title":"english"},
    {"code":"spa","full-eng-title":"spanish"},
    {"code":"fra","full-eng-title":"french"},
    {"code":"por","full-eng-title":"portugese"},
    {"code":"ita","full-eng-title":"italian"},
    {"code":"deu","full-eng-title":"german"},
]

numOfSectionsInDC= 138

def writeLinesToFile(lines, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            file.writelines(line for line in lines)

def getData(language,section):
    print(f"getting section {section} in {language}")
    url = f"https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang={language['code']}&uri=/scriptures/dc-testament/dc/{section}"

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()["content"]["body"].split("</div>", 1)[0]

        # Step 1: Remove page breaks
        cleaned_string = re.sub(r'<span\s+class="page-break"\s+data-page="\d+"></span>\n', '', json_data)
        # Step 2: Split the text by the verse number pattern
        verses = re.split(r'<span class="verse-number">\d+ </span>', cleaned_string)
        # Step 3: Remove footnotes (single letters between close and open angle brackets)
        verses = [re.sub(r'>[a-z]<', '><', verse) for verse in verses]
        # Step 4: Remove everything between and including < and >
        verses = [re.sub(r'<[^>]+>', '', verse) for verse in verses]


        #section 1's verse[0] starts with "Doctrine and Covenants\n". So I need to do a differnt case on the first one
        adjusterForFirstTimeThru=0
        if section=="1":
            adjusterForFirstTimeThru=1
        sectionIntro=verses[0].split("\n")[2+adjusterForFirstTimeThru]+"\n" #Revelation given through Joseph Smith the Prophet, on November 1, 1831, during a special conference of elders of the Church, hel
        verses[0]=sectionIntro

        verses[-1] = verses[-1][:-1] #remove the last new line so my txt file doesnt have an extra newline at the end
        
        #section breakdown
        pattern = r'<p class="study-summary".*?>(.*?)</p>'
        match = re.search(pattern, response.json()["content"]["body"], re.DOTALL)
        if match:
            summary_html = match.group(1)
            # Remove HTML tags from the content
            summary_text = re.sub(r'<.*?>', '', summary_html)
            verses.insert(1,f"{summary_text}\n")
            
        writeLinesToFile(verses,"dc2/dc-"+language["full-eng-title"]+"/"+str(section)+".txt")

    else:
        print("error in getting url")

def writeDC(language):
    getIntro(language)
    for i in range(1,numOfSectionsInDC+1):
        getData(language,str(i))
    getOD(language)

def getIntro(language):
    url = f"https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang={language['code']}&uri=/scriptures/dc-testament/introduction"

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()["content"]["body"].split("</div>", 1)[0]

        # Step 1: Remove page breaks
        cleaned_string = re.sub(r'<span\s+class="page-break"\s+data-page="\d+"></span>\n', '', json_data)
        # Step 2: Split the text by the verse number pattern
        verses = re.split(r'<span class="verse-number">\d+ </span>', cleaned_string)
        # Step 3: Remove footnotes (single letters between close and open angle brackets)
        verses = [re.sub(r'>[a-z]<', '><', verse) for verse in verses]
        # Step 4: Remove everything between and including < and >
        verses = [re.sub(r'<[^>]+>', '', verse) for verse in verses]
        writeLinesToFile(verses,"dc2/dc-"+language["full-eng-title"]+"/0.txt")
    else:
        print("error in getting url")

def getOD(language):
    for i in range(1,3):
        url = f"https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang={language['code']}&uri=/scriptures/dc-testament/od/{i}"

        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()["content"]["body"]

            # Step 1: Remove page breaks
            cleaned_string = re.sub(r'<span\s+class="page-break"\s+data-page="\d+"></span>\n', '', json_data)
            # Step 2: Split the text by the verse number pattern
            verses = re.split(r'<span class="verse-number">\d+ </span>', cleaned_string)
            # Step 3: Remove footnotes (single letters between close and open angle brackets)
            verses = [re.sub(r'>[a-z]<', '><', verse) for verse in verses]
            # Step 4: Remove everything between and including < and >
            verses = [re.sub(r'<[^>]+>', '', verse) for verse in verses]
            writeLinesToFile(verses,"dc2/dc-"+language["full-eng-title"]+"/od"+str(i)+".txt")
        else:
            print("error in getting url")


def main():
    start_time = time.time()
    #for language in languages:
    #    writeDC(language)
    writeDC(languages[0])
    end_time = time.time()
    print("Script execution time:", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()