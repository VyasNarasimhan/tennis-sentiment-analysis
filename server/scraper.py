import requests
from bs4 import BeautifulSoup

class ATP:
    
    def __init__(self):
        self.soup = BeautifulSoup(requests.get('https://www.atptour.com/en/rankings/singles').text, 'html.parser')

    def get_players(self):
        players = []
        rows = self.soup.find('table', attrs={'id': 'player-rank-detail-ajax'}).find('tbody').findAll('tr')
        for row in rows:
            data = row.findAll('td')
            players.append(
                {
                    'country_img': 'https://www.atptour.com' + data[2].div.div.img['src'], 
                    'country': data[2].div.div.img['alt'], 
                    'name': data[3].span.a.text.strip(),
                    'ranking': data[0].text.strip()
                }
            )
        return players
        
if __name__ == '__main__':
    atp = ATP()
    print(atp.get_players())