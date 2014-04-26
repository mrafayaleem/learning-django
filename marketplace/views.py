from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import RequestContext
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from marketplace.models import GenericMotorAd, CarAd, MotorCycleAd
from marketplace.forms import CarAdForm, MotorCycleAdForm


AD_PLACEMENT_CATEGORIES = {
    'motors': 'motors',
}


def dubai_home(request):
    type_objects_count = [len(CarAd.objects.all()),
                          len(MotorCycleAd.objects.all())]

    motor_ad_types = [(ad_type[0], ad_type[1], ad_type[2], type_objects_count[i]) for i, ad_type
                      in enumerate(GenericMotorAd.CATEGORY_ID)]

    return render_to_response('marketplace/dubai-home.html', {
        'motor_ad_types': motor_ad_types,
        'user_short_name': request.session.get('user_short_name', None),
    })


def ad_listing(request, category):
    if category == GenericMotorAd.CATEGORY_DICT['used-cars']:
        car_ads = CarAd.objects.all()[:15][::-1]

        ads = car_ads

        return render_to_response('marketplace/ad-listing-car.html', {
            'ads': ads,
            'user_short_name': request.session.get('user_short_name', None),
        })
    elif category == GenericMotorAd.CATEGORY_DICT['motorcycles']:
        raise Http404
    else:
        raise Http404


CATEGORY_DICT = {'used-cars': 'Cars', 'motorcycles': 'Motorcycles'}


class MotorCategoryDisplayView(TemplateView):
    """
    This view displays all the motor categories such as used cars, motor cycles, heavy vehicles, etc.
    """
    template_name = 'marketplace/taxonomy/motors.html'

    def get_context_data(self, **kwargs):
        context = super(MotorCategoryDisplayView, self).get_context_data(**kwargs)
        href = '%s/'
        template_tuple = tuple((href % key, value) for key, value in CATEGORY_DICT.iteritems())
        # template_dict = {href % value: key for key, value in CATEGORY_DICT.iteritems()}
        context['template_tuple'] = template_tuple
        return context


"""
Is this the right approach for what I am doing here? A bit confused about it. See the following dictionaries below.
"""
LINK_DICT = {'used-cars': 'used-cars', 'motorcycles': 'motorcycles'}
# CAR_MAKES = dict((b, b.replace(' ', '-').lower()) for i, (a, b) in enumerate(CarAd.MAKE))
CAR_MAKES = dict((b.replace(' ', '-').lower(), b) for i, (a, b) in enumerate(CarAd.MAKE))
CAR_MAKES_ENUM_DICT = dict((b.replace(' ', '-').lower(), a) for i, (a, b) in enumerate(CarAd.MAKE))
CAR_MAKES_TUPLE = CarAd.MAKE


class MotorMakeDisplayView(TemplateView):
    """
    This view will list all the makes of a related motor category. Eg: Makes for cars category
    could be Acura, Toyota, etc.
    """
    template_name = 'marketplace/taxonomy/motors.html'

    def get(self, request, *args, **kwargs):
        sub_category = kwargs.get('sub_category')
        href = '%s/'
        if sub_category in LINK_DICT:
            if LINK_DICT[str(sub_category)] == 'used-cars':
                context = self.get_context_data(**kwargs)
                template_tuple = tuple((href % key, value) for key, value in CAR_MAKES.iteritems())
                context['template_tuple'] = template_tuple
                return self.render_to_response(context)
            else:
                raise Http404
        else:
            raise Http404


class MotorModelDisplayView(TemplateView):
    """
    This view will list all the models for a related make. Eg: Models for Toyota could be Corolla, Hilux, etc.
    """
    template_name = 'marketplace/taxonomy/motors.html'

    def get(self, request, *args, **kwargs):
        sub_category = kwargs.get('sub_category')
        make = kwargs.get('make')
        href = '%s/'
        if sub_category in LINK_DICT:
            if LINK_DICT[sub_category] == 'used-cars' and make in CAR_MAKES:
                context = self.get_context_data(**kwargs)
                enum = CAR_MAKES_ENUM_DICT[make]
                choice_tuple = CarAd.MODEL[enum]
                choice_tuple = tuple((href % b.replace(' ', '-').replace('/', '').lower(), b) for i, (a, b)
                                     in enumerate(choice_tuple))
                template_tuple = choice_tuple
                context['template_tuple'] = template_tuple
                return self.render_to_response(context)
            else:
                raise Http404
        else:
            raise Http404


