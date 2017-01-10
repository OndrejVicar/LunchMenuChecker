'''
Post lunch menu from chosen restaurants to Glip chat.
'''
from re         import search, findall, DOTALL, sub
from requests   import get, post
from json       import dumps
from datetime   import datetime
from bs4        import BeautifulSoup

day = datetime.today().weekday()
time = datetime.now().time()

#we are looking for next day menu after 14:30
if time.hour > 15:
    day += 1

#we will look for monday if it is saturday or sunday
if day == 5 or day == 6:
    day = 0

days_of_week = ['pondělí','úterý','středa','čtvrtek','pátek']

def GetMenuVarna():
    varna = dict()
    varna["Menu 1"] = dict()
    varna["Menu 2"] = dict()
    varna["Menu 3"] = dict()
    varna["Menu 4"] = dict()

    varna["url"] = "http://www.restauracevarna.cz/denni-menu/"
    varna["Name"] = "Varna Pivní Restaurace"
    varna["Info"] = "Polévka a bonaqua 0,25l v ceně, Menu 4 je bonusové menu"
    varna["Icon"] = "http://www.restauracevarna.cz/images/layout/logo.png"
    varna["CardPay"] = "Ano"

    r = get(varna["url"])
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "html5lib") #gets html code

    for date in soup.findAll('h2'):
        if days_of_week[day] in date.get_text():
            varna["Polévka"] = date.findNext("td").get_text().strip()

            varna["Menu 1"]["menu"] = date.findAllNext("td", {'class':'nazev'})[0].get_text().strip()
            varna["Menu 1"]["cena"] = date.findAllNext("td", {'class':'cena'})[0].get_text().strip()
            varna["Menu 2"]["menu"] = date.findAllNext("td", {'class':'nazev'})[1].get_text().strip()
            varna["Menu 2"]["cena"] = date.findAllNext("td", {'class':'cena'})[1].get_text().strip()
            varna["Menu 3"]["menu"] = date.findAllNext("td", {'class':'nazev'})[2].get_text().strip()
            varna["Menu 3"]["cena"] = date.findAllNext("td", {'class':'cena'})[2].get_text().strip()
            varna["Menu 4"]["menu"] = date.findAllNext("td", {'class':'nazev'})[3].get_text().strip()
            varna["Menu 4"]["cena"] = date.findAllNext("td", {'class':'cena'})[3].get_text().strip()

            #get numbers from Kč string
            varna["Menu 1"]["cena"] = int(search(r'\d+', varna["Menu 1"]["cena"]).group())
            varna["Menu 2"]["cena"] = int(search(r'\d+', varna["Menu 2"]["cena"]).group())
            varna["Menu 3"]["cena"] = int(search(r'\d+', varna["Menu 3"]["cena"]).group())
            varna["Menu 4"]["cena"] = int(search(r'\d+', varna["Menu 4"]["cena"]).group())
            break; #so we cant find more days

    return varna


def GetMenuBuddha():
    buddha = {"url":"http://www.indian-restaurant-buddha.cz/index.html"}
    buddha["Name"] = "Buddha Indická a Nepálská Restaurace"
    buddha["Info"] = "Příloha ke každému jídlu (v ceně): Tandoori Nan (indický chléb) / indická rýže Basmati / kombinace obou příloh. Polévka se podává zvlášť/soup is served separately from menu. (22 Kč)"
    buddha["Icon"] = "https://www.jidloted.cz/images/logos/11721.png"
    buddha["CardPay"] = "Ano"

    r = get(buddha["url"])
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html5lib") #gets html code
    menu = soup.findAll("p",{"class","textmenu"})

    soups = findall("</span>(.*?)22,",str(menu[:2]),DOTALL) #looks for soups for all week
    first_meals = findall("22,- Kč(.*?)95",str(menu[:2]),DOTALL) #looks for all meals
    menu_extracted = sub(r'[\t\n\r]','',str(menu).replace("<br/>", "")
                                                    .replace("&amp;", " a "))

    if(day == 0):
        menu_extracted_day =  findall("PONDĚLÍ(.*?)ÚTERÝ",menu_extracted,DOTALL) #onlz monday text
    elif(day == 1):
        menu_extracted_day =  findall("ÚTERÝ(.*?)STŘEDA",menu_extracted,DOTALL) #onlz monday text
    elif(day == 2):
         menu_extracted_day =  findall("STŘEDA(.*?)ČTVRTEK",menu_extracted,DOTALL) #onlz monday text
    elif(day == 3):
        menu_extracted_day = findall("ČTVRTEK(.*?)PÁTEK",menu_extracted,DOTALL) #onlz monday text


    buddha["Polévka"] = findall("Polévka:(.*?)22,- Kč",menu_extracted_day[0],DOTALL)[0]
    buddha["Menu 1"] = dict()
    buddha["Menu 1"]["menu"] = findall("22,- Kč(.*?)95,- Kč",menu_extracted_day[0],DOTALL)[0]
    buddha["Menu 1"]["cena"] = 95


    buddha["Menu 2"] = dict()
    buddha["Menu 2"]["menu"] = findall("95,- Kč(.*?)95,- Kč",menu_extracted_day[0],DOTALL)[0]
    buddha["Menu 2"]["cena"] = 95

    buddha["Menu 3"] = dict()
    buddha["Menu 3"]["menu"] = findall("VEG(.*?)95,-.*?Kč", menu_extracted_day[0], DOTALL)[0]
    buddha["Menu 3"]["cena"] = 95

    buddha["Menu 4"] = dict()
    buddha["Menu 4"]["menu"] = findall("(150g Mix Thali.*?)130,- Kč", menu_extracted_day[0], DOTALL)[0]
    buddha["Menu 4"]["cena"] = 130

    return buddha


