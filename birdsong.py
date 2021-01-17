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
import subprocess
api_key = 'insert your key here'

class birds:
    def __init__(self, observation_queue, past_observations):
        self.observation_queue = observation_queue
        self.past_observations = past_observations

def get_birdsong(species):
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


def update_observations():
    latest_observations = get_observations(api_key, 'GB', back=1, max_results=3) 
    if latest_observations != todays_birds.past_observations:
        todays_birds.past_observations = [bird for bird in latest_observations if bird not in todays_birds.past_observations]
    else:
        print("no new birds spotted")
        # wait an hour and hopefully some new birds will appear
        time.sleep(3600)
    
def play_birdsong(name):
    if todays_birds.observation_queue:
        time.sleep(randrange(300))
        species = todays_birds.observation_queue[0]["speciesCode"]
        todays_birds.observation_queue = list(filter(lambda i: i['speciesCode'] != species, todays_birds.observation_queue))
        get_birdsong(species)
        print(len(todays_birds.observation_queue))
    else:
        update_observations()
    scheduler.enter(1, 1, play_birdsong, (name,))

# initialise observations
observations = get_observations(api_key, 'GB', back=1, max_results=3)
todays_birds = birds(observations, observations)

# start birdwatching
scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(1, 1, play_birdsong, (scheduler,))
scheduler.run()
