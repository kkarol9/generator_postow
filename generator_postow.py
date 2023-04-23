import json
from bs4 import BeautifulSoup

import json
import openai

openai.api_key = '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'


# Load the HTML file
def web_scraping():
    with open('index2.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    dates = [span.text for span in soup.find_all("span", class_="pprofile-activity-tournament__date")]




    # Find all div elements with class="pprofile-activity-widget"
    activity_divs = soup.find_all('div', class_='pprofile-activity-widget')

    # Loop through the divs and extract the data
    data = []
    data2 = []
    for div in activity_divs:

        city = div.find('span', class_='pprofile-activity-widget__location pprofile-activity-widget__details-pair')
        city = city.text if city else ''

        nation = div.find('span', class_='pprofile-activity-widget__nation pprofile-activity-widget__details-pair')
        nation = nation.text if nation else ''

        tournament_type = div.find('span', class_='pprofile-activity-widget__tournament-type pprofile-activity-widget__details-pair')
        tournament_type = tournament_type.text if tournament_type else ''

        surface = div.find('span', class_='pprofile-activity-widget__surface')
        surface = surface.text if surface else ''

        draw = div.find('span', class_='pprofile-activity-widget__draw pprofile-activity-widget__details-pair')
        draw = draw.text if draw else ''

        type = div.find('span', class_='pprofile-activity-widget__type pprofile-activity-widget__details-pair')
        type = type.text if type else ''

        entry = div.find('span', class_='pprofile-activity-widget__entry pprofile-activity-widget__details-pair')
        entry = entry.text if entry else ''

        everything = []
        for s in div.find_all('div', class_='pprofile-activity-widget__results'):
            round = s.find('strong', class_='pprofile-activity-widget__round-label--mobile')
            round = round.text if round else ''

            win_lose = s.find('span', class_='pprofile-activity-widget__win-loss')
            win_lose = win_lose.text if win_lose else ''

            nationality = s.find('span', class_='pprofile-activity-widget__nationality')
            nationality = nationality.text if nationality else ''

            name_surname = s.find('span', class_='player-wrapper')
            name_surname = name_surname.text if name_surname else ''
                
            score = s.find('ol').text
            everything.append({'Round': round,'Win/lose' : win_lose, 'Nationality' : nationality, 'Name anad surname' : name_surname,
                                    'Score' : score})
        data2.append(everything)





        data.append({'City': city, 'Nation' : nation, 'Tournament type': tournament_type, 'Surface' : surface,
                    'Draw' : draw, 'Type' : type, 'Entry' : entry, 'Results' : everything})

    data.append(dates)
    return data



def post_gen(data):
    for i in range(len(data)-1):
        tab_wyniki = []
        text = ""

        tournament = data[i]
        # odczytanie wartości poszczególnych kluczy w słowniku
        city = tournament['City']
        nation = tournament['Nation']
        tournament_type = tournament['Tournament type']
        surface = tournament['Surface']
        draw = tournament['Draw']
        type = tournament['Type']
        entry = tournament['Entry']
        
        for result in tournament["Results"]:
            amount = len(tournament["Results"])
            round = result["Round"]
            win_lose = result["Win/lose"]
            nationality = result["Nationality"]
            name_and_surname = result["Name anad surname"]
            score = result["Score"]
            
            if round == "R1":
                score_text = "W pierwszej rundzie"
            elif round == "R2":
                score_text = "W drugiej rundzie"
            elif round == "QF":
                score_text = "W cwiercfinale"
            elif round == "SF":
                score_text = "W polfinale"
            elif round == "F":
                score_text = "W finale"

            if win_lose == "W":
                win_lose_text = " wygrałem z "
            elif win_lose == "L":
                win_lose_text = " przegralem z "

            text += score_text + win_lose_text + name_and_surname + "(" + nationality + ")" + score + ". "
            #tab_wyniki.append(text)
        
        
        prompt = f"Bylem w {city[11:]} w kraju {nation[8:]}, gdzie rozegralem {amount} mecz. {text}"
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # this is "ChatGPT" $0.002 per 1k tokens
        messages=[{"role": "user", "content": "Hej, czy pomożesz mi stworzyć post na facebooka podsumowujący mój udział w turnieju tenisowym? W kolejnym zdaniu masz informacje które mozesz wykorzystac do stworzenia postu" + prompt}]
        )

        reply_content = completion.choices[0].message.content
        print(reply_content)    



a = web_scraping()
b = post_gen(a)