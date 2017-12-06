from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from suds.client import Client

import boto3
s3 = boto3.resource('s3')
polly_client = boto3.client('polly')

# response = client.synthesize_speech(
#     OutputFormat='mp3',
#     Text='<speak><amazon:effect name="whispered" vocal-tract-length="-500%">\
#         <prosody rate="x-slow" pitch="x-low" volume= "x-loud">{}<break time=".25s"/></prosody>\
#         </amazon:effect></speak>'.format('I am Yoda, heeheehee.'),
#     TextType='ssml',
#     VoiceId='Matthew'
# )
# response_id = response['ResponseMetadata']['RequestId']
# response_blob = response['AudioStream']
# # print(response_blob)
#
# s3.meta.client.upload_fileobj(response_blob, 'my-video-project', '{}.mp3'.format(response_id))

# add webtokens for authentication(either from Google or from my web app)
# import models
# import serializers?

@api_view(['GET', 'POST'])
def google_endpoint (request):
    print(request.data)
    if request.method == 'GET':
        return start_conversation(request)

    if request.data['inputs'][0]['intent'] == 'actions.intent.MAIN':
        return start_conversation(request)
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
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/help.mp3\">Help you I can, yes.</audio></speak>"
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
    print('request', request.data['inputs'][0]['arguments'][0]['textValue'])
    untranslated_text = request.data['inputs'][0]['arguments'][0]['textValue']
    client = Client("http://www.yodaspeak.co.uk/webservice/yodatalk.php?wsdl")
    result = client.service.yodaTalk(untranslated_text)

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

    s3.meta.client.upload_fileobj(response_blob, 'my-video-project', 'yoda_speak/{}.mp3'.format(response_id))
    print(result)

    yoda_mp3_link = "https://s3.amazonaws.com/my-video-project/yoda_speak/{}.mp3".format(response_id)
    print(yoda_mp3_link)

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
                    "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/yoda_speak/0567a688-da35-11e7-ad4b-bd742cdd6ad3.mp3\"\></speak>",
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
        # return response in speech to Google Home or to my front-end
