from django.contrib import admin
from leads.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(Category)
admin.site.register(UserProfile)
