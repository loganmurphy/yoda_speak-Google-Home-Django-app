from rest_framework.response import Response


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
