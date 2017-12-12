from graphene import relay, ObjectType, Schema
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from yoda_speak.models import YodaPhrase, Padawan
from yoda_speak.serializers import YodaPhraseSerializer


class YodaPhraseNode(DjangoObjectType):
  class Meta:
    model = YodaPhrase
    only_fields = ('phrase', 'translation', 'jedi', 'sith', 'created', 'url', 'padawan')
    filter_fields = {
      'phrase': ['exact', 'icontains', 'istartswith'],
    }
    interfaces = (relay.Node, )

class Query(ObjectType):
    all_yoda_phrases = DjangoFilterConnectionField(YodaPhraseNode)
    # def resolve_all_yoda_phrases (self, info):
    #
    #     return Post.objects.filter(author=info.context.user)

from graphene_django.views import GraphQLView


schema = Schema(query=Query)
