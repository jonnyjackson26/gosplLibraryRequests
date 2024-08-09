import requests
import re
import os
import time

books = [
    {"numOfChapters": 22, "title": "1-nephi", "uri": "1-ne"},
    {"numOfChapters": 33, "title": "2-nephi", "uri": "2-ne"},
    {"numOfChapters": 7, "title": "jacob", "uri": "jacob"},
    {"numOfChapters": 1, "title": "enos", "uri": "enos"},
    {"numOfChapters": 1, "title": "jarom", "uri": "jarom"},
    {"numOfChapters": 1, "title": "omni", "uri": "omni"},
    {"numOfChapters": 1, "title": "words-of-mormon", "uri": "w-of-m"},
    {"numOfChapters": 29, "title": "mosiah", "uri": "mosiah"},
    {"numOfChapters": 63, "title": "alma", "uri": "alma"},
    {"numOfChapters": 16, "title": "helaman", "uri": "hel"},
    {"numOfChapters": 30, "title": "3-nephi", "uri": "3-ne"},
    {"numOfChapters": 1, "title": "4-nephi", "uri": "4-ne"},
    {"numOfChapters": 9, "title": "mormon", "uri": "morm"},
    {"numOfChapters": 15, "title": "ether", "uri": "ether"},
    {"numOfChapters": 10, "title": "moroni", "uri": "moro"}
]

languages=[
    {"code":"eng","full-eng-title":"english"},
    {"code":"spa","full-eng-title":"spanish"},
    {"code":"fra","full-eng-title":"french"},
    {"code":"por","full-eng-title":"portugese"},
    {"code":"ita","full-eng-title":"italian"},
    {"code":"deu","full-eng-title":"german"},
]


def writeLinesToFile(lines, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            file.writelines(line for line in lines)

def getData(language,book,chapter):
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
        
        pattern = r"Chapter \d+"
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