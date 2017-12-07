from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from suds.client import Client
import datetime as Date

import boto3
import botocore

from yoda_speak.models import YodaPhrase, Padawan

s3 = boto3.resource('s3')
polly_client = boto3.client('polly')

bucket = s3.Bucket('my-video-project')

# add webtokens for authentication(either from Google or from my web app)
# import serializers?

@api_view(['GET', 'POST'])
def google_endpoint (request):
    print('request', request.data)

    q =  request.data['inputs'][0]['arguments'][0]['rawText']
    q2 = 'about time'

    if request.method == 'GET':
        return start_conversation(request)

    if request.data['inputs'][0]['intent'] == 'actions.intent.MAIN':
        return start_conversation(request)
    elif q2 in q:
        print('hi!')
        return ask_time(request)

    # elif request.data['inputs'][0]['intent'] == 'actions.intent.TIME':
    #     return ask_time(request)
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

def get_phrase(request):
    # print('request userID', request.data['user']['userId'])

    user_id = request.data['user']['userId']
    untranslated_text = request.data['inputs'][0]['arguments'][0]['textValue']
    client = Client("http://www.yodaspeak.co.uk/webservice/yodatalk.php?wsdl")
    result = client.service.yodaTalk(untranslated_text)
    words = sorted(untranslated_text.replace(".", "").replace("!", "").lower().split())
    result_list = sorted(result.replace(".", "").replace("!", "").lower().split())
    # print(words, result_list)

    for word in words:
        if word not in result_list:
            print('You are a dirty Sith, out of my sight!', word)
            padawan, created = Padawan.objects.get_or_create(userID=user_id)
            yoda_phrase, created = YodaPhrase.objects.get_or_create(
                phrase=untranslated_text, translation=result, sith=True, padawan=padawan
                )
            break
        else:
            print('You are true and honorable Jedi.', word)
            padawan, created = Padawan.objects.get_or_create(userID=user_id)
            yoda_phrase, created = YodaPhrase.objects.get_or_create(
                phrase=untranslated_text, translation=result, jedi=True, padawan=padawan
                )
    # fear/darkside mp3
    # padawan.objects.set_yodaphrase.all()
    # YodaPhrase.objects.filter(padawan=padawan)


    response = polly_client.synthesize_speech(
        OutputFormat='mp3',
        Text='<speak><amazon:effect name="whispered" vocal-tract-length="-500%">\
            <prosody rate="x-slow" pitch="x-low" volume= "x-loud">{}<break time=".25s"/></prosody>\
            </amazon:effect></speak>'.format(result),
        TextType='ssml',
        VoiceId='Matthew'
    )
    response_id = response['ResponseMetadata']['RequestId']
    response_blob = response['AudioStream']
    # print(response_blob)

    upload = s3.meta.client.upload_fileobj(response_blob, 'my-video-project', 'mp3/{}.mp3'.format(response_id))
    # print(response_id)
    yoda_mp3_link = "mp3/{}.mp3".format(response_id)

    object_acl = s3.ObjectAcl('my-video-project', '{}'.format(yoda_mp3_link))
    boto_response = object_acl.put(ACL='public-read')

    # django storage package
    # yp = YodaPhrase(text=untranslated_text, padawan=padawan)
    # yp.mp3.upload('filename', response_blob)
    # yp.save()
    # yp.mp3.url

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
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/{}.mp3\">{}</audio></speak>".format(response_id, result)
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

    now = Date.datetime.now().isoformat()

    temp_now = now[11:]
    now = temp_now[0:5]

    print('this is the time', now, temp_now)

    response = polly_client.synthesize_speech(
        OutputFormat='mp3',
        Text='<speak><amazon:effect name="whispered" vocal-tract-length="-500%">\
            <prosody rate="x-slow" pitch="x-low" volume= "x-loud">Right now, {} it is.<break time=".25s"/></prosody>\
            </amazon:effect></speak>'.format(now),
        TextType='ssml',
        VoiceId='Matthew'
    )
    # add in some comment depending on what time of day it is.
    # example: time_comments = ['before 6 am', 'before 12pm', 'around noon', 'after 12 but before 6pm', 'after 8pm']
        # ['for lunch, time it is', 'sleep must I', 'much time for training, still have we!']

    response_id = response['ResponseMetadata']['RequestId']
    response_blob = response['AudioStream']
    # print(response_blob)

    upload = s3.meta.client.upload_fileobj(response_blob, 'my-video-project', 'mp3/{}.mp3'.format(response_id))
    # print(response_id)
    yoda_mp3_link = "mp3/{}.mp3".format(response_id)

    object_acl = s3.ObjectAcl('my-video-project', '{}'.format(yoda_mp3_link))
    boto_response = object_acl.put(ACL='public-read')


    response = {
      'expectUserResponse': True,
      'expectedInputs': [
        {
          'possibleIntents': {'intent': 'actions.intent.TIME'},
          'inputPrompt': {
            'richInitialPrompt': {
              'items': [
                {
                  'simpleResponse': {
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/{}.mp3\">Right now, {} it is.</audio></speak>".format(response_id, now)
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

# def ask_day (request):
#     # what day is it?
#
# def yoda_wisdom (request):
#     # q = 'Talk to yodaspeak about wisdom'
#     # returns random yoda wise quote
#
# def happy_bday (request):
#     # happy birthday yoda_style
#
# def ask_time (request):
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
