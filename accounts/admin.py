from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    ordering = ('-date_joined', 'email', )
    add_fieldsets = (
                        (
                            None,
                            {
                                "classes": ("wide",),
                                "fields": ("username", "password1", "password2", "email"),
                            },
                        ),
                    )
    fieldsets = (
        *UserAdmin.fieldsets,(
            'Custom fields',
            {
                "fields":('name', 'bio', 'avatar')
            }
        )
    )
    



admin.site.register(User, CustomUserAdmin)