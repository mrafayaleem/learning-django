from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import DubizzleUser
from accounts.forms import RegistrationForm, DubizzleUserChangeForm


class DubizzleUserAdmin(UserAdmin):

    form = DubizzleUserChangeForm
    add_form = RegistrationForm

    list_display = ('email', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',  {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff',)})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(DubizzleUser, DubizzleUserAdmin)
