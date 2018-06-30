import sys
import requests
from bs4 import BeautifulSoup as BS
import random
import os

##Create a dict of people with number, age, address, follow up link
class Person:

    first_name: str = None
    middle_name: str = None
    last_name: str = None
    age: str = None
    state: str = None
    addr: str = None
    affil: str = None
    followUp: str = None

    def full_name(self):
        return " ".join([temp_name for temp_name in (self.first_name, self.middle_names, self.last_name) if temp_name])


    def set_name(self, input_string):
        input_string = input_string.split(" ")
        length = len(input_string)
        if length == 1:
            self.first_name = input_string[0]
        elif length == 2:
            self.first_name = input_string[0]
            self.last_name = input_string[0]
        else:
            self.first_name = input_string[0]
            self.last_name = input_string[-1]
            self.last_name = " ".join(input_string[1:])

    def __str__(self):
        attributes = [attr.capitalize() for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        values = [getattr(self, attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

        return_string = []
        for x in range(len(attributes)):
            attribute = attributes[x]
            value = values[x]
            if value:
                return_string.append("{}: {}".format(attribute, value))
        return_string = ", ".join(return_string)
        return return_string


##put the first middle last variables in a class

def get_people(main_person):

    people = []
    pageNum = 1
    max = 1
    while pageNum <= max:
        page = requests.get(get_url(main_person)+str(pageNum), get_UA())
        if int(page.status_code) != 200:
            sys.exit(('[!]Error, status code: ', page.status_code))
        html = BS(page.content, 'html.parser')

        tables = html.find_all('tr')
        for i, data in enumerate(tables):
            if i == 0 or data.find('ins'):
                continue
            person = Person()
            if data.find(itemprop='name'):
                person.set_name(data.find(itemprop='name').string)
            if data.find('strong'):
                person.age = data.find('strong').next_sibling
            if data.find(itemprop='address'):
                person.addr = data.find(itemprop='address').string
            if data.find(itemprop='affiliation'):
                person.affil = data.find(itemprop='affiliation').string
            if data.find(itemprop='url'):
                person.followUp = data.find(itemprop='url').get('href')


            people.append(person)
            #break
        if pageNum == 1:
            if html.find('div', id='PageBar'):
                max = int(html.find('div', id='PageBar').string.strip().split()[3])
            else:
                print(html)
                break
        pageNum += 1
        ##Sleep a random time to not seem robotic

    return people


def get_url(main_person):
    first = main_person.first_name
    middle = main_person.middle_name
    last = main_person.last_name
    state = main_person.state

    if state:
        state += "/"
        separator = "+"
    else:
        separator = "-"

    data = [temp_name for temp_name in (first, middle, last) if temp_name]
    name_stuff = separator.join(data)
    name_stuff += separator * (len(data) is 1 and name_stuff[-1] is not separator)
    url = 'https://voterrecords.com/voters/{}{}/'.format(state, name_stuff)
    return url

def get_UA():
    userAgents = [{'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/64.0.3282.119 Safari/537.36'},
    {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'},
    {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'},
    {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'},
    {'user-agent':'Opera 9.4 (Windows NT 6.1; U; en)'},
    {'user-agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/ Safari/530.5'},
    {'user-agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/6.0'},
    {'user-agent':'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'}]

    return userAgents[random.randint(0,len(userAgents)-1)]


def get_options(main_person):
    ##Required options
    output = {'First: ':main_person.first_name,
            'Last: ':main_person.last_name,
            'State: ':main_person.state}
    return output

def header():
    print("Super cool Header")

def main_menu():
    main_commands = {'help':'print help screen',
                    'set':'set a variable',
                    'unset':'reset a variable to None',
                    'use':'use a person',
                    'clear':'clear the screen',
                    'options':'show variables to set',
                    'run':'run the program',
                    'exit':'exit the program'}

    show_header = True
    main_person = Person()
    while True:
        if show_header:
            header()

        new_input = input("pyRecords>")
        new_input = new_input.lower()
        command = new_input.split()[0]
        options = new_input.split()[1:]
        #print(options)
        #print(command)
        if command not in main_commands:
            print("[!]That is not a command")


        if command == 'help':
            show_header = True
            print(header())
            ##look pretty
            for k, v in main_commands.items():
                print(k,":",v)


        ##Required variables
        if command == 'set':
            var = options[0]
            val = options[1]

            ##Have this iterate through a list of required variables returned be get_options
            ##Double check if the variable exists
            if var == 'first':
                main_person.first_name = val
            elif var == 'last':
                main_person.last_name = val
            elif var == 'state':
                main_person.state = val

        if command == 'unset':
            var = options[0]
            if var == 'first':
                main_person.first_name = None
            elif var == 'last':
                main_person.last_name = None
            elif var == 'state':
                main_person.state = None



        if command == 'use':
            ##integrate this into what is returned from get_people
            ##Go to the new followup link and scrape for real address and registration Date
            print("use person:", options[1])


        if command == 'options':
            ##Look pretty
            for k, v in get_options(main_person).items():
                print('{}:{}'.format(k, v))


        ##Check the set variables, if one is not set then continue
        if command == 'run':
            people = get_people(main_person)
            for i,x in enumerate(people):
                print('{}:[*]{}\n\
                            [*]Age:{}\n\
                            [*]Location{}\n'.format(i, x.full_name(), x.age, x.addr))
            #print(get_url(main_person))

        if command == 'clear':
            ##check on windows or linux
            os.system('clear')
            show_header = True
            continue

        if command == 'exit':
            sys.exit()

        show_header = False

#def get_more():
    ##Pull more info from the their page
    ##Real address
    ##Relativse
    ##Reg date

##Get the name/state
main_menu()
