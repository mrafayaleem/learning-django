from django import forms


class AuthenticationForm(forms.Form):
    """
    Dubizzle login form.
    """
    email = forms.EmailField(widget=forms.widgets.TextInput, label='Enter your email address:')
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']