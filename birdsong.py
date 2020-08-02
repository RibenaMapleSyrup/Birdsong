import requests
import time
from bs4 import BeautifulSoup
from playsound import playsound
from ebird.api import get_observations
import inspect
import re
import json
from random import randrange
import sched
api_key = 'insert your key here'

class birds:
    def __init__(self, queue, past_observations, update):
        self.queue = queue
        self.past_observations = past_observations
        self.update = update

def song(species):
    url = "https://ebird.org/species/" + species + ".html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    script = soup.find('script', text=re.compile('audioAssetsJson'))
    json_text = re.search("^\s*var audioAssetsJson =(.*^};)", 
              script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    json_text = json_text[:-1]
    data = json.loads(json_text)
    Id = data['galleryAssets'][0]['asset']['assetId']
    url2 = "https://download.ams.birds.cornell.edu/api/v1/asset/" + str(Id)
    playsound(url2)


def birdwatch(name):
    todays_birds.update = get_observations(api_key, 'GB', back=1, max_results=100) 
    if todays_birds.update != todays_birds.past_observations:
        todays_birds.past_observations = [bird for bird in todays_birds.update if bird not in todays_birds.past_observations]
    else:
        print("no new birds spotted")
    scheduler.enter(3600, 1, birdwatch, (name,))
    
def chorus(name2):
    if todays_birds.queue:
        time.sleep(randrange(300))
        species = todays_birds.queue[0]["speciesCode"]
        todays_birds.queue = list(filter(lambda i: i['speciesCode'] != species, todays_birds.queue))
        song(species)
        del birdsong[0]
        print(len(todays_birds.queue))
    scheduler.enter(3, 1, chorus, (name2,))

update = get_observations(api_key, 'GB', back=1, max_results=100)
todays_birds = birds(update, update, update)

scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(1, 1, chorus, (scheduler,))
scheduler.enter(1, 1, birdwatch, (scheduler,))
scheduler.run()
