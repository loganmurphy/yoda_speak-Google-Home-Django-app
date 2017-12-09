from rest_framework.response import Response
from suds.client import Client

import boto3
import botocore

from yoda_speak.models import YodaPhrase, Padawan

s3 = boto3.resource('s3')
polly_client = boto3.client('polly')

bucket = s3.Bucket('my-video-project')

CLIENT = Client("http://www.yodaspeak.co.uk/webservice/yodatalk.php?wsdl")


def get_phrase(request):
    user_id = request.data['user']['userId']
    untranslated_text = request.data['inputs'][0]['arguments'][0]['textValue']
    result = CLIENT.service.yodaTalk(untranslated_text)
    words = sorted(untranslated_text.replace(",", "").replace("?", "").replace(".", "").replace("!", "").lower().split())
    result_list = sorted(result.replace(",", "").replace("?", "").replace(".", "").replace("!", "").lower().split())

    for word in words:
        if word not in result_list:
            print('You are a dirty Sith, out of my sight!', word)
            padawan, created = Padawan.objects.get_or_create(userID=user_id)
            yoda_phrase, created = YodaPhrase.objects.get_or_create(
                phrase=untranslated_text, translation=result, sith=True, padawan=padawan
                )
            if created:
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

                upload = s3.meta.client.upload_fileobj(response_blob, 'my-video-project', 'mp3/{}.mp3'.format(response_id))
                yoda_mp3_link = "mp3/{}.mp3".format(response_id)

                object_acl = s3.ObjectAcl('my-video-project', '{}'.format(yoda_mp3_link))
                boto_response = object_acl.put(ACL='public-read')
                yoda_phrase.url = "https://s3.amazonaws.com/my-video-project/mp3/{}.mp3".format(response_id)
                yoda_phrase.save()

            else:
                print('aleady created')

        else:
            print('You are true and honorable Jedi.', word)
            padawan, created = Padawan.objects.get_or_create(userID=user_id)
            yoda_phrase, created = YodaPhrase.objects.get_or_create(
                phrase=untranslated_text, translation=result, jedi=True, padawan=padawan
                )
            if created:
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

                upload = s3.meta.client.upload_fileobj(response_blob, 'my-video-project', 'mp3/{}.mp3'.format(response_id))
                yoda_mp3_link = "mp3/{}.mp3".format(response_id)

                object_acl = s3.ObjectAcl('my-video-project', '{}'.format(yoda_mp3_link))
                boto_response = object_acl.put(ACL='public-read')
                yoda_phrase.url = response_id
                yoda_phrase.save()

            else:
                print('aleady created', yoda_phrase.url)


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
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/{}.mp3\">{}</audio></speak>".format(yoda_phrase.url, result)
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

def sith_vs_jedi(response):
    # determines if asker is jedi or sith
    padawan, created = Padawan.objects.get_or_create(userID=user_id)
    print(padawan.userID)
# padawan.objects.set_yodaphrase.all()
# YodaPhrase.objects.filter(padawan=padawan)
# sith vs jedi points