from django.contrib import admin
from .models import Blog, Page, Message, UserProfile

admin.site.register(Blog)
admin.site.register(Page)
admin.site.register(Message)
admin.site.register(UserProfile)
