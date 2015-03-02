from django.contrib import admin
from .models import Profile, Startup, Incubator
from django.contrib.auth.admin import UserAdmin

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'profiles')

	def profiles(self, obj):
		return ', '.join(profile.email for profile in obj.profiles.all())
	profiles.short_description = 'Profiles'

@admin.register(Profile)
class ProfileAdmin(UserAdmin):
	# The forms to add and change user instances

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('email', 'is_staff', 'is_superuser')
	list_filter = ('is_superuser','is_staff')
	fieldsets = (
		(None, {'fields': ('email', 'password', 'startup')}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password')}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()