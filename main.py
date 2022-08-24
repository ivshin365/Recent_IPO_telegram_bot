import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import telegram

from datetime import datetime

TOKEN = '5625171905:AAGLhNKR2a2Iq0OiyaAlcl-JATek6_dEDa8'
bot = telegram.Bot(TOKEN)
url = 'https://www.iposcoop.com/last-12-months'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


# Extracting the table
def extracting_table():
    main_table = soup.find(class_='standard-table')
    table_body = main_table.find('tbody')
    temp_rows = table_body.find_all('tr')
    return temp_rows


ipo_list = []


# Getting a list of recent IPO'S
def get_ipo_list():
    ipo_list.clear()
    rows = extracting_table()
    for row in rows:
        ticker = row.find_all('td')[1].get_text()
        return_percent = row.find_all('td')[8].get_text()
        offer_date = row.find_all('td')[3].get_text().strip()
        new_return = return_percent.strip("%")
        change_percent = int(float(new_return))
        if change_percent > 100:
            ipo_item = {
                'Ticker': ticker,
                'Return': return_percent,
                'offer_date': offer_date
            }
            ipo_list.append(ipo_item)
    df = pd.DataFrame(ipo_list)
    try:
        bot.send_message(chat_id="@ipo_watchlist", text=f'<pre>{df}</pre>',
                        parse_mode=telegram.ParseMode.HTML)
        print(df)
    except:
        print("some error")


while True:
    extracting_table()
    time.sleep(5)
    get_ipo_list()
    time.sleep(60)