def GetMenuOsmicka():
    osmicka = {"url":"http://www.naosmicce.cz/Menu.pdf"}
    osmicka["Name"] = "Bistro na Osmičce - Burger and Pasta"
    osmicka["Info"] = "Polévka dle denní nabídky je během doby poledního menu zahrnuta v ceně!"
    osmicka["Icon"] = "http://www.naosmicce.cz/img/logo.png"
    osmicka["CardPay"] = "Ne"

    r = get("https://www.menicka.cz/3840-bistro-na-osmicce.html")
    r.encoding = 'windows-1250'

    soup = BeautifulSoup(r.text, "html5lib") #gets html code
    menu = soup.findAll("div",{"class","menicka"})
    menu_extracted = sub(r'[\t\n\r]','',str(menu))

    if(day == 0):
        menu_extracted_day =  findall("Pondělí(.*?)Úterý",menu_extracted,DOTALL) #onlz monday text
    elif(day == 1):
        menu_extracted_day =  findall("Úterý(.*?)Středa",menu_extracted,DOTALL) #onlz monday text
    elif(day == 2):
         menu_extracted_day =  findall("Středa(.*?)Čtvrtek",menu_extracted,DOTALL) #onlz monday text
    elif(day == 3):
        menu_extracted_day = findall("Čtvrtek(.*?)Pátek",menu_extracted,DOTALL) #onlz monday text
    elif(day == 3):
        menu_extracted_day = findall("Pátek(.*?)Sobota",menu_extracted,DOTALL) #onlz monday text

    osmicka["Polévka"] = findall("Polévka:(.*?)<",menu_extracted_day[0],DOTALL)[0]
    osmicka["Veg polévka"] = findall("Vegetariánské menu:(.*?)<",menu_extracted_day[0],DOTALL)[0]

    osmicka["Menu 1"] = dict()
    osmicka["Menu 2"] = dict()
    osmicka["Menu 3"] = dict()

    menu_types = findall(r"\"nabidka_1\">(.*?)<",menu_extracted_day[0],DOTALL)

    if len(menu_types) > 3:
        osmicka["Menu 1"]["menu"] = menu_types[0] +  " " + menu_types[1]
        osmicka["Menu 2"]["menu"] = menu_types[2]
        osmicka["Menu 3"]["menu"] = menu_types[3]
    else:
        osmicka["Menu 1"]["menu"] = menu_types[0]
        osmicka["Menu 2"]["menu"] = menu_types[1]
        osmicka["Menu 3"]["menu"] = menu_types[2]

    osmicka["Menu 1"]["cena"] = findall(r"\"cena\">(.*?)<",menu_extracted_day[0],DOTALL)[0]
    osmicka["Menu 2"]["cena"] = findall(r"\"cena\">(.*?)<",menu_extracted_day[0],DOTALL)[1]
    osmicka["Menu 3"]["cena"] = findall(r"\"cena\">(.*?)<",menu_extracted_day[0],DOTALL)[2]

    return osmicka


