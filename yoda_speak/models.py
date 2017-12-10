from django.db import models
from django.conf import settings


class Padawan(models.Model):
    userID = models.CharField(max_length=250, unique=True)

    def __str__ (self):
      return self.userID

class YodaPhrase(models.Model):
    phrase = models.TextField(null=True)
    translation = models.TextField(null=True)
    url = models.CharField(max_length=250, blank=True, null=True)
    jedi = models.BooleanField(default=False)
    sith = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    padawan = models.ForeignKey(Padawan, on_delete=models.CASCADE)

    def __str__ (self):
      return self.phrase
