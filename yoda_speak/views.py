from rest_framework.response import Response
from rest_framework.decorators import api_view
from yoda_speak.models import YodaPhrase, Padawan

from django.utils import timezone

from yoda_speak.wise_yoda import yoda_wisdom, get_age, my_fortune
from yoda_speak.yoda_sing import seagull_song, happy_bday, christmas_carol
from yoda_speak.yoda_time import ask_time, ask_day
from yoda_speak.yoda_translate import get_phrase
# , sith_vs_jedi

# add webtokens for authentication(either from Google or from my web app)?
# import serializers?

@api_view(['GET', 'POST'])
def google_endpoint (request):
    print('request', request.data)

    # user_id = request.data['user']['userId']
    # padawan = Padawan.objects.get(userID = user_id)
    # # yoda_phrase = YodaPhrase.objects.filter(padawan = padawan).order_by('-created')[:1]
    # jedi_score = YodaPhrase.objects.filter(padawan = padawan).filter(jedi=True).count()
    # sith_score = YodaPhrase.objects.filter(padawan = padawan).filter(jedi=True).count()

    time_queries = ["what time is it Yoda", "what time is it", "what's the time"]
    day_queries = ["what day is it Yoda", "what day is it today", "what day is it"]
    dark_vs_light_queries = [
            'am i a jedi or sith', 'am i a jedi', 'am i a sith', 'am i on the lightside of the force',
            'am i on the darkside of the force', 'am i lightside', 'am i darkside'
        ]
    swear_word_check = ['fuck', 'shit', 'dick', 'pussy', 'cunt', 'asshole', 'whore', 'bitch']
    birthday_queries = ['birthday', 'happy birthday', 'sing happy birthday']
    christmas_queries = ['christmas', 'merry christmas', 'sing merry christmas']
    end_conversation_commands = ['end', 'finish', 'stop', 'end conversation', 'finish conversation', 'stop conversation']
    restart_conversation_commands = ['hey yoda', 'hey, yoda']
    requested = request.data['inputs'][0]['rawInputs'][0]['query']
    intent = request.data['inputs'][0]['intent']
    print (requested)
    if intent == 'actions.intent.MAIN' or requested in restart_conversation_commands:
        return start_conversation(request)
    else:
    #     if (requested.lower() == 'what can I say' or 'options' in requested.lower()):
    #         return get_options(request)
    #     elif (requested.lower() in time_queries):
    #         return ask_time(request)
    #     elif (requested.lower() in day_queries):
    #         return ask_day(request)
    #     elif ('wisdom' in requested.lower()):
    #         return yoda_wisdom(request)
    #     elif ('fortune' in requested.lower()):
    #         return get_age(request)
    #     elif (requested.isdigit() == True):
    #         age = int(requested)
    #         return my_fortune(request, age)
    #     elif ('seagull song' in requested):
    #         return seagull_song(request)
    #     elif (requested.lower() in birthday_queries):
    #         return happy_bday(request)
    #     elif (requested.lower() in christmas_queries):
    #         return christmas_carol(request)
    #     # elif (requested.lower() in dark_vs_light_queries):
    #     #     return sith_vs_jedi(request, jedi_score, sith_score)
    #     elif (requested.lower() in swear_word_check):
    #         return darkside(request)
    #     elif (requested.lower() in end_conversation_commands):
    #         return end_conversation(request)
    #     else:
            return get_phrase(request)

def start_conversation (request):
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
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/yoda_help.mp3\">Help you I can, yes.</audio></speak>"
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

def get_options(request):
    # options = """"Teach you to speak like me, can I. If you are Sith or Jedi, tell you can I.
    #   What day it is, ask me. What time it is, ask me. Your fortune, ask me.
    #   For wisdom, ask me. Happy birthday, for you I will sing. Merry Christmas, too will I sing."""
    options = "https://s3.amazonaws.com/my-video-project/mp3/%22Teach+you+to+speak+like+me%2C+can+I.+If+you+are+Sith+or+Jedi%2C+tell+you+can+I.%0A++++++What+day+it+is%2C+ask+me.+What+time+it+is%2C+ask+me.+Your+fortune%2C+ask+me.%0A++++++For+wisdom%2C+ask+me.+Happy+birthday%2C+for+you+I+will+sing.+Merry+Christmas%2C+too+will+I+sing..mp3"
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
                    "ssml": "<speak><audio src=\"{}\">Options, yes, many options have you.</audio></speak>".format(options)
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

def end_conversation(response):
    response = {
      'expectUserResponse': False,
      'expectedInputs': [
        {
          'possibleIntents': {'intent': 'actions.intent.TEXT'},
          'inputPrompt': {
            'richInitialPrompt': {
              'items': [
                {
                  'simpleResponse': {
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/end_conversation.mp3\"></audio></speak>"
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

# @api_view(['GET'])
# def yoda_get:
    # check for Google token or my front-end webtoken
    # make yoda api call here

# @api_view(['POST'])
# def yoda_post:
    # return response in speech to front-end
