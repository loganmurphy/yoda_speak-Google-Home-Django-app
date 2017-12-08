from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import datetime
import pytz

from django.utils import timezone

# from yoda_speak.models import YodaPhrase, Padawan
from yoda_speak.wise_yoda import yoda_wisdom, get_age, my_fortune
from yoda_speak.yoda_translate import get_phrase

# add webtokens for authentication(either from Google or from my web app)
# import serializers?

@api_view(['GET', 'POST'])
def google_endpoint (request):
    print('request', request.data)
    time_queries = ["what time is it Yoda", "what time is it", "what's the time"]

    # if request.method == 'GET':
    #     return start_conversation(request)

    if request.data['inputs'][0]['intent'] == 'actions.intent.MAIN':
        return start_conversation(request)
    else:
        if (request.data['inputs'][0]['arguments'][0]['rawText'].lower()) in time_queries:
            print('hi!')
            return ask_time(request)
        elif ('wisdom' in request.data['inputs'][0]['arguments'][0]['rawText'].lower()):
            return yoda_wisdom(request)
        elif ('fortune' in request.data['inputs'][0]['arguments'][0]['rawText'].lower()):
            return get_age(request)
        elif (request.data['inputs'][0]['arguments'][0]['rawText'].isdigit() == True):
            age = int(request.data['inputs'][0]['arguments'][0]['rawText'])
            return my_fortune(request, age)
        else:
            return get_phrase(request)


def start_conversation (request):
    # bucket api key
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
                    # mp3: Yoda voice
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


def ask_time (request):
    tz_now = timezone.now()
    central = pytz.timezone('US/Central')
    now = tz_now.astimezone(central).time().isoformat()
    temp_now = now[0:5]
    now = temp_now
    print(int(now[0:2]))
    # add in some comments depending on what time of day it is.

    if int(now[0:2]) < 7 and int(now[0:2]) > 4:
        yoda_message = 'Early it is, much time for training, still have we!'
        print('Early it is, much time for training, still have we!')
    elif int(now[0:2]) >= 12 and int(now[0:2]) < 13:
        yoda_message = 'For lunch, time it is.'
        print('For lunch, time it is.')
    elif int(now[0:2]) >= 22 or int(now[0:2]) <= 2:
        yoda_message = 'Late it is. Sleep must I.'
        print('Late it is. Sleep must I.')
    else:
        yoda_message = 'To start training, time it is.'
        print('To start training, time it is.')

    print('this is the time', now)

    if int(now[0:2]) > 12:
        yoda_time = str(int(now[0:2]) - 12) + now[2:]
    else:
        yoda_time = now
    print(yoda_time)
    response = polly_client.synthesize_speech(
        OutputFormat='mp3',
        Text='<speak><amazon:effect name="whispered" vocal-tract-length="-500%">\
            <prosody rate="x-slow" pitch="x-low" volume= "x-loud">Right now, {} it is. {}<break time=".25s"/></prosody>\
            </amazon:effect></speak>'.format(yoda_time, yoda_message),
        TextType='ssml',
        VoiceId='Matthew'
    )

    response_id = response['ResponseMetadata']['RequestId']
    response_blob = response['AudioStream']
    upload = s3.meta.client.upload_fileobj(response_blob, 'my-video-project', 'mp3/{}.mp3'.format(response_id))
    yoda_mp3_link = "mp3/{}.mp3".format(response_id)
    object_acl = s3.ObjectAcl('my-video-project', '{}'.format(yoda_mp3_link))
    boto_response = object_acl.put(ACL='public-read')

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
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/{}.mp3\">Right now, {} it is. {}</audio></speak>".format(response_id, yoda_time, yoda_message)
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


# Here are all of the conversations I will have.

# def option:
    #list available conversation options


# def ask_day (request):
#     # what day is it?
#
# def happy_bday (request):
#     # happy birthday yoda_style
        #happy birthday to you, happy birthday to you, you look like a wookie. And you smell like one too.
# def christmas_carol (request):
#     # we wish you a merry christmas
#
# def yoda_reminder (request):
    # add reminders to your calendar


# @api_view(['GET'])
# def yoda_get:
    # check for Google token or my front-end webtoken
    # make yoda api call here

# @api_view(['POST'])
# def yoda_post:
    # return response in speech to front-end
