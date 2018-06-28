##Scrap from voterrecords.com
import scrapy

class voterScraper(scrapy.Spider):

    def __init__(self):
        ##Make these variables you need to set in the module later
        ##Age
        self.name = input('[+]Please enter name(ex. First M Last): ')
        self.state = input('[+]Please enter the state(ex. OK): ')
        self.first = self.name.split()[0]
        self.middle = self.name.split()[1]
        self.last = self.name.split()[2]

        if self.middle:
            self.url = 'https://voterrecords.com/voters/'+self.state+'/'+self.first+'+'+self.middle+'+'+self.last+'/1'
        else:
            self.url = 'https://voterrecords.com/voters/'+self.state+'/'+self.first+'+'+self.last+'/1'

        self.parse(self.url)

    def get_page(self):

    def parse(self, response):
        page = response.url.split("/")[-2]
        print(page)

    def getInfo(self):
        print("Get age")
    def main_menu(self):
        print("<ain menu")
        #while True:
