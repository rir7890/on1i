from django.contrib import admin
from .models import app_user_mst, UserProfile, LinkProfile

admin.site.register(app_user_mst)
admin.site.register(UserProfile)
admin.site.register(LinkProfile)
