from rest_framework.response import Response

import boto3
import botocore

import datetime
import pytz

from django.utils import timezone

from yoda_speak.models import YodaPhrase, Padawan

s3 = boto3.resource('s3')
polly_client = boto3.client('polly')

bucket = s3.Bucket('my-video-project')

tz_now = timezone.now()
central = pytz.timezone('US/Central')

def ask_time (request):
    now = tz_now.astimezone(central).time().isoformat()
    temp_now = now[0:5]
    now = temp_now

    if int(now[0:2]) < 7 and int(now[0:2]) > 4:
        yoda_message = 'Early it is, much time for training, still have we!'
    elif int(now[0:2]) >= 12 and int(now[0:2]) < 13:
        yoda_message = 'For lunch, time it is.'
    elif int(now[0:2]) >= 22 or int(now[0:2]) <= 2:
        yoda_message = 'Late it is. Sleep must I.'
    else:
        yoda_message = 'To start training, time it is.'

    if int(now[0:2]) > 12:
        yoda_time = str(int(now[0:2]) - 12) + now[2:]
    elif int(now[0:2] == 00):
        yoda_time = '12' + now[2:]
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

def ask_day (request):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = tz_now.astimezone(central).weekday()
    today = days_of_week[day]
    yoda_message = 'May the force be with you.'
    response = polly_client.synthesize_speech(
      OutputFormat='mp3',
      Text='<speak><amazon:effect name="whispered" vocal-tract-length="-500%">\
          <prosody rate="x-slow" pitch="x-low" volume= "x-loud">Today, {} it is. {}<break time=".25s"/></prosody>\
          </amazon:effect></speak>'.format(today, yoda_message),
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
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/{}.mp3\">Today, {} it is. {}</audio></speak>".format(response_id, today, yoda_message)
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
