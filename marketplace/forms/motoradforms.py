from django import forms

from marketplace.models import GenericMotorAd, CarAd, MotorCycleAd
from accounts.models import DubizzleUser


class CarAdForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput, label='Title')
    phone = forms.CharField(widget=forms.NumberInput, label='Phone number')
    price = forms.CharField(widget=forms.NumberInput, label='Price')
    description = forms.CharField(widget=forms.TextInput, label='Description')
    seller_type = forms.ChoiceField(choices=GenericMotorAd.SELLER, label='Seller type')
    warranty = forms.ChoiceField(choices=GenericMotorAd.WARRANTY, label='Warranty')
    location = forms.ChoiceField(choices=GenericMotorAd.LOCATION, label='Location')

    # Ad specific.
    make = forms.ChoiceField(label='Make', required=False, initial=0)
    model = forms.CharField(label='Model', required=False, initial=0)

    year = forms.ChoiceField(choices=CarAd.YEAR, label='Year')
    kilometers = forms.CharField(widget=forms.NumberInput, label='Kilometers')
    color = forms.ChoiceField(choices=CarAd.COLOR, label='Color')
    doors = forms.ChoiceField(choices=CarAd.DOORS, label='Doors')
    body_condition = forms.ChoiceField(choices=CarAd.BODY_COND, label='Body condition')
    mech_condition = forms.ChoiceField(choices=CarAd.MECH_COND, label='Mechanical condition')
    trim = forms.ChoiceField(choices=CarAd.TRIM, label='Trim')
    body_type = forms.ChoiceField(choices=CarAd.BODY_TYPE, label='Body type')
    cylinders = forms.ChoiceField(choices=CarAd.CYLINDERS, label='Cylinders')
    transmission = forms.ChoiceField(choices=CarAd.TRANSMISSION, label='Transmission')
    horse_power = forms.ChoiceField(choices=CarAd.HORSEPOWER, label='Horse power')
    fuel = forms.ChoiceField(choices=CarAd.FUEL, label='Fuel')

    # Extras
    air_conditioning = forms.BooleanField(initial=False, label='Air conditioning', required=False)
    body_kit = forms.BooleanField(initial=False, label='Body kit', required=False)

    # Internal data not to be exposed.
    category_id = forms.ChoiceField(initial=GenericMotorAd.USED_CARS, required=False)

    class Meta:
        model = CarAd
        fields = ['title', 'phone', 'price', 'description', 'year', 'kilometers',
                  'body_condition', 'mech_condition', 'seller_type', 'trim', 'body_type', 'doors', 'cylinders',
                  'color', 'transmission', 'horse_power', 'warranty', 'fuel', 'air_conditioning', 'body_kit',
                  'location'
        ]
        exclude = ['make', 'model']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CarAdForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        ad = super(CarAdForm, self).save(commit=False)
        user_id = self.request.session.get('user_id')  # ID must exist, or else this should have never been called!
        user = DubizzleUser.objects.get(pk=user_id)
        ad.publisher = user
        if commit:
            ad.save()
        return ad


class MotorCycleAdForm(forms.ModelForm):
    pass


class PlaceHolderAdForm(forms.ModelForm):
    class Meta:
        model = CarAd
