from rest_framework.response import Response

import random

import boto3
import botocore

from yoda_speak.models import YodaPhrase, Padawan

s3 = boto3.resource('s3')
polly_client = boto3.client('polly')

bucket = s3.Bucket('my-video-project')

def yoda_wisdom (request):
    wise_yoda_quotes = [
        "https://s3.amazonaws.com/my-video-project/mp3/beware.wav", "https://s3.amazonaws.com/my-video-project/mp3/feeltheforce.wav",
        "https://s3.amazonaws.com/my-video-project/mp3/for_my_ally.wav", "https://s3.amazonaws.com/my-video-project/mp3/powerful.wav",
        "https://s3.amazonaws.com/my-video-project/mp3/sizemattersnot.wav", "https://s3.amazonaws.com/my-video-project/mp3/throughtheforce.wav",
        "https://s3.amazonaws.com/my-video-project/mp3/use_the_force.wav", "https://s3.amazonaws.com/my-video-project/mp3/trynot.wav",
        "https://s3.amazonaws.com/my-video-project/mp3/anger_fear_aggression.wav"
    ]

    print(random.choice(wise_yoda_quotes))
    quote = random.choice(wise_yoda_quotes)
    response = {
      'expectUserResponse': True,
      'expectedInputs': [
        {
          'possibleIntents': {'intent': 'actions.intent.TEXT'},
          'inputPrompt': {
            'richInitialPrompt': {
              'items': [
                {
                  'simpleResponse': {
                    "ssml": "<speak><audio src=\"{}\">From Master Yoda, learn you must.</audio></speak>".format(quote)
                  }
                }
              ]
            }
          }
        }
      ]
    }

    r = Response(response)
    r['Google-Assistant-API-Version'] = 'v2'
    return r

def get_age(request):
    how_old = "https://s3.amazonaws.com/my-video-project/mp3/how_old_are_you.mp3"

    response = {
      'expectUserResponse': True,
      'expectedInputs': [
        {
          'possibleIntents': {'intent': 'actions.intent.TEXT'},
          'inputPrompt': {
            'richInitialPrompt': {
              'items': [
                {
                  'simpleResponse': {
                    "ssml": "<speak><audio src=\"{}\">You, how old are?</audio></speak>".format(how_old)
                  }
                }
              ]
            }
          }
        }
      ]
    }

    r = Response(response)
    r['Google-Assistant-API-Version'] = 'v2'
    return r

def my_fortune (request, age):
    if age >= 20 and age <= 40:
        fortune_list = [
                "https://s3.amazonaws.com/my-video-project/mp3/become_storm_trooper_will_you.mp3", "https://s3.amazonaws.com/my-video-project/mp3/find_good_deal.mp3",
                "https://s3.amazonaws.com/my-video-project/mp3/look_out.mp3", "https://s3.amazonaws.com/my-video-project/mp3/pod_race.mp3"
            ]
        fortune = random.choice(fortune_list)
    elif age < 20:
        fortune_list = [
                "https://s3.amazonaws.com/my-video-project/mp3/Move.mp3", "https://s3.amazonaws.com/my-video-project/mp3/han-solo.mp3",
                "https://s3.amazonaws.com/my-video-project/mp3/seagulls.mp3", "https://s3.amazonaws.com/my-video-project/mp3/good_things.mp3"
            ]
        fortune = random.choice(fortune_list)
    else:
        fortune_list = [
            "https://s3.amazonaws.com/my-video-project/mp3/find_money.mp3", "https://s3.amazonaws.com/my-video-project/mp3/jedi_master.mp3",
            "https://s3.amazonaws.com/my-video-project/mp3/blue_milk.mp3", "https://s3.amazonaws.com/my-video-project/mp3/new_year.mp3"
            ]
        fortune = random.choice(fortune_list)

    five_dollars = "https://s3.amazonaws.com/my-video-project/mp3/five_dollars.mp3"

    response = {
      'expectUserResponse': True,
      'expectedInputs': [
        {
          'possibleIntents': {'intent': 'actions.intent.TEXT'},
          'inputPrompt': {
            'richInitialPrompt': {
              'items': [
                {
                  'simpleResponse': {
                    "ssml": "<speak><audio src=\"{}\">Your future, read can I!</audio></speak>".format(fortune)
                  }
                }
              ]
            }
          }
        }
      ]
    }

    r = Response(response)
    r['Google-Assistant-API-Version'] = 'v2'
    return r

def darkside(request):
    darkside = "https://s3.amazonaws.com/my-video-project/mp3/darkside.webm"
    response = {
      'expectUserResponse': True,
      'expectedInputs': [
        {
          'possibleIntents': {'intent': 'actions.intent.TEXT'},
          'inputPrompt': {
            'richInitialPrompt': {
              'items': [
                {
                  'simpleResponse': {
                    "ssml": "<speak><audio src=\"{}\">Beware the darkside of the force.</audio></speak>".format(darkside)
                  }
                }
              ]
            }
          }
        }
      ]
    }

    r = Response(response)
    r['Google-Assistant-API-Version'] = 'v2'
    return r
