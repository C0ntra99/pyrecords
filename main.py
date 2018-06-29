import sys
import requests
from bs4 import BeautifulSoup as BS


##Create a dict of people with number, age, address, follow up link
class Person:

    def __init__(self, name=None, age=None, addr=None, affil=None, url=None):
        self.name = name
        self.age = age
        self.addr = addr
        self.affil = affil
        self.url = url

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.name, self.age, self.addr, self.affil, self.url)


def get_people():

    people = []
    pageNum = 1
    max = 1
    while pageNum <= max:
        page = requests.get('https://voterrecords.com/voters/'+state+'/'+first+"+"+last+'/'+str(pageNum))
        html = BS(page.content, 'html.parser')

        tables = html.find_all('tr')
        for i, data in enumerate(tables):
            if i == 0 or data.find('ins'):
                continue
            person = Person()
            if data.find(itemprop='name'):
                person.name = data.find(itemprop='name').string
            if data.find('strong'):
                person.age = data.find('strong').next_sibling
            if data.find(itemprop='address'):
                person.addr = data.find(itemprop='address').string
            if data.find(itemprop='affiliation'):
                person.affil = data.find(itemprop='affiliation').string
            if data.find(itemprop='url'):
                person.url = data.find(itemprop='url').get('href')


            people.append(person)
            #break
        if pageNum == 1:
            max = int(html.find('div', id='PageBar').string.strip().split()[3])
        pageNum += 1

    return people
#def get_more():
    ##Pull more info from the their page
    ##Real address
    ##Relativse
    ##Reg date

##Get the name/state
'''
name = input("[+]Please input the name to search(ex. First M Last): ")
first = name.split()[0]

##Double check for this
middle = name.split()Non[1]

last = name.split()[2]
state = "OK"
'''
##Default variables
first = "James"
middle = "Lewis"
last = "Fowler"
state = "OH"




people = get_people()
for i,x in enumerate(people):
    print(i+1,":",x)
