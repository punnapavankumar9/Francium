from django.contrib import admin
from .models import Room, Topic, Message, User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

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
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Room)