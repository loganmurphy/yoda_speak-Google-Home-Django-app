from rest_framework.response import Response


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

def end_conversation(response):
    response = {
      'expectUserResponse': False,
      'finalResponse': {
        'richResponse': {
          'items': [
            {
              'simpleResponse': {
                "ssml": "<speak><audio src=\"https://s3.amazonaws.com/my-video-project/mp3/may_the_force_be_with_you.webm\">May the Force be with you.</audio></speak>"
              }
            }
          ]
        }
      }
    }

    r = Response(response)
    r['Google-Assistant-API-Version'] = 'v2'
    return r
