from rest_framework.response import Response

def happy_bday (request):
    yoda_bday = "https://s3.amazonaws.com/my-video-project/mp3/yoda_happy_birthday.mp4"
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
                    "ssml": "<speak><audio src=\"{}\">To you, happy birthday.</audio></speak>".format(yoda_bday)
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

def christmas_carol (request):
    yoda_christmas = "https://s3.amazonaws.com/my-video-project/mp3/yoda_christmas.mp4"
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
                    "ssml": "<speak><audio src=\"{}\">You a merry Christmas, we wish.</audio></speak>".format(yoda_christmas)
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

def seagull_song (request):
    seagulls = "https://s3.amazonaws.com/my-video-project/mp3/seagulls.mp4"
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
                    "ssml": "<speak><audio src=\"{}\">Seagulls!</audio></speak>".format(seagulls)
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
