"""Package Admin"""
#pylint: disable = no-name-in-module
from django.contrib import admin
from packages.models import Package

admin.site.register(Package)
