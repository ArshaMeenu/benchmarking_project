from django.contrib import admin

from .models import Competition, Footballer, Team

admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(Footballer)
