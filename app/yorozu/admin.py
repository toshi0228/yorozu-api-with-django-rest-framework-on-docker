from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account, Profile, Plan, Tag, Message, Review, Request, Contract

# カスタムユーザーモデルを作った時は、本当にadminもカスタマイズしないといけないのだろうか... 2020 64
# class UserAdmin(BaseUserAdmin):
#     ordering = ["id"]
#     list_diplay = ["email", "name"]

admin.site.register(Account)
admin.site.register(Profile)
admin.site.register(Plan)
admin.site.register(Tag)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(Request)
admin.site.register(Contract)
