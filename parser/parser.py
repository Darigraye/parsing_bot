import json
import re 
import requests
from parser.constants import *
from bs4 import BeautifulSoup
from datetime import date

def get_html_page():
    responce = requests.get(url, headers=headers)
    return responce.text if responce.status_code == 200 else None

def date_is_correct(checked_date):
    today = date.today()
    '''
        three flags to checking:
        <name>_is_eq: if year and month is equal we need check day
        <name>_is_gt: if year and/or month greater than current date result flag will be True
        <name>_day_flag: users can write date attributes sometimes. Therefore we need check 
        only first note
    '''
    month_is_eq, month_is_gt, first_moth_flag = False, False, True
    year_is_eq, year_is_gt, first_year_flag = False, False, True
    day_is_eq, day_is_gt, first_day_flag = False, False, True

    if isinstance(checked_date, str):                          
        list_words = re.split('[-]|[ ]|[—]|[–]', checked_date)

        for word in list_words:
            if word.isdigit() and len(word) == 4 and first_year_flag:
                year_is_gt = int(word) > today.year
                year_is_eq = int(word) == today.year
                first_year_flag = False
            elif word in months and first_moth_flag:
                month_is_gt = months[word] > today.month
                month_is_eq = months[word] == today.month
                first_moth_flag = False
            elif word.isdigit() and len(word) <= 2 and first_day_flag:
                day_is_gt = int(word) > today.day
                day_is_eq = int(word) == today.day
                first_day_flag = False

    return (day_is_eq or day_is_gt) and month_is_eq and year_is_eq or year_is_eq and month_is_gt or year_is_gt 

def get_information_line(line_data):
    information = dict()
    if re.search(r'(\<(/?[^>]+)>)', str(line_data.next_sibling)) or line_data.next_sibling == ' ':
        information[line_data.text] = 'TOO_MANY'
    else:
        information[line_data.text] = line_data.next_sibling
    return information

def get_hackathones():
    hackathones = list()
    hackathone = dict()
    text = get_html_page()
    soup = BeautifulSoup(text, "html.parser")

    all_events_href = soup.find_all('a', class_='js-product-link')
    for event in all_events_href:
        info_about_event = event.find(class_="t776__descr").find_all("strong")
        event_date = event.find(class_="t776__descr").find("strong").next_sibling
        #target_group = event.
        if date_is_correct(event_date):
            hackathone ['Имя'] = event.find(class_="t776__title").text.strip(' \n')
            for info in info_about_event:
                hackathone.update(get_information_line(info))
                print(info.next_sibling)
            hackathones.append(hackathone)
            hackathone = dict()
    return hackathones

def save_to_json():
    hackathones = get_hackathones()
    with open('json/saved_data.json', 'w', encoding='utf-8') as fd:
        json.dump(hackathones, fd, indent=4, ensure_ascii=False)

def _main():
    save_to_json()

if __name__ == '__main__':
    try:
        _main()
    except Exception as ex:
        print(str(ex))