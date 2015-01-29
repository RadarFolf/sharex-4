from django.contrib import admin
from .models import Pirate, Harbour, Ship

@admin.register(Pirate)
class PirateAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'ship')
	search_fields = ('name', 'ship__name', 'harbour__name')

@admin.register(Harbour)
class HarbourAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)

@admin.register(Ship)
class ShipAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
