import scrapy
import re
from bs4 import BeautifulSoup
from SoccerScrapy.items import SoccerscrapyItem


class InjurySpider(scrapy.Spider):
    name = 'injury'
    start_urls = [
        'https://www.transfermarkt.com/wettbewerbe/europa']

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html5lib')
        tags = soup.find_all('a', href=re.compile(r'.*/startseite/wettbewerb/.*'))
        for tag in tags[:10]:
            url = re.findall(r'https://www.transfermarkt.com/.+', response.urljoin(tag.get('href')))
            if len(url) == 0:
                continue
            else:
                yield scrapy.Request(url[0], callback=self.parse1, dont_filter=True)

    def parse1(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        all_info = dict()
        league = self.parse_league(soup)
        all_info['league'] = league
        tags = soup.find_all('a', href=re.compile(r'.*/startseite/verein/.*'))
        for tag in tags:
            url = re.findall(r'https://www.transfermarkt.com/.+', response.urljoin(tag.get('href')))
            if len(url) == 0:
                continue
            else:
                new_url = url[0].replace('/2018', '/2015')
                yield scrapy.Request(new_url, callback=self.parse2, meta={'all_info': all_info})

    def parse2(self, response):
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
            tags.append('https://www.transfermarkt.com/' + key + '/verletzungen/spieler/' + value)
        for tag in tags:
            yield scrapy.Request(tag, callback=self.parseInjury, meta={'all_info': all_info, 'url_info': player, 'url': tag})
    
    def parseInjury(self, response):
        # Parse the injury information of each Player
        soup = BeautifulSoup(response.body, 'html.parser')
        all_info = response.meta['all_info']
        url = response.meta['url']
        injury_info = self.injury_info(soup, url)
        all_info['injury_info'] = injury_info
        item = SoccerscrapyItem(injury_information=all_info['injury_info'])
        yield item

    def injury_info(self, soup, url):
        # Parse the injury detail of the injury page
        # Outputput is the injury detail of each season
        injury_detail = self.creat_detail(soup, url)
        if soup.find('tbody') is None:
            injury_detail['detail'] = None
            print('No Injury Information !')
            return injury_detail
        else:
            injury_info = soup.find('tbody').find_all('tr')
            all_injury = []
            for i in range(len(injury_info)):
                detail = dict()
                injury = []
                for item in injury_info[i].children:
                    injury.append(item.string)
                detail['season'] = injury[1]
                detail['injury_name'] = injury[2]
                detail['start_time'] = injury[3]
                detail['end_time'] = injury[4]
                detail['last_days'] = injury[5]
                all_injury.append(detail)
            injury_detail['detail'] = all_injury
            return injury_detail

    def creat_detail(self, soup, url):
        name = soup.find('h1', itemprop='name').text
        _id = re.findall(r'spieler/(.*)/page', url)[0]
        detail = dict()
        detail['name'] = name
        detail['id'] = _id
        detail['url'] = url
        return detail