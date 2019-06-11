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
                yield scrapy.Request(new_url, callback=self.parsePlayer, meta={'all_info': all_info, 'url': new_url})

    def parsePlayer(self, response):
        # This methond get the parse the infomation from the club mainpage
        # Which is the club's players in the coresponding season, then 
        # This methon extract the name and id of player to go to their profile page
        soup = BeautifulSoup(response.body, 'html.parser')
        info = soup.find_all('a', href=re.compile(r'.*/profil/spieler/.*'))
        player = dict()
        for tag in info:
            name = re.findall(r'/(.*)/profil', tag.get('href'))[0]
            _id = re.findall(r'spieler/(.*)', tag.get('href'))[0]
            player[name] = _id
        all_info = response.meta['all_info']
        tags = []
        for key, value in player.items():
            tags.append('https://www.transfermarkt.com/' + key + '/profil/spieler/' + value)
        for tag in tags:
            yield scrapy.Request(tag, callback=self.parseProfile, meta={'all_info': all_info, 'url_info': player, 'url': tag})

    def parseProfile(self, response):
        # Parse the profile of the club player
        soup = BeautifulSoup(response.body, 'html5lib')
        url = response.meta['url']
        player_detail = self.parse_personal(soup, url)
        item = PlayerItem(player_perform=player_detail)
        yield item

    def parse_personal(self, soup, url):
        # This method is used to parse the player profile 
        # Output is a dictionary contain player name, plyer id, player url and player detail
        player = dict()
        detail = dict()
        if soup.find("div", {"class": "dataMarktwert"}) is None:
            market_value = 'null'
        else:
            market_value = re.findall(r'^(.*)\t\t\t\t\t', soup.find("div", {"class": "dataMarktwert"}).text.strip())[0]
        name = soup.find('h1', itemprop='name').text
        player['name'] = name
        player['id'] = re.findall(r'spieler/(.*)', url)[0]
        player['url'] = url
        content = self.get_info(soup.find_all("table", {"class": "auflistung"})[0].text.strip())
        detail['market_value'] = market_value
        detail['dob'] = self.check_null('DateofBirth:', content)
        detail['age'] = self.check_null('Age:', content)
        detail['height'] = self.check_null('Height:', content)
        detail['position'] = self.check_null('Position:', content)
        detail['citizenship'] = self.check_null('Citizenship:', content)
        detail['agent'] = self.check_null('PlayerAgent:', content)
        detail['current_club'] = self.check_null('Currentclub:', content)
        detail['join_time'] = self.check_null('Joined:', content)
        player['detail'] = detail
        return player

    def get_info(self, info):
        # Filter data with some newline symbol and error symbol 
        rep = {'\t': '', '\r': '', '#': '', ' ': '', '\xa0': ''}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        my_str = pattern.sub(lambda m: rep[re.escape(m.group(0))], info)
        info = my_str.split('\n')
        self.no_empty(info)
        return info

    def no_empty(self, l):
        # Filter the None Data
        while '' in l:
            l.remove('')

    def check_null(self, name, list):
        # Give the page with no detail with a null
        if name in list:
            result = list[list.index(name) + 1]
        else:
            result = 'null'
        return result