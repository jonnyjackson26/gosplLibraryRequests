import requests
import re
import os
import time
import json

languages=[
    #{"code":"eng","full-eng-title":"english"},
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
    url = f"https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang={language['code']}&uri=/scriptures/dc-testament/dc/{section}"
    print(url)

    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()["content"]["body"].split("</div>", 1)[0]

        #remove page breaks, sometimes it gives u weird page break
        cleaned_string = re.sub('<span\s+class="page-break"\s+data-page="\d+"></span>\n', '', json_data)
        # Remove footnotes (single letters between close and open angle brackets)
        cleaned_string = re.sub('>[a-z]<', '><', cleaned_string)
        # Remove everything between < and >
        cleaned_string = re.sub('<[^>]+>', '', cleaned_string)
        
        # Split the text into a list of verses based on the verse number pattern, and remove the numbers
        verses = re.split('\d+ ', cleaned_string)

        print(verses[0])

        #section 1's verse[0] starts with "Doctrine and Covenants\n". So I need to do a differnt case on the first one
        adjusterForFirstTimeThru=0
        if section=="1":
            adjusterForFirstTimeThru=1
        sectionIntro=verses[0].split("\n")[2+adjusterForFirstTimeThru]+"\n" #Revelation given through Joseph Smith the Prophet, on November 1, 1831, during a special conference of elders of the Church, hel
        verses[0]=sectionIntro

        verses[-1] = verses[-1][:-1] #remove the last new line so my txt file doesnt have an extra newline at the end
        writeLinesToFile(verses,"dc/dc-"+language["full-eng-title"]+"/"+str(section)+".txt")

    else:
        print("error in getting url")

def writeDC(language):
    for i in range(1,numOfSectionsInDC+1):
        getData(language,str(i))

def main():
    start_time = time.time()
    #for language in languages:
    #    writeDC(language)
    getData(languages[0],"1")
    getData(languages[0],"2")
    getData(languages[0],"3")
    getData(languages[0],"4")
    getData(languages[0],"5")
    getData(languages[0],"6")
    getData(languages[0],"7")
    end_time = time.time()
    print("Script execution time:", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()