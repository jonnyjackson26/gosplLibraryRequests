import requests
import re
import os
import threading

books = [
    {"numOfChapters": 22, "title": "1 Nephi", "uri": "1-ne"},
    {"numOfChapters": 33, "title": "2 Nephi", "uri": "2-ne"},
    {"numOfChapters": 7, "title": "Jacob", "uri": "jacob"},
    {"numOfChapters": 1, "title": "Enos", "uri": "enos"},
    {"numOfChapters": 1, "title": "Jarom", "uri": "jarom"},
    {"numOfChapters": 1, "title": "Omni", "uri": "omni"},
    {"numOfChapters": 1, "title": "Words of Mormon", "uri": "w-of-m"},
    {"numOfChapters": 29, "title": "Mosiah", "uri": "mosiah"},
    {"numOfChapters": 63, "title": "Alma", "uri": "alma"},
    {"numOfChapters": 16, "title": "Helaman", "uri": "hel"},
    {"numOfChapters": 30, "title": "3 Nephi", "uri": "3-ne"},
    {"numOfChapters": 1, "title": "4 Nephi", "uri": "4-ne"},
    {"numOfChapters": 9, "title": "Mormon", "uri": "morm"},
    {"numOfChapters": 15, "title": "Ether", "uri": "ether"},
    {"numOfChapters": 10, "title": "Moroni", "uri": "moro"}
]


def writeLinesToFile(lines, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            file.writelines(line for line in lines)

def getData(language,book,chapter):
    base_url = "https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang={}&uri=/scriptures/bofm/{}/{}"  #https://www.churchofjesuschrist.org/study/api/v3/language-pages/type/content?lang=spa&uri=/scriptures/bofm/1-ne/5
    url = base_url.format(language, book, chapter) 
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
        verses=verses[1:] #get rid of chapter description
        #verses[0]=verses[0].split("\n")[2]+"\n" #this line of code sometimes shows the chapter description, sometimes not

        writeLinesToFile(verses,"bom_"+language+"/"+book+"/"+chapter+".txt")
    else:
        print("Failed to retrieve data. Status code:", response.status_code)





def main():
    threads = []
    for book in books:
        for chapter in range(1, book["numOfChapters"]):
            thread = threading.Thread(target=getData, args=("spa", book["uri"], chapter))
            threads.append(thread)
            thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()