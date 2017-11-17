from django.contrib import admin
from account.models import Account


# This view will allow admin to edit and modify models on web GUI

# Register account info
admin.site.register(Account)