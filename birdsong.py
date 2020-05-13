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
birdsong = []
observations = []
past_observations = []

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
    observations = get_observations(api_key, 'GB', back=1, max_results=10) 
    for i in observations: 
        if i not in past_observations:
            birdsong.append(i)
    past_observations == observations   
    print("birdwatch")
    scheduler.enter(1200, 1, birdwatch, (name,))

def chorus(name2):
    if birdsong:
        time.sleep(randrange(30))
        species = birdsong[0]["speciesCode"]
        song(species)
        del birdsong[0]
        print("birdsong")
    scheduler.enter(30, 1, chorus, (name2,))

scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(30, 1, chorus, (scheduler,))
scheduler.enter(1200, 1, birdwatch, (scheduler,))
#print('START:', time.time())

scheduler.run()
