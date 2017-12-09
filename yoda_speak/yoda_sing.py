from rest_framework.response import Response

# def happy_bday (request):
#     # happy birthday yoda_style
        #happy birthday to you, happy birthday to you, you look like a wookie. And you smell like one too.
# "https://s3.amazonaws.com/my-video-project/mp3/yoda_happy_birthday.mp4"

# def christmas_carol (request):
#     # we wish you a merry christmas
# "https://s3.amazonaws.com/my-video-project/mp3/yoda_christmas.mp4"

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
