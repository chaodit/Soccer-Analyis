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
            yield scrapy.Request(tag, callback=self.parsePerform, meta={'all_info': all_info, 'url_info': player, 'url': tag})

    def parsePlayer(self, response):
    # Go to the Player Performance in Premier League
        soup = BeautifulSoup(response.body, 'html.parser')
        info = soup.find_all('a', href=re.compile(r'.*/profil/spieler/.*'))
        player = dict()
        for tag in info:
            name = re.findall(r'/(.*)/profil', tag.get('href'))[0]
            _id = re.findall(r'spieler/(.*)', tag.get('href'))[0]
            player[name] = _id
        all_info = response.meta['all_info']
        tags = []
        year = '2017'
        for key, value in player.items():
            tags.append('https://www.transfermarkt.com/' + key + '/leistungsdaten/spieler/' + value +'/plus/0?saison=' + year)
        for tag in tags:
            yield scrapy.Request(tag, callback=self.parsePerform, meta={'all_info': all_info, 'url_info': player, 'url': tag})
    
    def parsePerform(self, response):
        # Parse the profile of the club player performance
        soup = BeautifulSoup(response.body, 'html5lib')
        url = response.meta['url']
        player_detail = self.parse_perform(soup, url)
        item = PlayerItem(player_perform=player_detail)
        yield item

    def parse_perform(self, soup, url):
        # This method is used to parse the player performance pages
        # The output is player name, player id, player url and player perform detail
        player = dict()
        player_performance = dict()
        info = soup.find('div',{'id':'yw2'}).find_all('td')
        name = soup.find('h1', itemprop='name').text
        player['name'] = name
        player['id'] = re.findall(r'spieler/(.*)/plus', url)[0]
        player['url'] = url
        for i in range(len(info)):
            if (info[i].img is not None and info[i].img.get('title') == "Premier League"):
                if(i+9 < len(info) and info[i+9].text.replace('\'','').replace('.','').isdigit()):
                    player_performance['league'] = info[i].img.get('title')
                    player_performance['match_plays'] = info[i + 2].text
                    player_performance['goal'] = info[i + 3].text
                    player_performance['yellow_card'] = info[i + 4].text
                    player_performance['second_yellow_card'] = info[i + 5].text
                    player_performance['red_card'] = info[i + 6].text
                    player_performance['conceded goal'] = info[i + 7].text
                    player_performance['clean sheets'] = info[i + 8].text
                    player_performance['minutes played'] = info[i + 9].text
                else:
                    player_performance['league'] = info[i].img.get('title')
                    player_performance['match_plays'] = info[i + 2].text
                    player_performance['goal'] = info[i + 3].text
                    player_performance['assist'] = info[i + 4].text
                    player_performance['yellow_card'] = info[i + 5].text
                    player_performance['second_yellow_card'] = info[i + 6].text
                    player_performance['red_card'] = info[i + 7].text
                    player_performance['minutes played'] = info[i + 8].text
        player['detail'] = player_performance
        return player

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
