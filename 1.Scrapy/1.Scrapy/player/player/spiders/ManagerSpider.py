import scrapy
import re
from bs4 import BeautifulSoup
from SoccerScrapy.items import SoccerscrapyItem


class ManagerSpider(scrapy.Spider):
    name = 'soccer'
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
        url = soup.find('a', href=re.compile(r'.*/profil/trainer/.*')).get('href')
        manager = dict()
        name = re.findall(r'/(.*)/profil/trainer/.*', url)[0]
        _id = re.findall(r'.*/profil/trainer/(.*)', url)[0]
        manager[name] = _id
        all_info = response.meta['all_info']
        tags = []
        for key, value in manager.items():
            tags.append('https://www.transfermarkt.com/' + key + '/profil/trainer/' + value)
        for tag in tags:
            yield scrapy.Request(tag, callback=self.parse_manager_detail, meta={'all_info': all_info, 'url_info': player, 'url': tag})

    def parse_manager_detail(self, response):
        # This method parse the manager information
        # The output is manager name, manager id and manager detail
        soup = BeautifulSoup(response.body, 'html5lib')
        content = soup.find_all('table', {'class': 'items'})[0].find_all('tr')
        url = response.meta['url']
        manager_content = self.creat_detail(soup,url)
        header = 'https:\\www.transfermarkt.com'
        manager = []
        for i in range(len(content)):
            detail = dict()
            info = content[5].find_all('td')
            detail['club_url'] = header + info[0].a.get('href')
            detail['club_name'] = info[1].text.strip()
            detail['appointed'] = info[2].text.strip()
            detail['in_charge_until'] = info[3].text.strip()
            detail['days_in_charge'] = info[4].text.strip()
            detail['position'] = info[5].text.strip()
            detail['matches'] = info[6].text.strip()
            detail['win'] = info[7].text.strip()
            detail['d'] = info[8].text.strip()
            detail['lose'] = info[9].text.strip()
            detail['player_used'] = info[10].text.strip()
            detail['total_goals'] = info[11].text.strip()
            detail['ppm'] = info[12].text.strip()
            manager.append(detail)
        manager_content['detail'] = manager
        item = SoccerscrapyItem(manager_detail_content=manager_content)
        yield item
    
     def check_null(self, name, list):
        if name in list:
            result = list[list.index(name) + 1]
        else:
            result = 'null'
        return result
    
    def no_empty(self, l):
        while '' in l:
            l.remove('')

    def get_info(self, info):
        rep = {'\t': '', '\r': '', '#': '', ' ': '', '\xa0': ''}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        my_str = pattern.sub(lambda m: rep[re.escape(m.group(0))], info)
        info = my_str.split('\n')
        self.no_empty(info)
        return info
