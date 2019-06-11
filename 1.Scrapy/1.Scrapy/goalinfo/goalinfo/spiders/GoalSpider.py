import scrapy
import re
from bs4 import BeautifulSoup
from goalinfo.items import GoalinfoItem

# This class define the spider class of scarpy classes
# It will start from the start_url and go deeper into the  crawlled url
# It inhrite the basic class scrapy Spider, and three variables have to be defined
# Name : The name of the spider
# Start_urls: The beginning webpage
# Parse: The method to define the parsing data  

class GoalSpider(scrapy.Spider):
    name = 'goal'
    start_urls = [
        'https://www.transfermarkt.com/wettbewerbe/europa']

    def parse(self, response):
        # This Method parse the start url by beautifulsoup, then extract the url tag into tags
        # The top is the Premier League, then it yield the url and go to the next webpage  
        soup = BeautifulSoup(response.body, 'html5lib')
        tags = soup.find_all('a', href=re.compile(r'.*/startseite/wettbewerb/.*'))
        for tag in tags[:2]:
            url = re.findall(r'https://www.transfermarkt.com/.+', response.urljoin(tag.get('href')))
            if len(url) == 0:
                continue
            else:
                new_url = url[0] + '/plus/?saison_id=2017'
                yield scrapy.Request(new_url, callback=self.parse1, dont_filter=True)

    def parse1(self, response):
        # This method get the information from the League webpages
        # This methon then parse the club web page and yield it to next step
        soup = BeautifulSoup(response.body, 'html.parser')
        tags = soup.find_all('a', href=re.compile(r'.*/startseite/verein/.*'))
        for tag in tags:
            url = re.findall(r'https://www.transfermarkt.com/.+', response.urljoin(tag.get('href')))
            if len(url) == 0:
                continue
            else:
                new_url = url[0].replace('/2018', '/2017')
                yield scrapy.Request(new_url, callback=self.parse2)

    def parse2(self, response):
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
        tags = []
        for key, value in player.items():
            tags.append('https://www.transfermarkt.com/' + key + '/alletore/spieler/' + value +
                        '/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/minute/0/torart/0/plus/1')
        for tag in tags:
            yield scrapy.Request(tag, callback=self.parseGoal, meta={'url_info': player, 'url': tag})

    def parseGoal(self, response):
        #Parse the goal detail of the players
        soup = BeautifulSoup(response.body, 'html.parser')
        url = response.meta['url']
        goal_info = self.parse_goal(soup, url)
        item = GoalinfoItem(goal_information=goal_info)
        yield item

    def check_null(self, name, list):
        if name in list:
            result = list[list.index(name) + 1]
        else:
            result = 'null'
        return result

    # Parse the goal information
    def parse_goal(self, soup, url):
        goal_detail = self.creat_detail(soup, url)
        if soup.find('div', {'class': 'responsive-table'}) is None:
            goal_detail['detail'] = None
            return goal_detail
        else:
            goal_info = soup.find('div', {'class': 'responsive-table'}).find_all('tr')
            tag = 'border-top:1px dotted red  !important;'
            season_goal = []
            header = 'https://www.transfermarkt.com/'
            season = []
            previous = dict()
            isleague = 15
            for i in range(1, (len(goal_info) - 1)):
                goal = dict()
                if goal_info[i].get('style') == tag:
                    season.append(goal_info[i].text.strip())
                elif len(goal_info[i].find_all('td')) == 1:
                    continue
                elif len(goal_info[i].find_all('td')) == 5:
                    goal['season'] = previous['season']
                    goal['league_name'] = previous['league_name']
                    goal['match_day'] = previous['match_day']
                    goal['date'] = previous['date']
                    goal['vanue'] = previous['vanue']
                    goal['host_url'] = previous['host_url']
                    goal['guest_url'] = previous['guest_url']
                    goal['guest_name'] = previous['guest_name']
                    goal['result'] = previous['result']
                    goal['position'] = previous['position']
                    goal['goal_minute'] = goal_info[i].find_all('td')[1].text
                    goal['at_point'] = goal_info[i].find_all('td')[2].text
                    goal['type_of_goal'] = goal_info[i].find_all('td')[3].text
                    goal['provider'] = goal_info[i].find_all('td')[4].text
                    if goal['provider'] == '':
                        goal['provider_id'] = 'null'
                    else:
                        goal['provider_id'] = goal_info[i].find_all('td')[4].a.get('id')
                    season_goal.append(goal)
                elif len(goal_info[i].find_all('td')) == isleague:
                    goal['season'] = re.findall(r'Season (.*)', season[len(season) - 1])[0]
                    goal['league_name'] = goal_info[i].find_all('td')[1].text.strip()
                    goal['match_day'] = goal_info[i].find_all('td')[2].text.strip()
                    goal['date'] = goal_info[i].find_all('td')[3].text
                    goal['vanue'] = goal_info[i].find_all('td')[4].text
                    goal['host_url'] = header + goal_info[i].find_all('td')[5].a.get('href')
                    goal['guest_url'] = header + goal_info[i].find_all('td')[7].a.get('href')
                    goal['guest_name'] = goal_info[i].find_all('td')[8].text
                    goal['result'] = goal_info[i].find_all('td')[9].text
                    goal['position'] = goal_info[i].find_all('td')[10].text
                    goal['goal_minute'] = goal_info[i].find_all('td')[11].text
                    goal['at_point'] = goal_info[i].find_all('td')[12].text
                    goal['type_of_goal'] = goal_info[i].find_all('td')[13].text
                    goal['provider'] = goal_info[i].find_all('td')[14].text
                    if goal['provider'] == '':
                        goal['provider_id'] = 'null'
                    else:
                        goal['provider_id'] = goal_info[i].find_all('td')[14].a.get('id')
                    season_goal.append(goal)
                    previous = goal
                else:
                    goal['season'] = re.findall(r'Season (.*)', season[len(season) - 1])[0]
                    goal['league_name'] = goal_info[i].find_all('td')[1].text.strip()
                    goal['match_day'] = goal_info[i].find_all('td')[2].text.strip()
                    goal['date'] = goal_info[i].find_all('td')[3].text
                    goal['vanue'] = goal_info[i].find_all('td')[4].text
                    goal['host_url'] = header + goal_info[i].find_all('td')[5].a.get('href')
                    goal['guest_url'] = header + goal_info[i].find_all('td')[6].a.get('href')
                    goal['guest_name'] = goal_info[i].find_all('td')[7].text
                    goal['result'] = goal_info[i].find_all('td')[8].text
                    goal['position'] = goal_info[i].find_all('td')[9].text
                    goal['goal_minute'] = goal_info[i].find_all('td')[10].text
                    goal['at_point'] = goal_info[i].find_all('td')[11].text
                    goal['type_of_goal'] = goal_info[i].find_all('td')[12].text
                    goal['provider'] = goal_info[i].find_all('td')[13].text
                    if goal['provider'] == '':
                        goal['provider_id'] = 'null'
                    else:
                        goal['provider_id'] = goal_info[i].find_all('td')[13].a.get('id')
                    season_goal.append(goal)
                    previous = goal
            goal_detail['detail'] = season_goal
            return goal_detail

    def no_empty(self,l):
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

    def creat_detail(self, soup, url):
        name = soup.find('h1', itemprop='name').text
        _id = re.findall(r'.*/alletore/spieler/(.*)/saison', url)[0]
        detail = dict()
        detail['name'] = name
        detail['id'] = _id
        detail['url'] = url
        return detail

