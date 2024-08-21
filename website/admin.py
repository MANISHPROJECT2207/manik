from django.contrib import admin
from .models import Item, Subject, Profile, Unit, Feedback

admin.site.register(Item)
admin.site.register(Subject)
admin.site.register(Profile)
admin.site.register(Unit)
admin.site.register(Feedback)