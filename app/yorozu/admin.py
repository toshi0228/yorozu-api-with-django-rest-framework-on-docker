from django.contrib import admin
from .models import Account, Profile, Plan, Tag, Message, Review


admin.site.register(Account)
admin.site.register(Profile)
admin.site.register(Plan)
admin.site.register(Tag)
admin.site.register(Message)
admin.site.register(Review)
