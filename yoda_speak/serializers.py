from rest_framework import serializers

from yoda_speak.models import YodaPhrase


class YodaPhraseSerializer(serializers.ModelSerializer):
  author_id = serializers.IntegerField(required=True)
  blog_id = serializers.IntegerField(required=True)
  class Meta:
      model = YodaPhrase
      fields = ('phrase', 'translation', 'jedi', 'sith', 'created', 'url', 'padawan')

  def create(self, validated_data):
    print(validated_data)
    return Post.objects.create(**validated_data)
