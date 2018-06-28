import sys
import requests
from bs4 import BeautifulSoup as BS


##Create a dict of people with number, age, address, follow up link
def get_people():
    people = {}
    names = html.find_all(itemprop='name')

    ##This is duplicating because it is picking up both names with iemprop=names
    ##Change that somehow
    for i,name in enumerate(names):
        print(name)
        people[i] = {}
        people[i]["Name"] = name.string

    #for i,age in enumerate(list(html.find_all('strong'))):
    #    if age.string.strip() == "Age:":
    #            people[i]["Age"] = age.next_sibling


    for i, age in enumerate(list(html.find_all('tr'))):
        if i == 0:
            continue
        for x in age.descendants:
            try:

                if x.string.strip() == "Age:":
                    people[i]["Age"] = x.next_sibling
                    break
            except:
                continue

    for i, addr in enumerate(list(html.find_all('tr'))):
        if i == 0:
            continue
        for x in addr.descendants:
            try:

                if x.string.strip() == "Residential Address:":
                    people[i]["Address"] = x.next_sibling.next_sibling.next_sibling.string
                    break
            except:
                continue

    print(people)
##Get the name/state
'''
name = input("[+]Please input the name to search(ex. First M Last): ")
first = name.split()[0]

##Double check for this
middle = name.split()[1]

last = name.split()[2]
state = "OK"
'''
##Default variables
first = "James"
middle = "Lewis"
last = "Fowler"
state = "OK"

page = requests.get('https://voterrecords.com/voters/'+state+'/'+first+"+"+last+'/1')


html = BS(page.content, 'html.parser')


##Name
get_people()
