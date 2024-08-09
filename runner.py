import requests
import re
import os
import time

books = [
    {"numOfChapters": 1, "title": "title", "uri": "bofm-title", "isTitlePage":True},
    {"numOfChapters": 1, "title": "introduction", "uri": "introduction", "isTitlePage":True},
    {"numOfChapters": 1, "title": "three", "uri": "three", "isTitlePage":True},
    {"numOfChapters": 1, "title": "eight", "uri": "eight", "isTitlePage":True},
    {"numOfChapters": 1, "title": "js", "uri": "js", "isTitlePage":True},
    {"numOfChapters": 22, "title": "1-nephi", "uri": "1-ne", "isTitlePage":False},
    {"numOfChapters": 33, "title": "2-nephi", "uri": "2-ne", "isTitlePage":False},
    {"numOfChapters": 7, "title": "jacob", "uri": "jacob", "isTitlePage":False},
    {"numOfChapters": 1, "title": "enos", "uri": "enos", "isTitlePage":False},
    {"numOfChapters": 1, "title": "jarom", "uri": "jarom", "isTitlePage":False},
    {"numOfChapters": 1, "title": "omni", "uri": "omni", "isTitlePage":False},
    {"numOfChapters": 1, "title": "words-of-mormon", "uri": "w-of-m", "isTitlePage":False},
    {"numOfChapters": 29, "title": "mosiah", "uri": "mosiah", "isTitlePage":False},
    {"numOfChapters": 63, "title": "alma", "uri": "alma", "isTitlePage":False},
    {"numOfChapters": 16, "title": "helaman", "uri": "hel", "isTitlePage":False},
    {"numOfChapters": 30, "title": "3-nephi", "uri": "3-ne", "isTitlePage":False},
    {"numOfChapters": 1, "title": "4-nephi", "uri": "4-ne", "isTitlePage":False},
    {"numOfChapters": 9, "title": "mormon", "uri": "morm", "isTitlePage":False},
    {"numOfChapters": 15, "title": "ether", "uri": "ether", "isTitlePage":False},
    {"numOfChapters": 10, "title": "moroni", "uri": "moro", "isTitlePage":False}
]

languages=[
    {"code":"deu","full-eng-title":"german"},
    {"code":"eng","full-eng-title":"english"},
    {"code":"spa","full-eng-title":"spanish"},
    {"code":"fra","full-eng-title":"french"},
    {"code":"por","full-eng-title":"portugese"},
    {"code":"ita","full-eng-title":"italian"},
]


def writeLinesToFile(lines, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            file.writelines(line for line in lines)

def getData(language,book,chapter):
    if(book["isTitlePage"]):
        base_url = "https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang={}&uri=/scriptures/bofm/{}"
    else:
        base_url = "https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang={}&uri=/scriptures/bofm/{}/{}"  #https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang=spa&uri=/scriptures/bofm/1-ne/5
    url = base_url.format(language["code"], book["uri"], chapter) 
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
        
        pattern = r"(Chapter|Capítulo|Kapitel|Chapitre) \d+"
        verses[0] = re.sub(pattern, "", verses[0])
        #verses[0] has a chapter desciption but it also contains book description and other stuff. this removes "Chapter X" thats also includded

        #verses=verses[1:] #get rid of chapter description
        #verses[0]=verses[0].split("\n")[2]+"\n" #this line of code sometimes shows the chapter description, sometimes not

        writeLinesToFile(verses,"bom2/bom-"+language["full-eng-title"]+"/"+book["title"]+"/"+chapter+".txt")
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

def writeBOM(language):
    for book in books:
        for chapter in range(1, int(book["numOfChapters"])+1):
            getData(language,book,str(chapter))

def main():
    start_time = time.time()
    for lang in languages:
        writeBOM(lang)
    end_time = time.time()
    print("Script execution time:", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()