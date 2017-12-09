from django.contrib import admin
from yoda_speak.models import YodaPhrase, Padawan


@admin.register(Padawan)
class PadawanAdmin(admin.ModelAdmin):
    list_display = ('userID', )

@admin.register(YodaPhrase)
class YodaPhraseAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'translation', 'jedi', 'sith', 'created', 'url', 'padawan')
    list_filter = ('created', )
    search_fields = ('phrase', )

class Meta:
  ordering = ['-created']
