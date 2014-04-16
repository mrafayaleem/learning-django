import datetime

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from accounts.models import DubizzleUser


class RegistrationForm(forms.ModelForm):
    """
    Dubizzle registration form.
    """
    YEAR = (
        range(1921, datetime.datetime.now().year + 1)
    )
    MOTHER_CALL = (
        ('', '- Select One -'), (0, 'Habibi (M)'), (1, 'Habibti (F)'),
    )

    COUNTRIES = (
        ('', '- Select One -'), (0, 'Pakistan'), (1, 'United States'),
    )

    COMPANY_CALL = (
        ('', '- Select One -'), (0, 'Student/Intern'), (1, 'Junior'), (2, 'Mid-level'),
    )

    ACADEMIC = (
        ('', '- Select One -'), (0, 'Bachelors Degree'), (1, 'Masters Degree'),
    )

    email1 = forms.EmailField(widget=forms.widgets.TextInput, label='Email Address')
    email2 = forms.EmailField(widget=forms.widgets.TextInput, label='Confirm Email')
    password1 = forms.CharField(widget=forms.widgets.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.widgets.PasswordInput, label='Confirm Password')
    first_name = forms.CharField(widget=forms.widgets.TextInput, label='First Name', max_length=30)
    last_name = forms.CharField(widget=forms.widgets.TextInput, label='Last Name', max_length=30)
    mother_call = forms.ChoiceField(choices=MOTHER_CALL, label='My Mother Calls me', initial='')
    dob = forms.DateField(widget=SelectDateWidget(years=YEAR, attrs={'span': ''}),
                          label='The world became a better place on (d.o.b)',
                          error_messages={'required': 'Please enter a complete date of birth'})
    nationality = forms.ChoiceField(choices=COUNTRIES, label='My Passport tells me I am from')
    company_call = forms.ChoiceField(choices=COMPANY_CALL, label='My friends call me often, but my company calls me')
    academics = forms.ChoiceField(choices=ACADEMIC, label='My highest academic achievement is')
    ocassional_updates = forms.BooleanField(required=False, label='Allow Dubizzle to send me ocassional updates about '
                                                                  'the site.', initial=True)
    amazing_offers = forms.BooleanField(required=False, label='Send me amazing offers and bargains from our advertising'
                                                              'partners.', initial=True)

    class Meta:
        model = DubizzleUser
        fields = ['email1', 'email2', 'password1', 'password2', 'first_name', 'last_name',
                  'mother_call', 'dob', 'nationality', 'company_call', 'academics',
                  'ocassional_updates', 'amazing_offers']

    def clean_email1(self):
        if 'email1' in self.cleaned_data:
            try:
                user = DubizzleUser.objects.get(email=self.cleaned_data['email1'])
                if user:
                    self._errors['email1'] = 'This email address is already in use. Please supply a different ' \
                                             'email address or login above.'
            except DubizzleUser.DoesNotExist:
                return self.cleaned_data['email1']
        return self.cleaned_data['email1']

    def clean(self):
        """
        Some after clean form validation.
        """
        if 'email1' in self.cleaned_data and 'email2' in self.cleaned_data:
            if self.cleaned_data['email1'] != self.cleaned_data['email2']:
                self._errors['email1'] = 'Email addresses must match.'
                self._errors['email2'] = 'Email addresses must match.'
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                self._errors['password1'] = 'Both passwords much match.'
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email1']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user





