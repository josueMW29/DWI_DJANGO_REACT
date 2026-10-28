from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'matricula', 'carrera', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'matricula', 'carrera')
    ordering = ('email',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Académica Extra', {'fields': ('matricula', 'carrera')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Académica Extra', {'fields': ('email', 'matricula', 'carrera')}),
    )
