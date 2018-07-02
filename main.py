import sys
import requests
from bs4 import BeautifulSoup as BS
import random
import os
from fake_useragent import UserAgent

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

    ##Gets populated when more_info is called
    relatives: list = None
    neighbors: list = None

    def full_name(self):
        return " ".join([temp_name for temp_name in (self.first_name, self.middle_name, self.last_name) if temp_name])


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
        ##Capture the cookies and set them
        page = requests.get(get_url(main_person)+str(pageNum), headers={'User-Agent':ua.random}, allow_redirects=True)
        if int(page.status_code) != 200:
            sys.exit('[!]Error, status code: {}'.format(page.status_code))
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
            if html.find('div', id='PageBar').string:
                max = int(html.find('div', id='PageBar').string.strip().split()[3])
            else:
                break
        pageNum += 1
        ##Sleep a random time to not seem robotic
        time.sleep(random.randInt(0,5))

    return people

def more_info(target):
    ##Scrape neighbors, relatives, reg date,
    page = requests.get('https://voterrecords.com/'+target.followUp, headers={'User-Agent':ua.random}, allow_redirects=True)

    if int(page.status_code) != 200:
        sys.exit('[!]Error, status code: {}'.format(page.status_code))
    html = BS(page.content, 'html.parser')

    neighbors = html.find_all('tr', itemprop='relatedTo')
    for i, data in enumerate(tables):
    ##Neighbors
        target.relatives.append()



    ##Parse more data

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


def get_options(main_person):
    ##Required options
    ##Optional options
    ##Max queries
    output = {'First':main_person.first_name,
            'Last':main_person.last_name,
            'State':main_person.state}

    return output

def header():
    print("Super cool Header")

def main_menu():
    main_commands = {'help':'print help screen',
                    'set':'set a variable',
                    'unset':'reset a variable to None',
                    'use':'use a person',
                    'clear':'clear the screen',
                    'options':'show variables',
                    'run':'run the program',
                    'exit':'exit the program'}

    usage = {'help': 'help [command]',
            'set': 'set [variable] [value]',
            'unset': 'unset [variable]',
            'use': 'use [number]',
            'clear': 'clear',
            'options': 'options',
            'run': 'run',
            'exit': 'exit'}

    show_header = True
    main_person = Person()
    while True:
        if show_header:
            header()

        new_input = input("pyRecords>")
        new_input = new_input.lower()
        command = new_input.split()[0]
        options = new_input.split()[1:]
        if command not in main_commands:
            print("[!]Not a valid command: {}".format(command))

        if command == 'help':
            if options:
                if options[0] in main_commands:
                    print('\tUsage: {}'.format(usage[options[0]]))
                    show_header = False
                    continue
                else:
                    print('[!]Not a valid command: {}'.format(options[0]))

            show_header = True
            header()
            ##look pretty
            print("\tCommand\tDescription")
            print("\t-------\t-----------")
            for k, v in main_commands.items():
                print("\t{}\t {}".format(k, v))

        ##Required variables
        if command == 'set':
            if len(options) <= 0:
                print("[!]Please enter a variable name")
                continue
            elif len(options) <2:
                print("[!]Please enter a value")
                continue
            var = options[0]
            val = options[1]

            ##Have this iterate through a list of required variables returned be get_options
            ##Double check if the variable exists
            vars = [x.lower() for x in list(get_options(main_person).keys())]
            if var in vars:
                ##I dont like how this is done
                if var == 'first':
                    main_person.first_name = val
                elif var == 'last':
                    main_person.last_name = val
                elif var == 'state':
                    if val not in available_states:
                        print("[!]Not a valid state: {}".format(var))
                        print("[*]Available states: {}".format(", ".join(available_states)))
                    main_person.state = val
            else:
                print("[!]Not a valid variable: {}".format(var))

        if command == 'unset':
            var = options[0]
            if var in vars:
                if var == 'first':
                    main_person.first_name = None
                elif var == 'last':
                    main_person.last_name = None
                elif var == 'state':
                    main_person.state = None
            else:
                print("[!]Not a valid variable: {}".format(var))



        if command == 'use':
            ##Go to the new followup link and scrape for real address and registration Date
            print("use person:", options[1])


        if command == 'options':
            ##Look pretty
            print('\tName\tCurrent value\tDescription')
            print('\t----\t-------------\t-----------')
            for k, v in get_options(main_person).items():
                if k == "First":
                    desc = "First name of the target"
                elif k == "Last":
                    desc = "Last name of the target"
                if k == 'State':
                    desc = "State of the target"
                    desc += ' List of available states: {}'.format(", ".join(available_states))
                print('\t{}\t{}\t\t{}'.format(k, v, desc))


        ##Check the set variables, if one is not set then continue
        if command == 'run':
            if None in get_options(main_person).values():
                print("[!]Set all variables before running")
                continue

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

##Get the name/state
if __name__ == "__main__":
    ua = UserAgent()
    available_states = ['ak', 'ar', 'co', 'ct', 'de', 'fl', 'mi', 'nv', 'nc', 'oh', 'ok', 'ri', 'ut', 'wa']
    main_menu()
