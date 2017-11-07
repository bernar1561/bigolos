from django.contrib import admin
from .models import *
# Register your models here.

#
# class LikeInlines(admin.TabularInline):
#     model = Like
#     extra = 1

#
# @admin.register(Nominees)
# class NominansAdmin(admin.ModelAdmin):
#

admin.site.register(Nominees)
admin.site.register(Show)
admin.site.register(LikeDislike)
admin.site.register(UserGolos)