class MotorAdRedirectView(RedirectView):
    """
    A simple redirect view that would convert a url like /place-an-ad/taxonomy/motors/used-cars/aston-martin/cygnet/ to
    /place-an-ad/motors/used-cars/aston-martin/cygnet/new/. That is, will redirect to a form view.
    """
    permanent = False
    query_string = True
    pattern_name = 'marketplace:motor-ad-form'

    def get_redirect_url(self, *args, **kwargs):
        return super(MotorAdRedirectView, self).get_redirect_url(*args, **kwargs)


class MotorAdFormView(FormView):
    """
    The actual motor ad form view. Note that this form would not require you to enter model and make for the motor ads.
    They will be retrieved from URL parameters passed during the redirection.
    """
    template_name = 'marketplace/adforms/used-cars.html'
    form_class = CarAdForm
    success_url = reverse_lazy('marketplace:dubai-home')

    def get(self, request, *args, **kwargs):
        if contains_valid_motor_arguments(**kwargs):
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            context = self.get_context_data(form=form, sub_category=kwargs.get('sub_category'), make=kwargs.get('make'),
                                            model=kwargs.get('model'))
            return self.render_to_response(context)
        else:
            raise Http404

    def post(self, request, *args, **kwargs):
        if contains_valid_motor_arguments(**kwargs):
            form_class = self.get_form_class()
            form = self.get_form(form_class, request=request)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            raise Http404

    def get_form(self, form_class, request=None):
        """
        This method is overridden to provide request argument to the form object so that an ad can be saved against
        a user.
        """
        return form_class(request=request, **self.get_form_kwargs())

    def form_valid(self, form):
        kwargs = self.kwargs
        sub_category = kwargs.get('sub_category')
        make = kwargs.get('make')
        model = kwargs.get('model')

        if sub_category in LINK_DICT:
            if LINK_DICT[sub_category] == 'used-cars' and make in CAR_MAKES:
                car_make_enum = CAR_MAKES_ENUM_DICT[make]
                car_model_dict = CarAd.MODEL[car_make_enum]
                car_model_dict = dict((b.replace(' ', '-').replace('/', '').lower(), a) for i, (a, b)
                                      in enumerate(car_model_dict))
                if model in car_model_dict:
                    # Actually adding the models and makes here.
                    ad = form.save(commit=False)
                    ad.make = car_make_enum
                    ad.model = car_model_dict[model]
                    form.save()
                    return super(MotorAdFormView, self).form_valid(form)
                else:
                    raise Http404
            else:
                raise Http404
        else:
            raise Http404

    def form_invalid(self, form):
        """
        Overridden this because we are generating the post action dynamically.
        """
        kwargs = self.kwargs
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(form=form, sub_category=kwargs.get('sub_category'), make=kwargs.get('make'),
                                        model=kwargs.get('model'))
        return self.render_to_response(context)


def contains_valid_motor_arguments(**kwargs):
    sub_category = kwargs.get('sub_category', None)
    make = kwargs.get('make', None)
    model = kwargs.get('model', None)

    assert sub_category is not None
    assert make is not None
    assert model is not None

    if LINK_DICT[sub_category] == 'used-cars' and make in CAR_MAKES:
        car_make_enum = CAR_MAKES_ENUM_DICT[make]
        car_model_dict = CarAd.MODEL[car_make_enum]
        car_model_dict = dict((b.replace(' ', '-').replace('/', '').lower(), a) for i, (a, b)
                              in enumerate(car_model_dict))
        if model in car_model_dict:
            return True
        return False
    return False