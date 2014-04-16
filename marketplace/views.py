from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext

from marketplace.models import GenericMotorAd, CarAd, MotorCycleAd
from marketplace.forms import CarAdForm, MotorCycleAdForm


AD_PLACEMENT_CATEGORIES = {
    'motors': 'motors',
}


def profile(request):
    if request.user is not None:
        if request.user.is_active:
            request.session['username'] = request.user.username
            request.session['user_id'] = request.user.id
            marketplaceuser = request.user.marketplaceuser if hasattr(request.user, 'marketplaceuser') else None
            if marketplaceuser is not None:
                gender = marketplaceuser.GENDER[marketplaceuser.gender][1]
                return HttpResponse('You are logged in as %s' % request.user.username + 'and you are a %s' % gender)
            else:
                return HttpResponse('You are logged in as %s' % request.user.username)

        else:
            pass
    else:
        return HttpResponse('Username or password was incorrect!')


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


def place_an_ad_select_category(request, ad_category):

    user_id = request.session.get('user_id', None)
    if user_id:
        if ad_category == AD_PLACEMENT_CATEGORIES['motors']:
            #  Show a motor select  where users can select whether it is a car or a bike.
            #  After chosing a category, redirect to the appropriate form where user can fill in data.
            href = '%s/'
            template_dict = {key: (value, href % value) for key, value in GenericMotorAd.CATEGORY_DICT.iteritems()}
            return render_to_response('marketplace/taxonomy/motors.html', {
                'template_dict': template_dict,
            }, context_instance=RequestContext(request))
        else:
            raise Http404
    else:
        return redirect(reverse('accounts:register'))


def place_an_ad_select_sub_category(request, ad_category, sub_category):
    user_id = request.session.get('user_id', None)
    if user_id:
        if ad_category == AD_PLACEMENT_CATEGORIES['motors']:
            if sub_category == GenericMotorAd.CATEGORY_DICT['used-cars']:
                form = CarAdForm()
                return render_to_response('marketplace/adforms/used-cars.html', {
                    'form': form,
                }, context_instance=RequestContext(request))
            elif sub_category == GenericMotorAd.CATEGORY_DICT['motorcycles']:
                raise Http404
                # form = MotorCycleAdForm()
                # return render_to_response('marketplace/adforms/motorcycles.html', {
                #     'form': form
                # }, context_instance=RequestContext(request))
            else:
                raise Http404
        else:
            raise Http404
    else:
        return redirect(reverse('accounts:register'))  # This should be login.


def submit_ad(request, ad_category, sub_category):
    user_id = request.session.get('user_id', None)
    if user_id and request.method == 'POST':
        if ad_category == AD_PLACEMENT_CATEGORIES['motors'] \
                and sub_category == GenericMotorAd.CATEGORY_DICT['used-cars']:
            form = CarAdForm(data=request.POST, request=request)
            if form.is_valid():
                ad = form.save()
                return HttpResponse('Ad was submitted successfully!')
            else:
                pass
            return render_to_response('marketplace/adforms/used-cars.html', {
                'form': form
            }, context_instance=RequestContext(request))
        else:
            raise Http404
    elif user_id:
        return redirect(reverse('marketplace:place-an-ad-select-sub-category',
                                kwargs={'ad_category': ad_category, 'sub_category': sub_category}))
    else:
        return redirect(reverse('accounts:register'))


