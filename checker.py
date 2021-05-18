#!/usr/bin/python

import os, sys  # system imports
import bs4, requests, smtplib, time
from datetime import datetime, timedelta
from pydub import AudioSegment as AS
from pydub.playback import play

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ALARM_SOUND = AS.from_wav(
    os.path.join(CURRENT_DIR, 'alarm.wav')
)
ALARM_LENGTH = 15 * 1000  # in milliseconds

NHS_URL = 'https://www.nhs.uk/conditions/coronavirus-covid-19/coronavirus-vaccination/coronavirus-vaccine/'
TEXT_TEMPLATES = [
    'people aged {} and over',
    'people who will turn {} before 1 July 2021'
]
DEFAULT_AGE = 35  # in years
DEFAULT_TIMER = 15  # in minutes


def scraper(AGE=DEFAULT_AGE):
    page = requests.get(NHS_URL)
    page.raise_for_status()  # stop if errors

    # Parse text for sections
    parsed_page = bs4.BeautifulSoup(page.text, 'html.parser')
    section = parsed_page.find(id='suitability').parent

    # Find the list items
    requirements = section.find_next('ul').find_all('li')
    for req in requirements:
        if req.text.lower() in [tpl.format(AGE) for tpl in TEXT_TEMPLATES]:
            play(ALARM_SOUND[:ALARM_LENGTH])
            break;            

if __name__ == '__main__':
    age = DEFAULT_AGE
    if len(sys.argv) == 2:
        age = int(sys.argv[1])

    while 1:
        print('[{}] > Checking...'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        sleep = DEFAULT_TIMER - datetime.now().minute % DEFAULT_TIMER  # checks every DEFAULT_TIMER minutes
        if sleep == DEFAULT_TIMER:
            scraper(age)
        time.sleep(DEFAULT_TIMER * 60)