def GetMenuGoldenNepal():
    GoldenNepal = {"url":"http://goldennepal.cz/"}
    GoldenNepal["Name"] = "Nepálská restaurace a bar"
    GoldenNepal["Info"] = "Ke každému jídlu ve všední den příloha rýže/placka/kombinace ZDARMA. Všechna jídla kromě Vindaloo, Jalfrezi, Madrasu a Falu obsahují smetanu. Všechny polévky obsahují mouku. KOrma obsahuje ořechy. Chicken Tikka Masala, Butter Chicken a Vindaloo obsahují barvivo."
    GoldenNepal["Icon"] = "http://goldennepal.cz/wp-content/uploads/2016/06/logotext.png"
    GoldenNepal["CardPay"] = "Ano"

    r = get("http://goldennepal.cz/denni-menu/")
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, "html5lib") #gets html code
    menu = soup.findAll("div",{"class","menu-list menu-list__dotted"})
    menu_extracted = sub(r'[\t\n\r]','',str(menu))

    if(day == 0):
        menu_extracted_day =  findall("Pondělí(.*?)Úterý",menu_extracted,DOTALL) #onlz monday text
    elif(day == 1):
        menu_extracted_day =  findall("Úterý(.*?)Středa",menu_extracted,DOTALL) #onlz monday text
    elif(day == 2):
         menu_extracted_day =  findall("Středa(.*?)Čtvrtek",menu_extracted,DOTALL) #onlz monday text
    elif(day == 3):
        menu_extracted_day = findall("Čtvrtek(.*?)Pátek",menu_extracted,DOTALL) #onlz monday text
    elif(day == 3):
        menu_extracted_day = findall("Pátek(.*?)Sobota",menu_extracted,DOTALL) #onlz monday text

    menu_courses = findall(r"content\">(.*?)</",menu_extracted_day[0],DOTALL)
    menu_prices = findall(r"price\">(.*?)</",menu_extracted_day[0],DOTALL)

    GoldenNepal["Polévka"] = menu_courses[0] + " " + menu_prices[0]

    GoldenNepal["Menu 1"] = dict()
    GoldenNepal["Menu 1"]["menu"] = menu_courses[1]
    GoldenNepal["Menu 1"]["cena"] = menu_prices[1]

    GoldenNepal["Menu 2"] = dict()
    GoldenNepal["Menu 2"]["menu"] = menu_courses[2]
    GoldenNepal["Menu 2"]["cena"] = menu_prices[2]

    GoldenNepal["Menu 3"] = dict()
    GoldenNepal["Menu 3"]["menu"] = menu_courses[3]
    GoldenNepal["Menu 3"]["cena"] = menu_prices[3]

    GoldenNepal["Menu 4"] = dict()
    GoldenNepal["Menu 4"]["menu"] = menu_courses[4]
    GoldenNepal["Menu 4"]["cena"] = menu_prices[4]

    return GoldenNepal


def PostMenu(menu_dict):


    body = menu_dict["url"] + "\n"
    body += menu_dict["Info"] + "\n"

    if "CardPay" in menu_dict.keys():
        body += "**Platba kartou:** " + menu_dict["CardPay"] + "\n"
    if "Polévka" in menu_dict.keys():
        body += "**Polévka:** " + menu_dict["Polévka"] + "\n"
    if "Menu 1" in menu_dict.keys():
        body += "**Menu 1:** " + menu_dict["Menu 1"]["menu"] + " - " + str(menu_dict["Menu 1"]["cena"]) + "\n"
    if "Menu 2" in menu_dict.keys():
        body += "**Menu 2:** " + menu_dict["Menu 2"]["menu"] + " - " + str(menu_dict["Menu 2"]["cena"]) + "\n"
    if "Menu 3" in menu_dict.keys():
        body += "**Menu 3:** " + menu_dict["Menu 3"]["menu"] + " - " + str(menu_dict["Menu 3"]["cena"]) + "\n"
    if "Menu 4" in menu_dict.keys():
        body += "**Menu 4:** " + menu_dict["Menu 4"]["menu"] + " - " + str(menu_dict["Menu 4"]["cena"]) + "\n"
    if "Menu 5" in menu_dict.keys():
        body += "**Menu 5:** " + menu_dict["Menu 5"]["menu"] + " - " + str(menu_dict["Menu 5"]["cena"]) + "\n"

    url = 'https://hooks.glip.com/webhook/0a6f78d2-cf25-49d5-aeae-25a10fbb6262' #Test conv
    #url = 'https://hooks.glip.com/webhook/feb6da0f-1cbe-4719-b0af-a1f0e871f885' #CASUAL: Oběd
    payload = \
    {
    'activity':menu_dict["Name"],
	'icon':menu_dict["Icon"],
	'body':body
    }

    headers = {'content-type': 'application/json'}
    response = post(url, data=dumps(payload), headers=headers)


PostMenu(GetMenuVarna())
PostMenu(GetMenuBuddha())
PostMenu(GetMenuOsmicka())
PostMenu(GetMenuGoldenNepal())