from bs4 import BeautifulSoup
import requests
import datetime

date_today = datetime.datetime.today()
URL = 'https://www.catholic.org/bible/daily_reading/'

def get_reading(book,chapter,verse_nos,verses_nos,i):
    if verse_nos.count('-') >= 1:
        filename = 'https://bible-api.com/' + book + "+" + chapter + ":" + verse_nos
        verse_nos_count = verse_nos.split('-')
        verse_nos_count = int(verse_nos_count[1]) - int(verse_nos_count[0]) + 1
    else:
        filename = 'https://bible-api.com/' + book + " " + chapter + ":" + verse_nos
        verse_nos_count = 0

    try:
        response = requests.get(filename)
        response.raise_for_status()
        data = response.json()
        # print(data)
        # print(x)
        if x == 0:
            file_entry = f"{book} {chapter}: {verses_nos}"
            write_to_file(file_entry)
            print(f"{book} {chapter}: {verses_nos}")
        if verse_nos_count > 1:
            for i in range(verse_nos_count):
                verse_no = data['verses'][i]['verse']
                verse = data['verses'][i]['text'].replace('\n',' ')
                file_entry = f'{verse_no} {verse}'
                write_to_file(file_entry)
                print(f'{verse_no} {verse}')
        else:
            verse = data['verses'][0]['text'].replace('\n', ' ')
            file_entry = f"{data['verses'][0]['verse']} {verse}"
            write_to_file(file_entry)
            print(data['verses'][0]['verse'],data['verses'][0]['text'].replace('\n',' '))

    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        print('please try again')
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        print('please try again')
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        print('please try again')
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)
        print('please try again')
    else:
        pass


def write_to_file(file_entry):
    with open('DailyBibleReadings.txt', 'a') as file:
        file.write(file_entry)
        file.write('\n')

#########Start of program#############

while True:
    response = requests.get(URL)
    result = response.text
    soup = BeautifulSoup(result, 'html.parser')
    reading = soup.findAll('em')
    # print(reading[1].text.split())
    if len(reading[1].text.split()) > 2:
        break

if date_today.weekday() == 6:
    len_em = 5
else:
    len_em = 4

readings_today = {}

for i in range(1,len_em):
    reading_split = reading[i].text.split()
    # print(reading_split)
    chapter = reading_split[1].split(':')
    reading_split[1] = chapter[0]
    reading_split.insert(2,chapter[1])
    # print(reading_split)
    readings_today[i] = reading_split
print("Today's Bible Readings")
write_to_file(date_today.strftime('%A %B %d, %Y'))
print(date_today.strftime('%A %B %d, %Y'))

#single verse
# URL1 = 'https://bible-api.com/john%203:16'

#verse range
# URL2 = 'https://bible-api.com/romans+12:1-2'

#multiple ranges
# URL3 = 'https://bible-api.com/romans%2012:1-2,5-7,9,13:1-10' #
reading_ctr = 0
for reading in readings_today.values():
    URL_bible_api = 'https://bible-api.com/'
    book = reading[0]
    chapter = reading[1]
    verses_list = reading[2:]
    if reading_ctr == 0:
        print('\nFirst Reading')
    elif reading_ctr == 1:
        print('\nResponsorial Psalm')
    elif reading_ctr == 2:
        print ('\nGospel')
    else:
        print('\nSecond Reading')

    if len(verses_list) > 1:
        verses_nos = ""
        for verse in verses_list:
            if verse.count(',') > 0:
                verses_nos += verse
            else:
                verses_nos += verse + ","
        verses_nos = verses_nos[:-1]
        x = 0
        for verse in verses_list:
            if verse.count(',') > 0:
                verse = verse[:-1]
            # print(verse)
            get_reading(book,chapter,verse,verses_nos,x)
            x += 1
    else:
        x = 0
        verse= verses_list[0]
        verses_nos = verse
        get_reading(book,chapter,verse,verses_nos,x)
    reading_ctr += 1
print('Done')