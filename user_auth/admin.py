from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active')
    list_display_links = ('id', 'email')
    list_filter = ('first_name', 'last_name', 'is_active', 'is_staff', 'age', 'location')
    search_fields = ('first_name', 'last_name', 'email')
    
admin.site.register(User, UserAdmin)
