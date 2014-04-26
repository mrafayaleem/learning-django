import datetime

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms.extras.widgets import SelectDateWidget

from accounts.models import DubizzleUser


class DubizzleUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = DubizzleUser
        fields = ('email', 'password')

    def clean_password(self):
        return self.initial["password"]


class DubizzleUserProfileChangeForm(forms.ModelForm):
    """
    This is the the model form for the Dubizzle user profile page.
    """
    YEAR = (
        range(1921, datetime.datetime.now().year + 1)
    )
    dob = forms.DateField(widget=SelectDateWidget(years=YEAR), )
    ocassional_updates = forms.BooleanField(required=False, label='Allow Dubizzle to send me ocassional updates about '
                                                                  'the site.', initial=True)
    amazing_offers = forms.BooleanField(required=False, label='Send me amazing offers and bargains from our advertising'
                                                              'partners.')

    class Meta:
        model = DubizzleUser
        fields = ('mother_call', 'passport', 'dob', 'company_call', 'academics', 'ocassional_updates', 'amazing_offers')
