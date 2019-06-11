import scrapy
import re
from bs4 import BeautifulSoup
from player.items import PlayerItem

# This class define the spider class of scarpy classes
# It will start from the start_url and go deeper into the  crawlled url
# It inhrite the basic class scrapy Spider, and three variables have to be defined
# Name : The name of the spider
# Start_urls: The beginning webpage
# Parse: The method to define the parsing data  

class playerSpider(scrapy.Spider):
    # Define the name
    name = 'player'
    # The Start Url
    start_urls = [
        'https://www.transfermarkt.com/wettbewerbe/europa']

    def parse(self, response):
        # This Method parse the start url by beautifulsoup, then extract the url tag into tags
        # The top is the Premier League, then it yield the url and go to the next webpage  
        soup = BeautifulSoup(response.body, 'html.parser')
        tags = soup.find_all('a', href=re.compile(r'.*/startseite/wettbewerb/.*'))
        for tag in tags[:2]:
            url = re.findall(r'https://www.transfermarkt.com/.+', response.urljoin(tag.get('href')))
            if len(url) == 0:
                continue
            else:
                # Define the seasonal url
                new_url = url[0] + '/plus/?saison_id=2017'
                yield scrapy.Request(new_url, callback=self.parse1, dont_filter=True)

    def parse1(self, response):
        # This method get the information from the League webpages
        # This methon then parse the club web page and yield it to next step
        soup = BeautifulSoup(response.body, 'html.parser')
        all_info = dict()
        tags = soup.find_all('a', href=re.compile(r'.*/startseite/verein/.*'))
        for tag in tags:
            url = re.findall(r'https://www.transfermarkt.com/.+', response.urljoin(tag.get('href')))
            if len(url) == 0:
                continue
            else:
                new_url = url[0]
                print(new_url)
                yield scrapy.Request(new_url, callback=self.parseClub, meta={'all_info': all_info, 'url': new_url})

    def parseClub(self, response):
        # Parse the club information of the page
        soup = BeautifulSoup(response.body, 'html.parser')
        url = response.meta['url']
        club_detail = self.parse_club(soup, url)
        item = PlayerItem(club_information=club_detail)
        yield item

    def parse_club(self, soup, url):
        # This method is used to parse the club information webpage
        # The output is the club name, club id and players information in that club
        club_info = dict()
        name = soup.find('h1', itemprop='name').text.strip()
        club_info['name'] = name
        club_info['id'] = re.findall(r'verein/(.*)/saison_id', url)[0]
        players = []
        info = soup.find('div', {'id': 'yw1'}).find('tbody').find_all('td')
        length = int(len(info) / 9)
        for i in range(length):
            player_info = dict()
            player_info['player number'] = info[i * 9 + 0].text
            player_info['id'] = info[i * 9 + 1].find('a', {'class': 'spielprofil_tooltip'}).get('id')
            player_info['position'] = info[i * 9 + 4].text
            player_info['market value'] = info[i * 9 + 8].text.strip()
            players.append(player_info)
        club_info['detail'] = players
        return club_info


    def get_info(self, info):
        rep = {'\t': '', '\r': '', '#': '', ' ': '', '\xa0': ''}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        my_str = pattern.sub(lambda m: rep[re.escape(m.group(0))], info)
        info = my_str.split('\n')
        self.no_empty(info)
        return info

    def no_empty(self, l):
        while '' in l:
            l.remove('')

    def check_null(self, name, list):
        if name in list:
            result = list[list.index(name) + 1]
        else:
            result = 'null'
        return result