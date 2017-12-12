from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.utils import timezone

from yoda_speak.models import YodaPhrase, Padawan
from yoda_speak.serializers import YodaPhraseSerializer


from yoda_speak.wise_yoda import yoda_wisdom, get_age, my_fortune, darkside
from yoda_speak.yoda_sing import seagull_song, happy_bday, christmas_carol
from yoda_speak.yoda_time import ask_time, ask_day
from yoda_speak.yoda_translate import get_phrase, sith_vs_jedi
from yoda_speak.yoda_options import get_options
from yoda_speak.yoda_conversation import start_conversation, end_conversation


@api_view(['GET', 'POST'])
def google_endpoint (request):
    print('request', request.data)

    user_id = request.data['user']['userId']
    padawan = Padawan.objects.get(userID = user_id)
    jedi_score = YodaPhrase.objects.filter(padawan = padawan).filter(jedi=True).count()
    sith_score = YodaPhrase.objects.filter(padawan = padawan).filter(sith=True).count()

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
    if intent == 'actions.intent.MAIN' or requested.lower() in restart_conversation_commands:
        return start_conversation(request)
    else:
        if (requested.lower() == 'what can I say' or 'options' in requested.lower()):
            return get_options(request)
        elif (requested.lower() in time_queries):
            return ask_time(request)
        elif (requested.lower() in day_queries):
            return ask_day(request)
        elif ('wisdom' in requested.lower()):
            return yoda_wisdom(request)
        elif ('fortune' in requested.lower()):
            return get_age(request)
        elif (requested.isdigit() == True):
            age = int(requested)
            return my_fortune(request, age)
        elif ('seagull song' in requested):
            return seagull_song(request)
        elif (requested.lower() in birthday_queries):
            return happy_bday(request)
        elif (requested.lower() in christmas_queries):
            return christmas_carol(request)
        elif (requested.lower() in dark_vs_light_queries):
            return sith_vs_jedi(request, jedi_score, sith_score)
        elif (requested.lower() in swear_word_check):
            return darkside(request)
        elif (requested.lower() in end_conversation_commands):
            return end_conversation(request)
        else:
            return get_phrase(request)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def yoda_get (request):
    print(request.data)
    yoda_phrases = YodaPhrase.objects.all()
    serializer = YodaPhraseSerializer(yoda_phrases, many=True)
    return Response(serializer.data)
